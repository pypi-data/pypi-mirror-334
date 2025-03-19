import json
import os
import platform
import pytest
import sys
import traceback

from collections import namedtuple
from io import StringIO
from pathlib import Path
from string import ascii_lowercase
from types import SimpleNamespace

from mvs.cli import main, CliRenamer, CLI
from mvs.constants import CON
from mvs.plan import RenamingPlan
from mvs.utils import write_to_clipboard
from mvs.version import __version__

from mvs.messages import (
    MSG_FORMATS as MF,
    LISTING_CATEGORIES as LC,
    PARENT_LISTING_CATEGORIES as PLC,
)

from mvs.problems import (
    FAILURE_FORMATS as FF,
    FAILURE_NAMES as FN,
    FAILURE_VARIETIES as FV,
    PROBLEM_FORMATS as PF,
    PROBLEM_NAMES as PN,
)


####
# Helper class to test CliRenamer instances.
####

BYPASS = object()
LOGS_OK = 'LOGS_OK'
PLAN_LOG_OK = 'PLAN_LOG_OK'

class CliRenamerSIO(CliRenamer):
    # A thin wrapper around a CliRenamer:
    #
    # - Adds args to disable pagination by default.
    # - Includes --yes among args by default.
    # - Sets I/O handles to be StringIO instances, so we can capture outputs.
    # - Adds a convenience to feed stdin (replies).
    # - Adds various properties/etc to simplify assertion making.

    def __init__(self, *args, pager = None, yes = True, replies = ''):
        pager = (
            ('--pager', '') if pager is None else
            () if pager is BYPASS else
            ('--pager', pager)
        )
        yes = ('--yes',) if yes else ()
        super().__init__(
            args + pager + yes,
            stdout = StringIO(),
            stderr = StringIO(),
            stdin = StringIO(replies),
            logfh = StringIO(),
        )

    @property
    def success(self):
        return self.exit_code == CON.exit_ok

    @property
    def failure(self):
        return self.exit_code == CON.exit_fail

    @property
    def out(self):
        return self.stdout.getvalue()

    @property
    def err(self):
        return self.stderr.getvalue()

    @property
    def log(self):
        return self.logfh.getvalue()

    @property
    def log_plan(self):
        return parse_log(self.log, self.LOG_TYPE.plan)

    @property
    def log_tracking(self):
        return parse_log(self.log, self.LOG_TYPE.tracking)

    @property
    def log_plan_dict(self):
        return json.loads(self.log_plan)

    @property
    def log_tracking_dict(self):
        return json.loads(self.log_tracking)

    @property
    def logs_valid_json(self):
        plan = self.log_plan
        tracking = self.log_tracking
        try:
            json.loads(plan)
            json.loads(tracking)
            return LOGS_OK
        except Exception as e:
            return dict(
                plan = plan,
                tracking = tracking,
                trackback = traceback.format_exc(),
            )

####
# A mega-helper to perform common checks.
# Used by most tests.
####

