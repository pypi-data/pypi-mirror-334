from textwrap import dedent

from short_con import cons

####
# General constants.
####

class CON:
    # Application configuration.
    app_name = 'mvs'
    encoding = 'utf-8'
    app_dir_env_var = f'{app_name.upper()}_APP_DIR'

    # Characters and simple tokens.
    newline = '\n'
    para_break = newline + newline
    space = ' '
    tab = '\t'
    colon = ':'
    pipe = '|'
    period = '.'
    comma_join = ', '
    underscore = '_'
    hyphen = '-'
    comma_space = ', '
    dash = hyphen + hyphen
    indent = '  '
    all = 'all'
    all_tup = (all,)
    yes = 'yes'
    empty_row_marker = '__EMPTY__'

    # User-supplied code.
    code_actions = cons('rename', 'filter')
    func_name_fmt = '_do_{}'
    user_code_fmt = dedent('''
        def {func_name}(o, n, po, pn, seq, r, plan):
        {indent}{user_code}
    ''').lstrip()

    # Command-line exit codes.
    exit_ok = 0
    exit_fail = 1

    # Logging.
    datetime_fmt = '%Y-%m-%d_%H-%M-%S'
    logfile_ext = 'json'
    prefs_file_name = 'config.json'

    # Executables.
    default_pager_cmd = 'more'
    default_editor_cmd = 'vim'

####
# Structures for input paths data.
####

STRUCTURES = cons(
    'flat',
    'paragraphs',
    'pairs',
    'rows',
    'origs',
)

