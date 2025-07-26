from capl_bridge.canalyzer_session import CANalyzerSession

canalyzer_path = "C:\\Path\\To\\Your\\config.cfg"
capl_path = "C:\\Path\\To\\Your\\script.capl"

bridge = CANalyzerSession(canalyzer_path, capl_path)

bridge.call_capl("InitTest", None, False)
return_value = bridge.call_capl("InitTest",2, True )
value = bridge.read_signal("CAN1", "MsgID", "SignalName")
bridge.write_signal("CAN1", "MsgID", "SignalName", 100)
bridge.shutdown()