def run_checks(
               # Fixtures.
               tr,
               creators,
               # WorkArea (and arbitrary positionals for CliRenamer).
               origs,
               news,
               *cli_xs,
               extras = None,
               expecteds = None,
               rootless = False,
               # UserPrefs.
               prefs = None,
               blob = None,
               # Outputs.
               inventory = None,
               out = None,
               out_in = None,
               fail_params = None,
               err = None,
               err_starts = None,
               err_in = None,
               log = None,
               # Functions allowing user to do things midway through.
               other_prep = None,
               early_checks = None,
               # Assertion making.
               check_wa = True,
               check_outs = True,
               done = True,
               failure = False,
               no_change = False,
               # CliRenamer.
               cli_cls = CliRenamerSIO,
               include_origs = True,
               include_news = True,
               prepare_only = False,
               prepare_before = 0,
               diagnostics = False,
               setup_only = False,
               no_checks = False,
               rename_via_do = False,
               skip_rename = False,
               **cli_kws):

    # Get the fixtures.
    create_wa, create_outs, create_prefs = creators

    # Set up preferences.
    if blob is not None:
        create_prefs(blob = blob)
    elif prefs is not None:
        create_prefs(**prefs)

    # Set up WorkArea.
    wa = create_wa(
        origs,
        news,
        extras = extras,
        expecteds = expecteds,
        rootless = rootless
    )

    # Set up Outputs.
    outs = create_outs(
        wa.origs,
        wa.news,
        inventory = inventory,
        fail_params = fail_params,
    )

    # Set up CliRenamer
    args = (
        (wa.origs if include_origs else ()) +
        (wa.news if include_news else ()) +
        cli_xs
    )
    cli = cli_cls(*args, **cli_kws)

    # Return early if user does not want to do anything
    # other than create WorkArea, Outputs, and CliRenamer.
    if setup_only:
        return (wa, outs, cli)

    # Let caller do other set up stuff before renaming.
    if other_prep:
        other_prep(wa, outs, cli)

    # Run preparations.
    if prepare_only:
        no_change = True
    n_preps = int(
        prepare_before or
        prepare_only or
        rename_via_do or
        diagnostics
    )
    for _ in range(n_preps):
        cli.do_prepare()

    # Print diagnostic info.
    if diagnostics:
        tr.dumpj(wa.as_dict, 'WorkArea-before')
        tr.dumpj(cli.plan.as_dict, 'RenamingPlan-before')

    # Run the renaming.
    if not prepare_only:
        if rename_via_do:
            cli.do_rename()
        elif rootless:
            with wa.cd():
                cli.run()
        elif not skip_rename:
            cli.run()

    # Print diagnostic info.
    if diagnostics:
        tr.dumpj(wa.as_dict, 'WorkArea-after')
        tr.dumpj(cli.plan.as_dict, 'RenamingPlan-after')

    # Return early if user does not want to check anything.
    if no_checks:
        return (wa, outs, cli)

    # Let caller make early assertions.
    if early_checks:
        early_checks(wa, outs, cli)

    # Check work area.
    if check_wa:
        wa.check(no_change = no_change)

    # Check CliRenamer outputs.
    if check_outs:
        # Standard output.
        if out_in:
            for exp in to_tup(out_in):
                assert exp in cli.out
        elif callable(out):
            assert cli.out == out(wa, outs, cli)
        elif out is None:
            assert cli.out == outs.renaming_listing(cli.plan)
        elif out is not BYPASS:
            assert cli.out == out

        # Error output.
        if err_starts:
            assert cli.err.startswith(err_starts)
        if err_in:
            for exp in to_tup(err_in):
                assert exp in cli.err
        if err is not None:
            assert cli.err == err

        # Log output.
        if log is LOGS_OK:
            assert cli.logs_valid_json is LOGS_OK
        elif log is PLAN_LOG_OK:
            assert isinstance(cli.log_plan_dict, dict)
        elif log is BYPASS:
            pass
        elif log is None:
            if failure:
                assert cli.log == ''
            else:
                assert cli.logs_valid_json is LOGS_OK
        elif log:
            assert cli.log == log

    # Check CliRenamer success/failure status.
    if failure:
        assert cli.failure
    elif done:
        assert cli.success
    else:
        assert not cli.done

    # Let the caller make other custom assertions.
    return (wa, outs, cli)

####
# Helper functions.
####

def parse_log(text, log_type):
    # CliRenamerSIO collects logging output from CliRenamer
    # in a single StringIO, which means that the plan-log and
    # the tracking-log are combined. This function takes a
    # log_type and returns the desired portion of the log output.

    # Find the index of the divider between the two logging calls.
    # If we don't find it, all content will go to the plan-log.
    div = '\n}{\n'
    try:
        i = text.index(div) + 2
    except ValueError:
        i = len(text)

    # Partition the text into the two logs and return the requested one.
    logs = {
        CliRenamer.LOG_TYPE.plan:     text[0 : i],
        CliRenamer.LOG_TYPE.tracking: text[i : None],
    }
    return logs[log_type]

def to_tup(x):
    # Takes a value. Returns it in a tuple if its not already one.
    if isinstance(x, tuple):
        return x
    else:
        return (x,)

def pre_fmt(fmt):
    # Takes a format string.
    # Returns the portion before the first brace.
    return fmt.split('{')[0]

def can_use_clipboard():
    # I could not get pyperclip working on ubuntu in Github Actions,
    # I'm using this to bypass clipboard checks.
    return platform.system() != 'Linux'

####
# Command-line arguments and options.
####

