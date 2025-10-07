from config.PNAConfig import PNAConfig
from config.GRBLConfig import Axes

import h5py
import pandas as pd
import datetime

class DataHandler:
    starttimestamp = 0
    stoptimestamp = 0
    axiis_information = 0
    pnaconfig_dict = 0
    axesconfig_dict = 0
    positions_dict = {}
    metadata = {}
    dataframe = pd.DataFrame()
    filename = "h5py_test.h5"
    
    def get_time(self):
        now = datetime.datetime.now()
        formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
        return formatted_date
    
    def set_pnaconfig(self, pnaconfig: PNAConfig):
        pna_dict = pnaconfig.to_dict()
        self.pnaconfig_dict = pna_dict

    def set_axesconfig(self, axesconfig: Axes):
        axes_dict = axesconfig.to_dict()
        self.axesconfig_dict = axes_dict
    
    def set_metadata(self):
        self.metadata = {
                "Start Time:": self.starttimestamp,
                "Stop Time:": self.stoptimestamp,
                "Axiis ": self.axesconfig_dict,
                "Scan Parameters": self.pnaconfig_dict,
                "Scan Description: ": 0
        }

    def write_to_HDF5(self):
        with h5py.File(self.filename, 'w') as file:

            file.create_dataset('data', data=self.dataframe.values)
        
            for key, value in self.metadata.items():
                file.attrs[key] = value

    def read_from_HDF5(self):
        with h5py.File(self.filename, "r") as readfile:
            
            retrieved_metadata = {}
            for key, value in readfile.attrs.items():
                retrieved_metadata[key] = value
            
            retrieved_data = readfile['data'][:]
            dataframe = pd.DataFrame(retrieved_data)
            
            return retrieved_metadata, retrieved_data

testPNAconfig = PNAConfig()
testGRBLconfig = Axes()
testGRBLconfig.X.stop = 10
testGRBLconfig.Azimuth.stop = 100

testDataHandler = DataHandler()
testDataHandler.dataframe = pd.read_csv('MRI_scan_02_03_afternoon.csv')

testDataHandler.set_axesconfig(testGRBLconfig)
# testDataHandler.set_pnaconfig(testPNAconfig)
testDataHandler.starttimestamp = testDataHandler.get_time()
testDataHandler.set_metadata()

testDataHandler.write_to_HDF5()

meta, data = testDataHandler.read_from_HDF5()
# print(meta, data)
print(meta)