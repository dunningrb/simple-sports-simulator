import subprocess
import sys
import termios
import tty


def any_key_continue():
    print(f'Hit any key to continue except Q/q to quit.')

    def _get_char():
        return sys.stdin.read(1)

    while True:
        option = _get_char()

        if option in ['Q', 'q']:
            sys.exit()
        else:
            return


def clear_screen():
    subprocess.run(['clear'])


def get_char():
    """Get character input from keyboard.
    """

    def _get_char():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    return _get_char()


def get_user_option(*, prompt, allowed_options, exit_options):
    while True:
        print(prompt)
        option = get_char()

        if option in exit_options:
            sys.exit()
        elif option not in allowed_options:
            print(f'\n*** Invalid entry. Please try again. ***\n')
            continue
        else:
            clear_screen()
            return option