def test_version_and_help(tr, creators):
    # Exercise the command-line options that report
    # information about the app and exit immediately.

    # Paths and args.
    origs = ('a', 'b')
    news = ()
    run_args = (tr, creators, origs, news)
    kws = dict(
        include_origs = False,
        include_news = False,
        no_change = True,
        log = '',
    )

    # Version.
    wa, outs, cli = run_checks(
        *run_args,
        '--version',
        out = MF.cli_version + CON.newline,
        **kws,
    )

    # Details: general check for same roster of words.
    wa, outs, cli = run_checks(
        *run_args,
        '--details', 'all',
        out = BYPASS,
        **kws,
    )
    assert cli.out.split() == ' '.join(
        section
        for _, section in CLI.details.items()
    ).split()

    # Help.
    wa, outs, cli = run_checks(
        *run_args,
        '--help',
        out = BYPASS,
        **kws,
    )
    got = cli.out
    N = 40
    assert got.startswith(f'Usage: {CON.app_name}')
    assert CLI.description[0:N] in got
    for oc in CLI.opt_configs.values():
        assert oc.params['help'][0:N] in got
        if oc.name != 'paths':
            assert f'\n  --{oc.name}' in got

def test_indent_and_posint(tr, creators):
    # Paths and args.
    origs = ('a', 'b', 'c')
    news = ('aa', 'bb', 'cc')
    run_args = (tr, creators, origs, news)
    valid_indents = ('2', '4', '8')
    invalid_indents = ('-4', 'xx', '0', '1.2')

    # Valid indent values.
    for ind in valid_indents:
        wa, outs, cli = run_checks(
            *run_args,
            '--rename', 'return o + o',
            '--indent', ind,
            '--origs',
            include_news = False,
            rootless = True,
        )

    # Invalid indent values.
    for ind in invalid_indents:
        wa, outs, cli = run_checks(
            *run_args,
            '--rename', 'return o + o',
            '--indent', ind,
            '--origs',
            include_news = False,
            rootless = True,
            failure = True,
            no_change = True,
            err_in = '--indent: invalid positive_int value',
            err_starts = f'Usage: {CON.app_name}',
            out = '',
        )

####
# Basic renaming usage.
####

def test_basic_use_cases(tr, creators):
    # Paths and args.
    origs = ('a', 'b', 'c')
    news = ('aa', 'bb', 'cc')
    run_args = (tr, creators, origs, news)

    # Basic use cases:
    # - Flat structure as the default.
    # - Flat passed explicitly.
    # - Renaming via code and just original paths.
    wa, outs, cli = run_checks(*run_args)
    wa, outs, cli = run_checks(*run_args, '--flat')
    wa, outs, cli = run_checks(
        *run_args,
        '--rename',
        'return po.with_name(po.name + po.name)',
        '--origs',
        include_news = False,
    )

####
# Input paths and sources.
####

def test_no_input_paths(tr, creators):
    # Paths and args.
    origs = ('a', 'b', 'c')
    news = ('aa', 'bb', 'cc')
    empty_paths = ('', '   ', ' ') * 2
    run_args = (tr, creators, origs, news)

    # Initial scenario: it works.
    wa, outs, cli = run_checks(*run_args)

    # But it fails if we omit the input paths.
    wa, outs, cli = run_checks(
        *run_args,
        include_origs = False,
        include_news = False,
        failure = True,
        no_change = True,
        err_starts = MF.opts_require_one,
        err_in = CLI.sources.keys(),
        out = '',
    )

    # It also fails if the input paths are empty.
    wa, outs, cli = run_checks(
        *run_args,
        *empty_paths,
        include_origs = False,
        include_news = False,
        failure = True,
        no_change = True,
        err_in = MF.no_action,
        out_in = FF[FN.parsing, FV.no_paths],
        log = PLAN_LOG_OK,
    )

def test_odd_number_inputs(tr, creators):
    # An odd number of inputs will fail.
    origs = ('z1', 'z2', 'z3')
    news = ()
    wa, outs, cli = run_checks(
        tr,
        creators,
        origs,
        news,
        failure = True,
        no_change = True,
        err_in = MF.no_action,
        out_in = FF[FN.parsing, FV.imbalance],
        log = PLAN_LOG_OK,
    )

