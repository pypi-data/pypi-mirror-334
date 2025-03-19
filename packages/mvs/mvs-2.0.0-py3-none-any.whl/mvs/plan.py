import re
import shutil
import sys
import traceback

from copy import deepcopy
from dataclasses import asdict
from itertools import groupby
from os.path import commonprefix, samefile
from pathlib import Path
from short_con import cons

from .constants import CON, STRUCTURES
from .messages import MSG_FORMATS as MF

from .filesys import (
    ANY_EXISTENCE,
    EXISTENCES,
    FS_TYPES,
    PATH_TYPES as PT,
    case_sensitivity,
    determine_path_type,
    is_non_empty_dir,
    path_existence_and_type,
)

from .problems import (
    FAILURE_FORMATS as FF,
    FAILURE_NAMES as FN,
    FAILURE_VARIETIES as FV,
    Failure,
    PROBLEM_FORMATS as PF,
    PROBLEM_NAMES as PN,
    PROBLEM_VARIETIES as PV,
    Problem,
    StrictMode,
)

from .renaming import (
    NAME_CHANGE_TYPES as NCT,
    Renaming,
)

from .utils import (
    MvsError,
    get_source_code,
    indented,
    validated_choices,
)

####
# A class to manage a batch of renamings.
####

class RenamingPlan:

    # Special values used by self.tracking_index.
    #
    # During rename_paths(), we track progress via self.tracking_index. It has
    # two special values, as shown in TRACKING. Otherwise, a non-negative value
    # indicates which Renaming we are currently trying to rename. If an
    # exception occurs, that index tells us which Renaming was in progress. API
    # users of RenamingPlan who care can catch the exception and infer which
    # paths were renamed and which were not. Similarly, CliRenamer logs the
    # necessary information to figure that out.
    #
    TRACKING = cons(not_started = -1, done = None)

    def __init__(self,
                 # Path inputs and their structure.
                 inputs,
                 structure = None,
                 # User code for renaming and filtering.
                 rename_code = None,
                 filter_code = None,
                 indent = 4,
                 # Sequence numbering.
                 seq_start = 1,
                 seq_step = 1,
                 # Problem handling.
                 skip = None,
                 strict = None,
                 ):

        # Input paths and structure.
        self.inputs = tuple(inputs)
        self.structure = structure or STRUCTURES.flat

        # We begin with full universe of Renaming instances (rns).
        # During processing, they get put into four buckets:
        # - rns filtered out by user code;
        # - rns that must be excluded, due to unresolvable problems;
        # - rns the user wants to skip, due to problems;
        # - rns that are still active.
        self.n_initial = None
        self.filtered = []
        self.excluded = []
        self.skipped = []
        self.active = []

        # Attributes holding a breakdown of the active Renaming instances, by
        # problem name. These are populated at the end of prepare() and are
        # used for listing/reporting.
        self.parent = []
        self.exists = []
        self.collides = []
        self.ok = []

        # User-supplied code.
        self.rename_code = rename_code
        self.filter_code = filter_code
        self.filter_func = None
        self.rename_func = None
        self.indent = indent
        self.seq_start = seq_start
        self.seq_step = seq_step
        self.prefix_len = 0

        # Plan state.
        self.has_prepared = False
        self.has_renamed = False
        self.tracking_index = self.TRACKING.not_started
        self.call_at = None

        # Information used when checking Renaming instance for problems.
        self.path_groups = None
        self.collision_key_func = (
            str if case_sensitivity() == FS_TYPES.case_sensitive else
            str.lower
        )

        # Validate and standardize the user's problem-handling parameters.
        self.strict = StrictMode.from_user(strict)
        self.skip = self.validated_str_ids(skip)
        self.skip_lookup = self.build_skip_lookup()

        # Failure halting the plan.
        self.failure = None

    ####
    #
    # Preparation before renaming.
    #
    # This method performs various validations and computations needed before
    # renaming can occur.
    #
    # The method does not raise; rather, it keeps track of information
    # about any failure or problems that occur and organizes the Renaming
    # instances into appropriate buckets based on those problems, if any,
    # and how the user wants to handle them.
    #
    ####

    def prepare(self):
        # Don't prepare more than once.
        if self.has_prepared:
            return
        else:
            self.has_prepared = True

        # Run each step of preparation.
        steps = (
            [True, self.prepare_inputs],
            [True, self.prepare_code, CON.code_actions.filter],
            [True, self.prepare_code, CON.code_actions.rename],
            [False, self.prepare_renamings],
            [False, self.prepare_probs],
            [False, self.prepare_strict],
        )
        for halt_on_fail, step, *xs in steps:
            step(*xs)
            if halt_on_fail and self.failed:
                return

    def prepare_inputs(self):
        # Parse input paths to get the Renaming instances.
        self.active = self.parse_inputs()
        self.n_initial = len(self.active)

    def prepare_code(self, action):
        # Create the filtering/renaming functions from
        # user-supplied code, if any was given.
        func = self.make_user_func(action)
        setattr(self, action + '_func', func)

    def prepare_renamings(self):
        # Run the steps that process Renaming instances individually:
        # - setting their attributes related to path existence/type/etc.
        # - filtering
        # - computing new paths
        # - checking for problems
        rn_steps = (
            (self.set_exists_and_types, None),
            (self.execute_user_filter, None),
            (self.execute_user_rename, None),
            (self.set_exists_and_types, None),
            (self.check_equal, None),
            (self.check_orig_uniq, 'orig'),
            (self.check_orig_exists, None),
            (self.check_orig_type, None),
            (self.check_new_exists, None),
            (self.check_new_parent_exists, None),
            (self.check_new_collisions, 'new'),
        )
        for step, prep_arg in rn_steps:
            # Run preparatory step.
            if prep_arg:
                self.prepare_path_groups(prep_arg)

            # Prepare common-prefix and sequence number iterator, which might
            # be used by the user-suppled renaming/filtering code.
            self.prefix_len = self.compute_prefix_len()
            seq = self.compute_sequence_iterator()

            # Execute the step for each Renaming. Some steps set attributes on
            # the Renaming to guide subsequent filtering, renaming, etc.
            # Steps return a Problem or None.
            still_active = []
            for rn in self.active:
                # Run step and put the Renaming in the appropriate bucket.
                prob = step(rn, next(seq))
                if prob:
                    rn.problem = prob
                xs = (
                    self.filtered if rn.filtered else
                    self.skipped if self.should_skip(rn) else
                    self.excluded if self.should_exclude(rn) else
                    still_active
                )
                xs.append(rn)
                # Set create and clobber attributes on the Renaming.
                if rn.prob_name == PN.parent:
                    rn.create = True
                elif rn.prob_name in (PN.exists, PN.collides):
                    rn.clobber = True
            self.active = still_active

        # Register Failure if everything was filtered out.
        if not self.active:
            self.handle_failure(FN.all_filtered)

    def prepare_probs(self):
        # Populate the lists of active Renaming instances
        # having problems (or not).
        for rn in self.active:
            nm = rn.prob_name
            if nm == PN.parent:
                self.parent.append(rn)
            elif nm == PN.exists:
                self.exists.append(rn)
            elif nm == PN.collides:
                self.collides.append(rn)
            else:
                self.ok.append(rn)

    def prepare_strict(self):
        sm = self.strict
        if not self.passes_strict(sm):
            self.handle_failure(FN.strict, sm.as_str)

    def passes_strict(self, sm):
        # Takes a StrictMode instance.
        # Returns true if the plan passes its settings.
        if sm.excluded and self.excluded:
            return False
        else:
            active_probs = set(rn.prob_name for rn in self.active)
            return all(
                p not in active_probs
                for p in sm.probs
            )

    ####
    # Parsing inputs to obtain the original and, in some cases, new paths.
    ####

    def parse_inputs(self):
        # Parses self.inputs. If valid, returns a tuple of Renaming
        # instances. Otherwise, registers a Failure and returns empty list.

        # Helper to handle a Failure and return empty.
        def do_fail(name, variety, *xs):
            self.handle_failure(name, *xs, variety = variety)
            return []

        # Organize inputs into original paths and new paths.
        if self.structure == STRUCTURES.origs:
            # Just original file paths.
            origs = [orig for orig in self.inputs if orig]
            news = [None for _ in origs]
            if not self.rename_code:
                return do_fail(FN.parsing, FV.origs_rename)

        elif self.structure == STRUCTURES.paragraphs:
            # Paragraphs: first original paths, then new paths.
            # - Group into non-empty vs empty lines.
            # - Ensure exactly two groups of non-empty.
            groups = [
                list(lines)
                for g, lines in groupby(self.inputs, key = bool)
                if g
            ]
            if len(groups) == 2:
                origs, news = groups
            else:
                return do_fail(FN.parsing, FV.paragraphs)

        elif self.structure == STRUCTURES.pairs:
            # Pairs: original path, new path, original, new, etc.
            groups = [[], []]
            i = 0
            for line in self.inputs:
                if line:
                    groups[i % 2].append(line)
                    i += 1
            origs, news = groups

        elif self.structure == STRUCTURES.rows:
            # Rows: original-new path pairs, as tab-delimited rows.
            origs = []
            news = []

            for row in self.inputs:
                if row:
                    cells = row.split(CON.tab)
                    if len(cells) == 2 and all(cells):
                        origs.append(cells[0])
                        news.append(cells[1])
                    else:
                        return do_fail(FN.parsing, FV.row, row)

        else:
            # Flat: like paragraphs without the blank-line delimiter.
            paths = [line for line in self.inputs if line]
            i = len(paths) // 2
            origs, news = (paths[0:i], paths[i:])

        # Failure if we got no paths or unequal original vs new.
        if not origs and not news:
            return do_fail(FN.parsing, FV.no_paths)
        elif len(origs) != len(news):
            return do_fail(FN.parsing, FV.imbalance)

        # Return the Renaming instances.
        return [
            Renaming(orig, new)
            for orig, new in zip(origs, news)
        ]

    ####
    # Creating the user-defined functions for filtering and renaming.
    ####

    def make_user_func(self, action):
        # Get the user's code, if any.
        user_code = getattr(self, f'{action}_code')
        if not user_code:
            return None

        # If the user code is already a callable, just return it.
        if callable(user_code):
            return user_code

        # Define the text of the code.
        func_name = CON.func_name_fmt.format(action)
        code = CON.user_code_fmt.format(
            func_name = func_name,
            user_code = user_code,
            indent = ' ' * self.indent,
        )

        # Create the function via exec() in the context of:
        # - Globals that we want to make available to the user's code.
        # - A locals dict that we can use to return the generated function.
        globs = dict(
            re = re,
            Path = Path,
        )
        locs = {}
        try:
            exec(code, globs, locs)
            return locs[func_name]
        except Exception as e:
            tb = traceback.format_exc(limit = 0)
            self.handle_failure(FN.code, action, indented(tb.lstrip()))
            return None

    ####
    # The steps that process Renaming instance individually.
    # Each step returns a Problem or None.
    ####

    def set_exists_and_types(self, rn, seq_val):
        # This step is called twice, at the beginning and then after user-code
        # for filtering and renaming has been executed. The initial call sets
        # information for rn.orig and, if possible, rn.new. The second call
        # handles rn.new if we have not done so already. The attributes set
        # here are used for most of the subsequent steps.

        # Handle attributes related to rn.orig.
        if rn.exist_orig is None:
            # Existence, type, and non-empty dir.
            e, pt = path_existence_and_type(rn.orig)
            rn.exist_orig = e
            rn.type_orig = pt
            if pt == PT.directory:
                rn.full_orig = is_non_empty_dir(rn.orig)

        # Handle attributes related to rn.new.
        if rn.exist_new is None and rn.new is not None:
            po = Path(rn.orig)
            pn = Path(rn.new)
            # Existence, type, and non-empty dir.
            e, pt = path_existence_and_type(rn.new)
            rn.exist_new = e
            rn.type_new = pt
            if pt == PT.directory:
                rn.full_new = is_non_empty_dir(rn.new)
            # Existence of parent.
            e, _ = path_existence_and_type(pn.parent)
            rn.exist_new_parent = e
            # Attributes characterizing the renaming.
            rn.same_parents = (
                False if rn.exist_new_parent == EXISTENCES.missing else
                samefile(po.parent, pn.parent)
            )
            rn.name_change_type = (
                NCT.noop if po.name == pn.name else
                NCT.case_change if po.name.lower() == pn.name.lower() else
                NCT.name_change
            )

        return None

    def execute_user_filter(self, rn, seq_val):
        if self.filter_code:
            try:
                kws = self.user_func_kwargs(rn, seq_val)
                keep = self.filter_func(**kws)
                if not keep:
                    rn.filtered = True
            except Exception as e:
                return Problem(PN.code, e, rn.orig, variety = PV.filter)
        return None

    def execute_user_rename(self, rn, seq_val):
        if self.rename_code:
            # Compute the new path.
            try:
                kws = self.user_func_kwargs(rn, seq_val)
                new = self.rename_func(**kws)
            except Exception as e:
                return Problem(PN.code, e, rn.orig, variety = PV.rename)
            # Validate its type and either set rn.new or return Problem.
            if isinstance(new, (str, Path)):
                rn.new = str(new)
            else:
                typ = type(new).__name__
                return Problem(PN.code, typ, rn.orig, variety = PV.rename)
        return None

    def user_func_kwargs(self, rn, seq_val):
        return dict(
            o = rn.orig, 
            n = rn.new, 
            po = Path(rn.orig),
            pn = Path(rn.new) if rn.new else None,
            seq = seq_val,
            r = rn,
            plan = self,
        )

    def check_equal(self, rn, seq_val):
        if rn.orig == rn.new:
            return Problem(PN.noop, variety = PV.equal)
        else:
            return None

    def check_orig_uniq(self, rn, seq_val):
        k = self.collision_key_func(rn.orig)
        others = [o for o in self.path_groups[k] if o is not rn]
        if others:
            return Problem(PN.duplicate)
        else:
            return None

    def check_orig_exists(self, rn, seq_val):
        # Key question: is renaming possible?
        if rn.exist_orig in ANY_EXISTENCE:
            return None
        else:
            return Problem(PN.missing)

    def check_orig_type(self, rn, seq_val):
        if rn.type_orig in (PT.file, PT.directory):
            return None
        else:
            return Problem(PN.type)

    def check_new_exists(self, rn, seq_val):
        # Handle situation where rn.new does not exist in any sense.
        # In this case, we can rename freely, regardless of file
        # system type or other renaming details.
        new_exists = (rn.exist_new in ANY_EXISTENCE)
        if not new_exists:
            return None

        # Determine the type of Problem to return if clobbering would occur.
        tnew = rn.type_new
        if tnew == PT.other:
            prob = Problem(PN.exists, variety = PV.other)
        elif tnew == PT.directory and rn.full_new:
            prob = Problem(PN.exists, variety = PV.full)
        elif tnew == rn.type_orig:
            prob = Problem(PN.exists)
        else:
            prob = Problem(PN.exists, variety = PV.diff)

        # Handle the simplest file systems: case-sensistive or
        # case-insensistive. Since rn.new exists, we have clobbering
        if case_sensitivity() != FS_TYPES.case_preserving: # pragma: no cover
            return prob

        # Handle case-preserving file system where rn.orig and rn.new have
        # different parent directories. Since the parent directories differ,
        # case-change-only renaming (ie, self clobber) is not at issue,
        # so we have regular clobbering.
        if not rn.same_parents:
            return prob

        # Handle case-preserving file system where rn.orig and rn.new have
        # the same parent, which means the renaming involves only changes
        # to the name-portion of the path.
        if rn.name_change_type == NCT.noop:
            # New exists because rn.orig and rn.new are functionally the same
            # path. User inputs implied that a renaming was desired (rn.orig
            # and rn.new were not equal) but the only difference lies in the
            # casing of the parent path. By policy, mvs does not rename parents.
            return Problem(PN.noop, variety = PV.same)
        elif rn.name_change_type == NCT.case_change:
            if rn.exist_new == EXISTENCES.exists_case:
                # User inputs implied that a case-change renaming
                # was desired, but the path's name-portion already
                # agrees with the file system, so renaming is impossible.
                return Problem(PN.noop, variety = PV.recase)
            else:
                # User wants a case-change renaming (self-clobber).
                rn.clobber_self = True
                return None
        else:
            # User wants a name-change, and it would clobber something else.
            return prob

    def check_new_parent_exists(self, rn, seq_val):
        # Key question: does renaming also require parent creation?
        # Any type of existence is sufficient.
        if rn.exist_new_parent in ANY_EXISTENCE:
            return None
        else:
            return Problem(PN.parent)

    def check_new_collisions(self, rn, seq_val):
        # Checks for collisions among all of the new paths in the RenamingPlan.
        # If any, returns the most serious variety of a Problem(collides).
        #
        #   - full: collision with non-empty directory
        #   - diff: collision with a path of a different type
        #   - regular collision.
        #
        # To determine the variety, we need to consider the relevant 
        # orig and new attributes of the other files.

        # Get the other Renaming instances that have the same new-path as
        # the current rn. If rn.new is unique, there is no problem.
        k = self.collision_key_func(rn.new)
        others = [o for o in self.path_groups[k] if o is not rn]
        if not others:
            return None

        # Check for collisions with non-empty directories.
        if any(o.full_orig or o.full_new for o in others):
            return Problem(PN.collides, variety = PV.full)

        # Check for collisions with a different path type.
        pt = rn.type_orig
        for o in others:
            if o.type_orig != pt or (o.type_new and o.type_new != pt):
                return Problem(PN.collides, variety = PV.diff)

        # Otherwise, it's a regular collision.
        return Problem(PN.collides)

    def prepare_path_groups(self, attrib):
        # A preparation-step for check_orig_uniq() and check_new_collisions().
        # Organize rns into dict-of-list, keyed by either rn.orig or rn.new.
        # Those keys are stored as-is for case-sensistive file
        # systems and in lowercase for non-sensistive systems.
        self.path_groups = {}
        for rn in self.active:
            path = getattr(rn, attrib)
            k = self.collision_key_func(path)
            self.path_groups.setdefault(k, []).append(rn)

    ####
    # Methods related to failure and problem handling.
    ####

    def handle_failure(self, name, *xs, variety = None):
        # Takes name/args to create a Failure and then stores it.
        f = Failure(name, *xs, variety = variety)
        self.failure = f

    @property
    def failed(self):
        return bool(self.failure)

    def validated_str_ids(self, skip):
        try:
            return validated_choices(skip, Problem.SKIP_CHOICES)
        except Exception:
            msg = MF.invalid_skip.format(skip)
            raise MvsError(msg)

    def build_skip_lookup(self):
        return set(
            prob.sid
            for sid in self.skip
            for prob in Problem.probs_matching_sid(sid)
        )

    def should_skip(self, rn):
        prob = rn.problem
        return prob and prob.sid in self.skip_lookup

    def should_exclude(self, rn):
        prob = rn.problem
        return prob and not prob.is_resolvable

    ####
    # Sequence number and common prefix.
    ####

    def compute_sequence_iterator(self):
        return iter(range(self.seq_start, sys.maxsize, self.seq_step))

    def compute_prefix_len(self):
        origs = tuple(rn.orig for rn in self.active)
        return len(commonprefix(origs))

    def strip_prefix(self, orig):
        i = self.prefix_len
        return str(orig)[i:] if i else orig

    ####
    # Files system operations.
    ####

    def rename_paths(self):
        # Don't rename more than once.
        if self.has_renamed:
            raise MvsError(MF.rename_done_already)
        else:
            self.has_renamed = True

        # Ensure than we have prepared, and raise if it failed.
        self.prepare()
        if self.failed:
            raise MvsError(MF.prepare_failed, failure = self.failure)

        # Rename paths.
        for i, rn in enumerate(self.active):
            self.tracking_index = i
            self.do_rename(rn)
        self.tracking_index = self.TRACKING.done

    def do_rename(self, rn):
        # Takes a Renaming and executes its renaming.

        # For testing purposes, call any needed code in
        # the middle of renaming -- eg, to raise an error
        # of some kind or to affect the file system in some way.
        if self.call_at and self.tracking_index == self.call_at[0]:
            self.call_at[1](self)

        # Set up Path instances.
        po = Path(rn.orig)
        pn = Path(rn.new)

        # Create new parent if requested.
        if rn.create:
            pn.parent.mkdir(parents = True, exist_ok = True)

        # If new path exists already, deal with it before
        # we attempt to renaming from rn.orig to rn.new.
        # We do this for a few reasons.
        #
        # (1) We want to make a best-effort to avoid unintended
        # clobbering, whether due to race conditions (creation
        # of rn.new since the problem-checks were performed)
        # or due to interactions among the renamings (eg, multiple
        # collisions among rn.new values).
        #
        # (2) We don't want the renamed path to inherit casing from
        # the existing rn.new, which occurs on case-preseving systems.
        #
        # (3) Python's path renaming functions fail on some
        # systems in the face of clobbering, and we don't want
        # to deal with those OS-dependent complications.
        #
        if pn.exists():
            if rn.clobber_self:
                # User requested case-change renaming. No problem.
                pass
            elif rn.clobber:
                # Make sure the clobber victim is (still) a supported path type.
                # Select the appropriate deletion operation.
                pt = determine_path_type(rn.new)
                if pt == PT.other:
                    raise MvsError(
                        MF.unsupported_clobber,
                        orig = rn.orig,
                        new = rn.new,
                    )
                elif pt == PT.file:
                    pn.unlink()
                else:
                    shutil.rmtree(rn.new)
            else:
                # An unrequested clobber.
                raise MvsError(
                    MF.unrequested_clobber,
                    orig = rn.orig,
                    new = rn.new,
                )

        # Rename.
        po.rename(rn.new)

    ####
    # Other info.
    ####

    @property
    def all_renamings(self):
        return self.filtered + self.excluded + self.skipped + self.active

    @property
    def tracking_rn(self):
        # The Renaming that was being renamed when rename_paths()
        # raised an exception.
        ti = self.tracking_index
        if ti in (self.TRACKING.not_started, self.TRACKING.done):
            return None
        else:
            return self.active[ti]

    @property
    def as_dict(self):
        # The plan as a dict.
        return dict(
            # Primary arguments from user.
            inputs = self.inputs,
            structure = self.structure,
            rename_code = get_source_code(self.rename_code),
            filter_code = get_source_code(self.filter_code),
            indent = self.indent,
            seq_start = self.seq_start,
            seq_step = self.seq_step,
            skip = self.skip,
            strict = asdict(self.strict),
            # Renaming instances.
            filtered = [asdict(rn) for rn in self.filtered],
            skipped = [asdict(rn) for rn in self.skipped],
            excluded = [asdict(rn) for rn in self.excluded],
            active = [asdict(rn) for rn in self.active],
            # Other.
            failure = asdict(self.failure) if self.failure else None,
            prefix_len = self.prefix_len,
            tracking_index = self.tracking_index,
        )

