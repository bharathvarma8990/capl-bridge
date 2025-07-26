import re

class CAPLFunctionManager:
    """
    Manages CAPL functions extracted from a CAPL script file and interfaces with CANalyzer.
    """

    def __init__(self, capl_path, canalyzer, logger=None):
        """
        Initializes the CAPLFunctionManager.

        Args:
            capl_path (str): Path to the CAPL script file.
            canalyzer (COM object): CANalyzer application object.
            logger (logging.Logger, optional): Logger for error/warning output.
        """
        self.capl_path = capl_path
        self.canalyzer = canalyzer
        self.logger = logger
        self.capl_functions = {}
        self.capl_function_names = []

        if self.capl_path:
            self.capl_function_names = self.extract_capl_functions()
            self.canalyzer.CAPL.Compile()

    def extract_capl_functions(self):
        """
        Parses the CAPL script file and extracts function names using regex.

        Returns:
            List[str]: A list of CAPL function names defined in the script.

        Notes:
            Matches functions with return types: void, int, byte, word, dword, long, int64, qword.
        """
        pattern = r"^(void|int|byte|word|dword|long|int64|qword)\s+(\w+)\s*\("
        try:
            with open(self.capl_path, "r") as file:
                matches = re.findall(pattern, file.read(), re.MULTILINE)
                return [match[1] for match in matches]
        except FileNotFoundError:
            if self.logger:
                self.logger.error(f"CAPL script not found at path: {self.capl_path}")
            raise
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error reading CAPL script: {e}")
            raise

    def load_capl_functions(self):
        """
        Loads callable CAPL functions from CANalyzer and stores them in a dictionary.

        Populates:
            self.capl_functions (dict): {function_name: callable_object}
        """
        for name in self.capl_function_names:
            try:
                self.capl_functions[name] = self.canalyzer.CAPL.GetFunction(name)
            except Exception as e:
                if self.logger:
                    self.logger.warning(f"Failed to load CAPL function '{name}': {e}")

    def call_function(self, name, value=None, return_value: bool = False):
        """
        Calls a CAPL function by name with an optional argument and return value.

        Args:
            name (str): The CAPL function name to call.
            value (any, optional): The value to pass as an argument.
            return_value (bool): Whether to return the value from the CAPL function.

        Returns:
            Any: Return value from CAPL function if return_value is True.
            bool: True if function is successfully called and return_value is False.

        Raises:
            NameError: If the function is not found.
        """
        if name in self.capl_functions:
            func = self.capl_functions[name]
            try:
                if return_value:
                    return func.Call(value) if value is not None else func.Call()
                else:
                    func.Call(value) if value is not None else func.Call()
                    return True
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Error calling CAPL function '{name}': {e}")
                raise
        else:
            if self.logger:
                self.logger.error(f"CAPL function '{name}' not found.")
            raise NameError(f"CAPL function '{name}' not found.")