def test_sources(tr, creators):
    # Paths and args.
    origs = ('z1', 'z2', 'z3')
    news = ('A1', 'A2', 'A3')
    extras = ('input_paths.txt',)
    run_args = (tr, creators, origs, news)

    # Create a WorkArea to get some paths in it.
    # Use them to create two constants.
    WA = creators[0](origs, news, extras = extras)
    PATHS_TEXT = CON.newline.join(WA.origs + WA.news)
    INPUTS_PATH = WA.extras[0]

    # Helpers to write PATHS_TEXT to either a file or the clipboard.
    def write_paths_to_file(wa, outs, cli):
        with open(INPUTS_PATH, 'w') as fh:
            fh.write(PATHS_TEXT)

    def write_paths_to_clipboard(wa, outs, cli):
        write_to_clipboard(PATHS_TEXT)

    # Base scenario: paths via args.
    wa, outs, cli = run_checks(
        *run_args,
        extras = extras,
    )

    # Paths via stdin.
    wa, outs, cli = run_checks(
        *run_args,
        '--stdin',
        replies = PATHS_TEXT,
        include_origs = False,
        include_news = False,
    )

    # Paths via a file.
    wa, outs, cli = run_checks(
        *run_args,
        '--file',
        INPUTS_PATH,
        extras = extras,
        include_origs = False,
        include_news = False,
        other_prep = write_paths_to_file,
    )

    # Paths via clipboard.
    if can_use_clipboard():
        wa, outs, cli = run_checks(
            *run_args,
            '--clipboard',
            include_origs = False,
            include_news = False,
            other_prep = write_paths_to_clipboard,
        )

    # Too many sources: renaming will be rejected.
    wa, outs, cli = run_checks(
        *run_args,
        '--clipboard',
        '--stdin',
        include_origs = False,
        include_news = False,
        failure = True,
        no_change = True,
        err_starts = MF.opts_mutex,
        err_in = ('--clipboard', '--stdin'),
        out = '',
    )

def test_origs_rename(tr, creators):
    # Paths and args.
    origs = ('z1', 'z2', 'z3')
    news = tuple(o + '.new' for o in origs)
    run_args = (tr, creators, origs, news)

    # Working scenario with --origs and --rename.
    wa, outs, cli = run_checks(
        *run_args,
        '--rename', 'return o + ".new"',
        '--origs',
        include_news = False,
    )

    # Should fail without --rename.
    wa, outs, cli = run_checks(
        *run_args,
        '--origs',
        include_news = False,
        failure = True,
        no_change = True,
        err_starts = MF.opts_origs_rename,
        out = '',
    )

####
# The --edit and --editor options.
####

def test_edit(tr, creators):
    # Paths and args.
    origs = ('a', 'b', 'c')
    news = tuple(o + '.new' for o in origs)
    run_args = (tr, creators, origs, news)

    # Initial scenario: it works.
    wa, outs, cli = run_checks(
        *run_args,
        '--edit',
        '--editor', tr.TEST_EDITOR,
        include_news = False,
    )

    # Renaming attempt fails if we try to edit without an editor.
    wa, outs, cli = run_checks(
        *run_args,
        '--edit',
        '--editor', '',
        include_news = False,
        failure = True,
        no_change = True,
        err = MF.no_editor + '\n',
        out = '',
    )

    # Renaming attempt fails if the editor exits unsuccessfully.
    wa, outs, cli = run_checks(
        *run_args,
        '--edit',
        '--editor', tr.TEST_FAILER,
        include_news = False,
        failure = True,
        no_change = True,
        err_in = (
            pre_fmt(MF.editor_cmd_nonzero),
            pre_fmt(MF.edit_failed_unexpected),
        ),
        out = '',
    )

####
# Preferences.
####

def test_preferences_file(tr, creators):
    # Paths and args.
    origs = ('a', 'b', 'c')
    news = ('aa', 'bb', 'cc')
    run_args = (tr, creators, origs, news)

    # Scenario: an empty but valid preferences file: renaming works fine.
    wa, outs, cli = run_checks(
        *run_args,
        prefs = {},
    )

    # Scenario: an invalid JSON file.
    wa, outs, cli = run_checks(
        *run_args,
        blob = 'INVALID_JSON',
        failure = True,
        no_change = True,
        err_starts = pre_fmt(MF.prefs_reading_failed),
        err_in = 'JSONDecodeError',
        out = '',
    )

    # Scenario: a valid JSON file; confirm that we affect cli.opts.
    default = {}
    custom = dict(indent = 2, seq = 100, step = 10)
    exp_default = dict(indent = 4, seq = 1, step = 1)
    for prefs in (default, custom):
        wa, outs, cli = run_checks(
            *run_args,
            prefs = prefs,
            prepare_only = True,
            check_outs = False,
            done = False,
        )
        exp = prefs or exp_default
        got = {
            k : getattr(cli.opts, k)
            for k in exp
        }
        assert got == exp

    # Scenario: disable testing ENV variable and exercise the code
    # path based on the user's home directory.
    nm = CON.app_dir_env_var
    prev = os.environ[nm]
    try:
        del os.environ[nm]
        wa, outs, cli = run_checks(*run_args)
    finally:
        os.environ[nm] = prev

