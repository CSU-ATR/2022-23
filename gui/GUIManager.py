from gui.GRBLConfigViewController import GRBLConfigViewController
from gui.PNAConfigViewController import PNAConfigViewController
from gui.TerminalViewController import TerminalViewController

from procedure.ProcedureManager import ProcedureManager
from interface.InterfaceManager import InterfaceManager
from config.ConfigManager import ConfigManager

import tkinter as tk

class GUIManager:
    
    def __init__(self, procedures: ProcedureManager, interfaces: InterfaceManager, configs: ConfigManager):
        self.procedures = procedures
        self.interfaces = interfaces
        self.configs = configs
        
        # Create the root window
        self.root = tk.Tk()

        # Initialize the controller frames (widgets), passing root as parent
        self.GRBLController = GRBLConfigViewController(self.root)
        self.PNAController = PNAConfigViewController(self.root)
        self.TerminalController = TerminalViewController(self.root, self.interfaces, self.configs, self.procedures, self)
        
        # Grid layout to position the frames on the root window
        self.GRBLController.gui.grid(row=0, column=0, sticky="nsew")  # Position the frame in the root window
        self.PNAController.gui.grid(row=0, column=1, sticky="nsew")  # Position the frame in the root window
        self.TerminalController.gui.grid(row=1, column=0, columnspan=2, sticky="nsew")  # Position the frame in the root window
        
        # Configure grid row and column weights to make the layout responsive
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        # Set the root window size (optional)
        self.root.geometry("480x600")
        
