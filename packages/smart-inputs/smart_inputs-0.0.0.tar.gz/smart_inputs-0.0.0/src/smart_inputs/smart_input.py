import curses
from curses import ascii, window


class SmartInput:
    """
    Contains the logics relating to handle users inputs in the console.

    Args:
        prompt: the prompt to show in the console.
        default_string: the default answer for the prompt.
    """

    def __init__(self, prompt: str, default_string: str = '') -> None:
        self.__entered_value: str = None
        self.__prompt: str = prompt
        self.__default_string: str = default_string

        self.__cursor_x: int = len(self.__prompt) + \
            len(self.__default_string) + 1
        self.__cursor_y: int = 0

    def __initiate_screen(self, stdscr: window, message_content: str) -> None:
        """
        Initiate the screen by showing the prompt and the current answer as well as
        moving the cursor to the target position.

        Args:
            stdscr: the current screen.
            message_content: the current content on the screen.
        """
        stdscr.addstr(message_content)
        stdscr.move(self.__cursor_y, self.__cursor_x)

    def __run(self, stdscr: window) -> None:
        """
        Run the main logic to handle the user inputs.

        Args:
            stdscr: the current screen.
        """
        stdscr.clear()
        selected = self.__default_string

        while True:
            stdscr.clear()

            msg = f'{self.__prompt} {selected}'
            current_len = len(msg)
            self.__initiate_screen(stdscr, msg)

            try:
                key = stdscr.getch()
            except KeyboardInterrupt:
                print("Program terminated by the user.")
                exit(1)

            if key == ord('\b'):
                if selected and self.__cursor_x > len(self.__prompt) + 1:
                    selected = f'{selected[:self.__cursor_x-len(self.__prompt)-2]}{selected[self.__cursor_x-len(self.__prompt)-1:]}'
                    self.__cursor_x -= 1
            elif key == ord('\n'):
                self.__entered_value = selected
                break

            elif key == curses.KEY_LEFT:
                if self.__cursor_x > (len(self.__prompt) + 1):
                    self.__cursor_x -= 1
            elif key == curses.KEY_RIGHT:
                if self.__cursor_x < current_len:
                    self.__cursor_x += 1

            elif key in (curses.KEY_UP, curses.KEY_DOWN):
                pass

            elif ascii.isprint(key):
                selected = f'{selected[:self.__cursor_x-len(self.__prompt)-1]}{chr(key)}{selected[self.__cursor_x-len(self.__prompt)-1:]}'
                self.__cursor_x += 1

    def run(self) -> str:
        """
        Wrapper to run the main logic to handle the user inputs.
        """
        curses.wrapper(self.__run)
        return self.__entered_value


def smart_input(prompt: str, default: str = '') -> str:
    """
    Ask for an input from the user with the potential of showing a default value.

    Args:
        prompt: the prompt for the user.
        default_string: the default answer for the prompt.

    Returns:
        the user's entered value.
    """
    return SmartInput(prompt=prompt, default_string=default).run()