def test_preferences_validation(tr, creators):
    # Paths and args.
    origs = ('a', 'b', 'c')
    news = ('aa', 'bb', 'cc')
    run_args = (tr, creators, origs, news)

    # Scenario: invalid preferences keys.
    prefs = dict(indent = 2, foo = 999, bar = 'fubb')
    wa, outs, cli = run_checks(
        *run_args,
        prefs = prefs,
        prepare_only = True,
        failure = True,
        err_starts = pre_fmt(MF.invalid_pref_keys),
        err_in = ('foo', 'bar'),
        out = '',
    )

    # Scenario: invalid preferences value.
    # Currently, no command line options take floats, so
    # we will use that for the bad value.
    BAD_VAL = 3.14
    for oc in CLI.opt_configs.values():
        prefs = {oc.name: BAD_VAL}
        exp = MF.invalid_pref_val.format(
            oc.name,
            oc.check_value(BAD_VAL),
            BAD_VAL,
        )
        wa, outs, cli = run_checks(
            *run_args,
            prefs = prefs,
            prepare_only = True,
            failure = True,
            err = exp + '\n',
            out = '',
        )

def test_preferences_merging(tr, create_prefs):
    # Paths and args.
    origs = ('a', 'b')
    news = ('aa', 'bb')

    # Some user preferences that we will set.
    PREFS = dict(
        paragraphs = True,
        indent = 8,
        seq = 1000,
        step = 10,
        filter = 'return True',
        edit = True,
        editor = 'sed',
        yes = True,
        nolog = True,
        limit = 20,
        skip = [PN.exists],
    )

    # Helper to get cli.opts and confirm that CliRenamer did
    # not gripe about invalid arguments.
    def get_opts(*args):
        cli = CliRenamer(origs + news + args)
        opts = cli.parse_command_line_args()
        assert opts is not None
        assert not cli.done
        return vars(opts)

    # Helper to check resulting opts against expecations.
    def check_opts(got, exp):
        assert sorted(got) == sorted(DEFAULTS)
        for k, def_val in DEFAULTS.items():
            assert (k, got[k]) == (k, exp.get(k, def_val))

    # Helper to convert OVERRIDES to command-line-style args.
    def overrides_as_args():
        for k, v in OVERRIDES.items():
            yield f'--{k}'
            if isinstance(v, list):
                yield from map(str, v)
            else:
                yield str(v)

    # Setup: get the defaults for cli.opts.
    DEFAULTS = get_opts()

    # Scenario: an empty preferences file won't change the defaults.
    create_prefs()
    opts = get_opts()
    assert opts == DEFAULTS

    # Scenario: set some user preferences.
    # Those settings should be reflected in opts.
    create_prefs(**PREFS)
    opts = get_opts()
    check_opts(opts, PREFS)

    # Scenario: set the same preferences, but also supply some arguments on the
    # command-line. The latter should override the prefs. The overrides also
    # exercise the --disable option, which is used to unset a flag option that
    # was set true in preferences.
    OVERRIDES = dict(
        indent = 2,
        seq = 50,
        step = 5,
        filter = 'return p.suffix == ".txt"',
        editor = 'awk',
        limit = 100,
        disable = ['paragraphs', 'edit', 'yes', 'nolog'],
        skip = [PN.collides],
    )
    create_prefs(**PREFS)
    opts = get_opts(*overrides_as_args())
    check_opts(opts, OVERRIDES)

####
# Dryrun and no-confirmation.
####

