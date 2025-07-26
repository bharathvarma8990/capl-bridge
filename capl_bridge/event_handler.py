class CANalyzerMeasurementEvents:
    def __init__(self, capl_manager):
        """
        Initializes the CANalyzerMeasurementEvents handler.

        Args:
            capl_manager (CAPLFunctionManager): Instance responsible for managing CAPL functions.
        """
        self.capl_manager = capl_manager

    def OnInit(self):
        """
        Callback triggered automatically when CANalyzer starts its measurement.

        Purpose:
            - Loads all available CAPL functions into memory using the CAPL manager.
            - Ensures all CAPL functions are registered and callable from Python before the test begins.
        """
        self.capl_manager.load_capl_functions()
