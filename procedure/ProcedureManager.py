from procedure.ScanData import ScanData
from interface.InterfaceManager import InterfaceManager
from config.ConfigManager import ConfigManager
from procedure import GCodeGenerator
from procedure import ScanController

import time

class ProcedureManager:
    
    def __init__(self, interfaces: InterfaceManager, configs: ConfigManager, debug=False, ui_output=True):
        self.scan_data = ScanData()
        self.interfaces = interfaces
        self.configs = configs
        self.filename = "Scan"
    
    def update_scan_data(self, new_scan_dataframe):
        """Takes in a data frame from the PNA output"""
        grbl_response = self.interfaces.grbl.get_response()
        self.scan_data.update_dataframe(new_scan_dataframe, grbl_response)
        self.save_dataframe()
    
    # def singular_plane_sweep_scan(self):
    #     gcode = GCodeGenerator.single_dimensional_sweeps_from_axes(self.configs.GRBLConfig)
    #     print(gcode)
    #     command_set = ScanController.compile_gcode_with_scan(gcode)
    #     ScanController.run(command_set, self.interfaces.grbl, self.interfaces.pna, self.scan_data, self.configs.PNAConfig)
    
    # def two_coordinate_plane_scan(self):
    #     gcode = GCodeGenerator.multi_dimensional_coordinates_from_axes(self.configs.GRBLConfig)
        # command_set = ScanController.compile_gcode_with_scan(gcode)
        # ScanController.run(command_set, self.interfaces.grbl, self.interfaces.pna, self.scan_data, self.configs.PNAConfig)
    
    def two_coordinate_plane_scan(self):
        gcode = GCodeGenerator.multi_dimensional_coordinates_from_axes(self.configs.GRBLConfig)
        print(gcode)
        
        self.scan(gcode)
        
    def singular_plane_sweep_scan(self):
        gcode = GCodeGenerator.single_dimensional_sweeps_from_axes(self.configs.GRBLConfig)
        print(gcode)
        self.scan(gcode)
    
    def scan(self, gcode_instructions):
        #Configure PNA
        print("Reset Data Frame")
        self.scan_data.reset_dataframe()
        self.interfaces.pna.configure_analyzer(self.configs.PNAConfig)

        for instruction in gcode_instructions:
            print(f"Running {instruction}")
            
            #Move ATR
            self.interfaces.grbl.send_instruction(instruction)
            status = self.interfaces.grbl.get_status()
            while status == "Run":
                status = self.interfaces.grbl.get_status()
                time.sleep(0.05)
        
            #Scan
            data = self.interfaces.pna.fetch_data()
            grbl_response = self.interfaces.grbl.get_response()
            self.scan_data.parse_position_from_response(grbl_response)
            self.scan_data.update_dataframe(data, grbl_response)
            self.scan_data.save_dataframe()
    
        print("done")