def test_dryrun(tr, creators):
    # Paths and args.
    origs = ('a', 'b', 'c')
    news = ('aa', 'bb', 'cc')
    run_args = (tr, creators, origs, news)

    # Callable to check cli.out.
    exp_out = lambda wa, outs, cli: outs.no_action_output(cli.plan)

    # In dryrun mode, we get the usual listing,
    # but no renaming or logging occurs.
    wa, outs, cli = run_checks(
        *run_args,
        '--rename',
        'return o + o',
        '--dryrun',
        '--origs',
        include_news = False,
        rootless = True,
        no_change = True,
        out = exp_out,
        log = '',
    )

def test_no_confirmation(tr, creators):
    # Paths and args.
    origs = ('a', 'b', 'c')
    news = ('aa', 'bb', 'cc')
    run_args = (tr, creators, origs, news)

    # Callable to check cli.out.
    exp_out = lambda wa, outs, cli: outs.no_confirm_output(cli.plan)

    # If user does not confirm, we get the usual listing,
    # but no renaming or logging occurs.
    wa, outs, cli = run_checks(
        *run_args,
        '--rename',
        'return o + o',
        '--origs',
        include_news = False,
        rootless = True,
        no_change = True,
        out = exp_out,
        log = '',
        yes = False,
    )

####
# User-supplied code.
####

def test_rename_paths_raises(tr, creators):
    # Paths, etc.
    origs = ('z1', 'z2', 'z3')
    news = ('ZZ1', 'ZZ2', 'ZZ3')
    expecteds = news[:1] + origs[1:]
    NSTART = RenamingPlan.TRACKING.not_started
    run_args = (tr, creators, origs, news)

    # Helper to format expected error text for subsequent checks.
    def exp_err_text(tracking_index):
        msg = MF.renaming_raised.format(tracking_index)
        return '\n' + msg.strip().split(CON.colon)[0]

    # Helpers to call do_prepare() and do_rename() in various ways.
    def other_prep1(wa, outs, cli):
        cli.do_prepare()
        cli.do_prepare()
        assert cli.plan.tracking_rn is None
        cli.do_rename()
        assert cli.plan.tracking_rn is None
        cli.do_rename()
        assert cli.plan.tracking_rn is None

    def other_prep2(wa, outs, cli):
        cli.do_prepare()
        cli.plan.has_renamed = True
        cli.do_rename()

    def other_prep3(wa, outs, cli):
        cli.do_prepare()
        assert cli.plan.tracking_rn is None
        assert cli.plan.tracking_index == NSTART
        cli.plan.call_at = (N, raiser)
        cli.do_rename()

    def raiser(plan):
        raise ZeroDivisionError('SIMULATED_ERROR')

    # Basic scenario: it works.
    wa, outs, cli = run_checks(*run_args)

    # Same thing, but using do_prepare() and do_rename().
    wa, outs, cli = run_checks(
        *run_args,
        rename_via_do = True,
    )

    # Same thing, but we can call those methods multiple times.
    wa, outs, cli = run_checks(
        *run_args,
        skip_rename = True,
        other_prep = other_prep1,
    )

    # Same scenario, but we will set plan.has_renamed to trigger
    # an exception when plan.rename_paths() is called.
    wa, outs, cli = run_checks(
        *run_args,
        skip_rename = True,
        other_prep = other_prep2,
        failure = True,
        no_change = True,
        err_starts = exp_err_text(NSTART),
        err_in = 'raise MvsError(MF.rename_done_already)',
        out = BYPASS,
        log = LOGS_OK,
    )
    assert cli.plan.tracking_index == NSTART
    exp = outs.renaming_listing(cli.plan, final_msg = False).rstrip()
    assert cli.out.rstrip() == exp

    # Same scenario, but this time we will trigger the exception via
    # the call_at attribute, so we can check the tracking_index in
    # the tracking log and in the command-line error message.
    N = 1
    wa, outs, cli = run_checks(
        *run_args,
        expecteds = expecteds,
        skip_rename = True,
        other_prep = other_prep3,
        failure = True,
        err_starts = exp_err_text(N),
        err_in = 'ZeroDivisionError: SIMULATED_ERROR',
        out = BYPASS,
        log = LOGS_OK,
    )
    assert cli.plan.tracking_rn.orig == wa.origs[N]
    assert cli.plan.tracking_index == N
    assert cli.log_tracking_dict == dict(tracking_index = N)
    exp = outs.renaming_listing(cli.plan, final_msg = False).rstrip()
    assert cli.out.rstrip() == exp

