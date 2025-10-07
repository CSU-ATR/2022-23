from interface.InterfaceManager import InterfaceManager
from procedure.ProcedureManager import ProcedureManager
from gui.GUIManager import GUIManager
from config.ConfigManager import ConfigManager

import atexit
import threading

def on_exit():
    """Define Exit behavior even if Unexpected"""
    try:
        stop_event.set()
        interfaces.close_connections()
        print("connections closed")
    except Exception as e:
        pass

def background_initialization():
    """Tasks that need to be run in the background as GUI Initializes"""
    try:
        interfaces.initialize_connection()
    except Exception as e:
        pass

atexit.register(on_exit) #Register the function to close with
stop_event = threading.Event() #Create a threading event for closing

# Initialize managers
configs = ConfigManager()
interfaces = InterfaceManager(debug=True, ui_output=True)
procedures = ProcedureManager(interfaces, configs)
guis = GUIManager(procedures, interfaces, configs)

# Start background initialization task in a daemon thread
initialization_thread = threading.Thread(target=background_initialization, daemon=True)
initialization_thread.start()

# Main GUI loop
guis.root.mainloop()

print("closing connections")
