import time
from win32com.client import DispatchEx
import win32com.client
from .capl_manager import CAPLFunctionManager
from .event_handler import CANalyzerMeasurementEvents


class CANalyzerSession:
    """
    A class to manage CANalyzer session, initialize measurement, and interface with CAPL functions.
    """

    def __init__(self, config_path, capl_path=None, logger=None):
        """
        Initializes the CANalyzer session with the given configuration and CAPL script.

        Args:
            config_path (str): Path to the CANalyzer configuration file (.cfg).
            capl_path (str, optional): Path to the CAPL script to load and parse functions.
            logger (logging.Logger, optional): Logger instance for logging messages.
        """
        self.logger = logger
        self.retries = 0
        self.max_retries = 5

        self.canalyzer = DispatchEx('CANalyzer.Application')

        # Retry logic to handle CANalyzer initialization race conditions
        while self.retries < self.max_retries:
            try:
                self.canalyzer.Open(config_path)
                break
            except Exception as e:
                self.retries += 1
                if self.logger:
                    self.logger.warning(
                        f"[Attempt {self.retries}] CANalyzer failed to open: {e}"
                    )
                time.sleep(1)
        else:
            raise RuntimeError("CANalyzer failed to open after multiple retries.")

        # Load CAPL function manager
        self.capl_manager = CAPLFunctionManager(capl_path, self.canalyzer, logger)

        # Register measurement event handler
        self.event_handler = win32com.client.WithEvents(
            self.canalyzer.Measurement,
            CANalyzerMeasurementEvents(self.capl_manager)
        )

        # Start measurement
        self.canalyzer.UI.Write.Output("Starting measurement...")
        self.canalyzer.Measurement.Start()
        while not self.canalyzer.Measurement.Running:
            time.sleep(2)
        self.canalyzer.UI.Write.Output("Measurement started.")

    def shutdown(self):
        """
        Shuts down the CANalyzer application.
        """
        self.canalyzer.Quit()

    def read_signal(self, channel, message, signal):
        """
        Reads the value of a CAN signal from the specified channel and message.

        Args:
            channel (str): CAN channel name or number.
            message (str): CAN message name.
            signal (str): Signal name inside the message.

        Returns:
            float: The current value of the signal.
        """
        return float(str(self.canalyzer.Bus.GetSignal(channel, message, signal)))

    def write_signal(self, message, signal, value):
        """
        Writes a value to a CAN signal by calling its corresponding CAPL function.

        Args:
            message (str): CAN message name.
            signal (str): Signal name within the message.
            value (any): Value to write.

        Returns:
            bool: True if the function was found and called, False otherwise.
        """
        func_name = f"{message}_{signal}"
        return self.capl_manager.call_function(func_name, value)

    def call_capl(self, name, value=None, return_value: bool = False):
        """
        Calls a CAPL function by name with optional value and return result.

        Args:
            name (str): Name of the CAPL function to call.
            value (any, optional): Value to pass as an argument.
            return_value (bool, optional): If True, returns CAPL function output.

        Returns:
            Any: CAPL function return value if return_value is True.
            bool: True if the function was successfully called.
        """
        return self.capl_manager.call_function(name, value, return_value)
