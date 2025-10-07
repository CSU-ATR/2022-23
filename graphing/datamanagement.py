from config.PNAConfig import PNAConfig
from config.GRBLConfig import Axes

import datetime
import h5py
import pandas as pd

class DataHandler:
    starttimestamp = 0
    stoptimestamp = "NA"
    axiis_information = 0
    pnaconfig_dict = 0
    axesconfig_dict = 0
    positions_dict = {}

    def set_time(self, timestamp):
        now = datetime.datetime.now()
        formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
        timestamp = formatted_date
    
    def set_pnaconfig(self, pnaconfig: PNAConfig):
        pna_dict = pnaconfig.to_dict()
        self.pnaconfig_dict = pna_dict
    
    def set_axesconfig(self, axesconfig: Axes):
        axes_dict = axesconfig.to_dict()
        self.axesconfig_dict = axes_dict
    
    def add_position(self, location, scans):
        pass
    
    def to_dict(self):

        return {
                "Start Time:": self.starttimestamp,
                "Stop Time:": self.stoptimestamp,
                "Axiis ": self.axesconfig_dict,
                "Scan Parameters": self.pnaconfig_dict,
                "Scan Description: ": 0
        }
    
    def encode_to_hdf5(self, filename, dataframe, metadata):
        with h5py.File(filename, 'w') as file:
            # Store DataFrame
            file.create_dataset('data', data=dataframe.values)
            
            # Add metadata
            for key, value in metadata.items():
                file.attrs[key] = value


if __name__ == "__main__":
    testPNAconfig = PNAConfig()
    testGRBLconfig = Axes()
    testGRBLconfig.X.stop = 10
    testGRBLconfig.Azimuth.stop = 100
    
    testDataHandler = DataHandler()
    testDataHandler.set_pnaconfig(testPNAconfig)
    testDataHandler.set_axesconfig(testGRBLconfig)
    testDataHandler.set_time(testDataHandler.starttimestamp)

    df = pd.read_csv('MRI_scan_02_03_afternoon.csv')
    df = df.sort_values("Frequency")

    print(df)

    metadata = testDataHandler.to_dict()
    
    testDataHandler.encode_to_hdf5('HDF5Test.h5', df, metadata)
    
    with h5py.File('HDF5Test.h5', 'r') as f:
    # Print metadata
        print("Metadata:")
        for key, value in f.attrs.items():
            print(f"{key}: {value}")