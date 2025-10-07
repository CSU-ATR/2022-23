from interface.GRBLController import GRBL
from interface.PNAController import PNA
from misc.Logger import Logger

class InterfaceManager:
    def __init__(self, debug=False, ui_output=True):
        self.debug = debug
        self.ui_output = ui_output
        self.grbl = GRBL(debug=debug, ui_output=ui_output)
        self.pna = PNA(debug=debug, ui_output=ui_output)
        self.source = "Interface"
    
    def output_message(self, message, level="info"):
        if self.debug :
            Logger.console(message, self.source, level)
        
        if self.ui_output:
            Logger.ui(message, self.source, level)
            
    def initialize_connection(self):
        self.output_message("Initializing Connections")
        self.grbl.initialize()
        self.pna.setup_connection()
        if self.grbl.connection and self.pna.connection:
            self.output_message("ATR is ready to scan")
        else :
            self.output_message("Connections Failed", level="error")
        
    def close_connections(self):
        self.pna.close_connection()
        self.grbl.close_connection()
