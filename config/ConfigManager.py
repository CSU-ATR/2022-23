from config.GRBLConfig import Axes
from config.PNAConfig import PNAConfig

class ConfigManager:
    def __init__(self):
        self.GRBLConfig = Axes()
        self.PNAConfig = PNAConfig()
        
    #Functionality to load and save these axes from files
        