def test_filter_all(tr, creators):
    # Paths and args.
    origs = ('a', 'b', 'c')
    news = ('aa', 'bb', 'cc')
    inventory = (LC.filtered,) * len(origs)
    run_args = (tr, creators, origs, news)

    # Initial scenario: it works.
    wa, outs, cli = run_checks(*run_args)

    # Scenario: renaming attempt fails if the user code filters everything.
    wa, outs, cli = run_checks(
        *run_args,
        '--filter',
        'return False',
        failure = True,
        no_change = True,
        err_in = MF.no_action,
        log = PLAN_LOG_OK,
        inventory = inventory,
        fail_params = (FN.all_filtered, None),
    )

####
# Textual outputs.
####

def test_log(tr, creators):
    # Paths and args.
    origs = ('a', 'b', 'c')
    news = ('aa', 'bb', 'cc')
    run_args = (tr, creators, origs, news)

    # A basic renaming scenario.
    # We can load its logging data and check that both dicts
    # contain expected some of the expected keys and/or vals.
    wa, outs, cli = run_checks(*run_args)
    assert cli.log_tracking_dict == dict(tracking_index = cli.plan.TRACKING.done)
    d = cli.log_plan_dict
    assert d['version'] == __version__
    exp_keys = (
        'current_directory',
        'opts',
        'inputs',
        'active',
        'filtered',
        'skipped',
        'excluded',
    )
    for k in exp_keys:
        assert k in d

def test_log_write_fail(tr, creators):
    # Exercise code path where log writing fails.
    # It is sufficient to do this just on MacOS.
    if platform.system() != 'Darwin':
        return

    # Paths and args.
    origs = ('a', 'b', 'c')
    news = ('a.new', 'b.new', 'c.new')
    run_args = (tr, creators, origs, news)

    # Modify the mvs application directory to a unwritable path,
    # which will cause log writing to raise.
    k = CON.app_dir_env_var
    prev = os.environ[k]
    try:
        os.environ[k] = '/'
        wa, outs, cli = run_checks(
            *run_args,
            failure = True,
            no_change = True,
            err_starts = pre_fmt(MF.log_writing_failed),
            out = '',
            log = '',
        )
    finally:
        os.environ[k] = prev

def test_pagination(tr, creators):
    # Paths and args.
    origs = tuple(ascii_lowercase)
    news = tuple(o + o for o in origs)
    run_args = (tr, creators, origs, news)

    # A scenario to exercise the paginate() function.
    wa, outs, cli = run_checks(
        *run_args,
        pager = tr.TEST_PAGER,
        out_in = MF.paths_renamed,
    )

####
# Exercising main().
####

def test_main(tr, create_wa, create_outs):
    # Paths.
    origs = ('xx', 'yy')
    news = ('xx.new', 'yy.new')

    # Helper to check that logging output is valid JSON.
    def check_log(cli, log_name):
        log_type = getattr(CliRenamer.LOG_TYPE, log_name)
        text = parse_log(cli.logfh, log_type)
        d = json.loads(text)
        assert isinstance(d, dict)

    # File handles to pass into main().
    fhs = dict(
        stdout = StringIO(),
        stderr = StringIO(),
        stdin = StringIO(),
        logfh = StringIO(),
    )

    # Create work area.
    wa = create_wa(origs, news)
    outs = create_outs(wa.origs, wa.news)
    inputs = wa.origs + wa.news

    # Separately, create a RenamingPlan using the same inputs.
    # We do this because the main() below will not give us access to
    # the plan, which is needed when checking STDOUT.
    plan = RenamingPlan(inputs = wa.origs + wa.news)
    plan.prepare()

    # Call main(). It should exit successfully.
    args = inputs + ('--yes', '--pager', '')
    with pytest.raises(SystemExit) as einfo:
        main(args, **fhs)
    einfo.value.code == CON.exit_ok

    # Confirm that paths were renamed as expected.
    wa.check()

    # Check textual outputs.
    cli = SimpleNamespace(**{
        k : fh.getvalue()
        for k, fh in fhs.items()
    })
    assert cli.stdout == outs.renaming_listing(plan)
    assert cli.stderr == ''
    assert cli.stdin == ''
    check_log(cli, 'plan')
    check_log(cli, 'tracking')

####
# Problem control.
####

