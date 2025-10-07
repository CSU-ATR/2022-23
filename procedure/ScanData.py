from dataclasses import dataclass
import pandas as pd
import numpy as np
import re
from misc.Logger import Logger

@dataclass
class ScanData:
    columns = ['X', 'Y', 'Z', 'Polar', 'Azimuth', 'Elevation', 'Frequency', 'Magnitude', 'Phase']
    
    scan_data = pd.DataFrame(columns=columns)
    source = "ScanData"
    filename = "Scan"
    
    def parse_position_from_response(self, grbl_response):
        match = re.search(r'MPos:([0-9.-]+),([0-9.-]+),([0-9.-]+),([0-9.-]+),([0-9.-]+),([0-9.-]+)', grbl_response)
        if match:
            X = float(match.group(1))
            Y = float(match.group(2))
            Z = float(match.group(3))
            Polar = float(match.group(4))
            Azimuth = float(match.group(5))
            Elevation = float(match.group(6))
            return X, Y, Z, Polar, Azimuth, Elevation
        else:
            Logger.console("No Position Data Found", source=self.source, level="error")
            return None  # Return None if no match found

    def update_dataframe(self, new_scan_data, grbl_response):
        # Extract X, Y, Z, Polar, Azimuth, Elevation from grbl_response
        position = self.parse_position_from_response(grbl_response)
        if position is None:
            return
        
        X, Y, Z, Polar, Azimuth, Elevation = position
        
        new_scan_data_length = len(new_scan_data)
        
        # Create a temporary DataFrame for the position values
        temp_data = pd.DataFrame({
            'X': [X] * new_scan_data_length,
            'Y': [Y] * new_scan_data_length,
            'Z': [Z] * new_scan_data_length,
            'Polar': [Polar] * new_scan_data_length,
            'Azimuth': [Azimuth] * new_scan_data_length,
            'Elevation': [Elevation] * new_scan_data_length
        })
        
        # Ensure new_scan_data has a matching index and columns
        new_scan_data.reset_index(drop=True, inplace=True)
        
        # Combine temp_data (position data) and new_scan_data
        combined_data = temp_data.join(new_scan_data)
        
        # Ensure the columns match the order defined in 'columns'
        formatted_new_scan_dataframe = combined_data[self.columns]
        
        # Use np.vstack to vertically stack the current scan_data with the new data
        new_values = np.vstack([self.scan_data.values, formatted_new_scan_dataframe.values])
        
        # Create a new DataFrame from the stacked values
        self.scan_data = pd.DataFrame(new_values, columns=self.columns)

    def save_dataframe(self):
        filename=self.filename+".csv"
        self.scan_data.to_csv(filename, index=False)
    
    def set_filename(self, filename):
        self.filename = filename
    
    def reset_dataframe(self):
        self.scan_data = pd.DataFrame(columns=self.columns)
