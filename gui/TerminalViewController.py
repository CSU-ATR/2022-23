from gui.TerminalView import TerminalView
from interface.InterfaceManager import InterfaceManager
from config.ConfigManager import ConfigManager
from procedure.ProcedureManager import ProcedureManager

from misc.Commands import Commands
from misc.Logger import Logger

import tkinter as tk

class TerminalViewController:

    def __init__(self, parent, interfaces: InterfaceManager, configs: ConfigManager, procedures: ProcedureManager, manager):
        self.gui = TerminalView(parent, self)  # Instantiate Terminal UI and pass self
        self.interfaces = interfaces
        self.configs = configs
        self.procedures = procedures
        self.manager = manager
        self.commands = Commands(self.interfaces, self.configs, self.procedures, self.manager.GRBLController, self.manager.PNAController)
        self.source = "Terminal"
        
        Logger._ui_terminal = self #Pass Logger this instance of terminal for message display
    
    def clear_terminal(self):
        """clears the terminal"""
        self.gui.textbox.config(state=tk.NORMAL)
        self.gui.textbox.delete(1.0, tk.END)
        self.gui.textbox.config(state=tk.DISABLED)

    def display(self, message):
        """Sends a string or list of strings to terminal display"""
        self.gui.append_message(message)
    
    #We process commands here that way Terminal doesnt need to be passed around, and can just use Commands class as a helper class
    def process_command(self, command):
        """takes a command parses it and executes it
        parse command to check if its multiple segments"""
        
        parts = command.split(maxsplit=1) #Split command into its individual entries
        base_command = parts[0] #first part of the command
        args = parts[1] if len(parts) > 1 else None #creates second set if there is any

        command_entry = self.commands.dict.get(base_command) #parses the dictionary for the base command
        
        if command_entry: #if it exists within the command dictionary
            method_name = command_entry["function"] #pulls the function associated with the command
            method = getattr(self.commands, method_name)
            
            if method_name == "clear_terminal": #Handle clearing terminal in house because of tkinter objects (sloppy but functional)
                self.clear_terminal()
                
            elif method_name == "grbl_commands": #grbl is a multipart command
                method(args)
                
            else:
                method()
        else:
            self.commands.unknown_command(command) #command not found in dictionary
        