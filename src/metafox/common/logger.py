
class Logger:
    def __init__(self, name):
        self.name = name
        self._RED = "\033[91m"          # ANSI escape code for red color
        self._GREEN = "\033[92m"        # ANSI escape code for green color    
        self._YELLOW = "\033[93m"       # ANSI escape code for yellow color
        self._BLUE = "\033[94m"         # ANSI escape code for blue color
        self._RESET = "\033[0m"         # ANSI escape code to reset colors

    def debug(self, msg):
            """
            Prints a debug message with the specified message.

            Args:
                msg (str): The debug message to be printed.
            """
            print(f"{self._BLUE}[DEBUG] {self.name}: {msg}{self._RESET}")

    def info(self, msg):
            """
            Log an informational message.

            Args:
                msg (str): The message to be logged.
            """
            print(f"{self._GREEN}[INFO] {self.name}: {msg}{self._RESET}")
        
    def warning(self, msg):
            """
            Prints a warning message with the name of the logger.

            Args:
                msg (str): The warning message to be printed.
            """
            print(f"{self._YELLOW}[WARNING] {self.name}: {msg}{self._RESET}")
    
    def error(self, msg):
            """
            Log an error message.

            Args:
                msg (str): The error message to be logged.
            """
            print(f"{self._RED}[ERROR] {self.name}: {msg}{self._RESET}")
        
    def critical(self, msg):
            """
            Log a critical message.

            Args:
                msg (str): The message to be logged.

            Returns:
                None
            """
            print(f"{self._RED}[CRITICAL] {self.name}: {msg}{self._RESET}")