def test_listings(tr, creators):
    # Define some paths data to set up a situation where the
    # renaming listing will contain every top-level category.
    Pd = namedtuple('PathsData', 'inv orig new')
    pds = (
        # Filtered.
        Pd('filtered', 'F1', 'F1.new'),
        Pd('filtered', 'F2', 'F2.new'),
        # Excluded.
        Pd('duplicate', 'SAME_A', 'same1.new'),
        Pd('duplicate', 'SAME_A', 'same2.new'),
        Pd('duplicate', 'SAME_B', 'same3.new'),
        Pd('duplicate', 'SAME_B', 'same4.new'),
        # Skipped.
        Pd('exists-full', 's1', 's1.new'),
        Pd('exists-full', 's2', 's2.new'),
        # Parent.
        Pd('active-parent', 'p1', 'parent_dir/p1.new'),
        Pd('active-parent', 'p2', 'parent_dir/p2.new'),
        Pd('active-parent', 'p3', 'parent_dir/p3.new'),
        Pd('active-parent', 'p4', 'parent_dir/p4.new'),
        # Exists.
        Pd('active-exists', 'e1', 'e1.new'),
        Pd('active-exists', 'e2', 'e2.new'),
        Pd('active-exists', 'e3', 'e3.new'),
        # Collides.
        Pd('active-collides', 'c1', 'c12.new'),
        Pd('active-collides', 'c2', 'c12.new'),
        Pd('active-collides', 'c3', 'c34.new'),
        Pd('active-collides', 'c4', 'c34.new'),
        # OK.
        Pd('ok', 'a', 'a.new'),
        Pd('ok', 'b', 'b.new'),
    )

    # Use that data to set up the paths and args.
    origs = tuple(t.orig for t in pds)
    news = tuple(t.new for t in pds)
    inventory = tuple(t.inv for t in pds)
    extras = (
        # The paths needed for the exists situations implied above.
        tuple(t.new for t in pds if t.inv == 'active-exists') +
        ('s1.new/', 's1.new/bar', 's2.new/', 's2.new/bar')
    )
    expecteds = (
        # The extras, plus the needed parent directory, plus
        # either the orig path or new path from pds.
        extras +
        ('parent_dir',) +
        tuple(
            t.new if t.inv == LC.ok or t.inv.startswith(PLC.active) else t.orig
            for t in pds
        )
    )
    run_args = (tr, creators, origs, news)

    # Run the scenario. This will end up using Outputs.renaming_listing() to
    # confirm expectations for both the inventory of Renaming instances in the
    # RenamingPlan and for the text output sent to cli.out.
    wa, outs, cli = run_checks(
        *run_args,
        '--filter', 'return "F" not in o',
        '--skip', 'exists-full',
        extras = extras,
        expecteds = expecteds,
        inventory = inventory,
    )

####
# Miscellaneous.
####

def test_wrapup_with_tb(tr, create_wa):
    # Excercises all calls of wrapup_with_tb() and checks for expected
    # attribute changes. Most of those code branches (1) are a hassle to reach
    # during testing, (2) are unlikely to occur in real usage, (3) do nothing
    # interesting other than call the method tested here, and thus (4) are
    # pragma-ignored by test-coverage. Here we simple exercise the machinery to
    # insure against MF attribute names or format strings becoming outdated.

    # Paths.
    origs = ('z1', 'z2', 'z3')
    news = ('A1', 'A2', 'A3')

    # Format strings and dummy params they can use.
    fmts = (
        ('', MF.plan_creation_failed),
        (99, MF.renaming_raised),
        ('PATH', MF.prefs_reading_failed),
        ('', MF.path_collection_failed),
        ('', MF.edit_failed_unexpected),
        ('', MF.log_writing_failed),
    )

    # Check all the format strings.
    for param, fmt in fmts:
        # Create WorkArea and CliRenamer.
        # Initially, the latter is not done.
        wa = create_wa(origs, news)
        cli = CliRenamerSIO(*wa.origs, *wa.news)
        assert cli.exit_code is None
        assert cli.done is False

        # Call wrapup_with_tb().
        msg = fmt.format(param) if param else fmt
        cli.wrapup_with_tb(msg)

        # Now the CliRenamer is done and its error
        # output is what we expect.
        assert cli.exit_code == CON.exit_fail
        assert cli.done is True
        assert cli.out == ''
        assert cli.log == ''
        assert pre_fmt(fmt) in cli.err
        wa.check(no_change = True)

