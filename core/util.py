import os
import readline

def splitpath(path):
    return os.path.normpath(path).split(os.sep)

def init_readline(env_state):
    readline.parse_and_bind('tab:complete')
    def command_completer(text, state):
        options = [i for i in env_state.commands if i.startswith(text)]
        if state < len(options):
            return options[state]
        else:
            options = [i for i in env_state.local_autocomplete if i.startswith(text)]
            if state < len(options):
                return options[state]
            else:
                return None

    readline.set_completer(command_completer)

class BrightColor:
    BLACK = '\033[90m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

class Color:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'
