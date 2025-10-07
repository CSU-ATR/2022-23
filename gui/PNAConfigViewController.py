from gui.PNAConfigView import PNAConfigView
from config.PNAConfig import PNAConfig

import tkinter as tk

class PNAConfigViewController:
    UI_FONT = ("Arial", 8, "bold")
    SPINBOX_WIDTH = 10
    COMBOBOX_WIDTH = 10
    PADX = 5
    PADY = 5
    MAX_COLUMN_WIDTH = 150  # Max width for column
    COLUMN0_WEIGHT = 1
    COLUMN1_WEIGHT = 1
    ROW_WEIGHT = 1
    
    GHz_to_Hz = 1e9
    
    #(start, _from, to, increment)
    box_settings = {
        "S Parameter": (["S11", "S12", "S21", "S22"], "S21"), #
        "Source Power (dB)": (-10, -100, 100, 1),
        "Start Frequency (GHz)": (1.0, 10e-3, 50.0, 0.001),  # Scaled to GHz
        "Stop Frequency (GHz)": (6.0, 10e-3, 50.0, 0.001),  # Scaled to GHz
        "IF Bandwidth": (20, 1, 10_000, 1),
        "Sweep Points": (21, 2, 1001, 1),
        "Averaging Points": (10, 1, 100, 1),
        }
    
        
    box_count = len(box_settings)
    
    def __init__(self, parent):
        settings = {
            "font": self.UI_FONT,
            "spinbox_width": self.SPINBOX_WIDTH,
            "combobox_width": self.COMBOBOX_WIDTH,
            "padx": self.PADX,
            "pady": self.PADY,
            "max_column_width": self.MAX_COLUMN_WIDTH,
            "box_settings": self.box_settings,
            "box_count": self.box_count,
            "column_0_weight": self.COLUMN0_WEIGHT,
            "column_1_weight": self.COLUMN1_WEIGHT,
            "row_weight": self.ROW_WEIGHT,
        }
        
        self.gui = PNAConfigView(parent, settings)  # Create an instance of PNAConfigView
    
    def get_config_values(self):
        # Create an array of the keys in box_settings called parameter_names
        parameter_names = list(self.box_settings.keys())
        
        # Get the parameters from the GUI
        params = self.gui.get_parameters()
        
        # Create config_values with converted frequencies in the same line
        config_values = {
            "s_parameter": params.get(parameter_names[0]),  # S Parameter
            "source_power": float(params.get(parameter_names[1])) if params.get(parameter_names[1]) else None,  # Source Power
            "start_frequency": float(params.get(parameter_names[2])) * self.GHz_to_Hz if params.get(parameter_names[2]) else None,  # Start Frequency in Hz
            "stop_frequency": float(params.get(parameter_names[3])) * self.GHz_to_Hz if params.get(parameter_names[3]) else None,  # Stop Frequency in Hz
            "if_bandwidth": float(params.get(parameter_names[4])) if params.get(parameter_names[4]) else None,  # IF Bandwidth
            "sweep_points": int(params.get(parameter_names[5])) if params.get(parameter_names[5]) else None,  # Sweep Points
            "averaging_points": int(params.get(parameter_names[6])) if params.get(parameter_names[6]) else None,  # Averaging Points
        }
        
        # Return the PNAConfig with the dynamically retrieved values
        return PNAConfig(
            s_parameter=config_values.get("s_parameter"),
            source_power=float(config_values.get("source_power")),
            start_frequency=float(config_values.get("start_frequency")),
            stop_frequency=float(config_values.get("stop_frequency")),
            if_bandwidth=float(config_values.get("if_bandwidth")),
            sweep_points=int(config_values.get("sweep_points")),
            averaging_points=int(config_values.get("averaging_points")),
        )