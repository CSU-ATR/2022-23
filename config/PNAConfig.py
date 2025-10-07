from dataclasses import dataclass


@dataclass
class PNAConfig:
    """A data class to hold the configurations required for the PNA"""
    s_parameter: str = None             # S Parameter in S11, S12, S21, S22
    source_power: float = None         # Source Power in dBm or watts
    start_frequency: float = None      # Start Frequency in Hz
    stop_frequency: float = None       # Stop Frequency in Hz
    if_bandwidth: float = None         # IF Bandwidth in Hz
    sweep_points: int = None           # Number of Sweep Points
    averaging_points: int = None       # Number of Averaging Points
    
    def __repr__(self):
        return (f"s_parameter {self.s_parameter}\n"
                f"Source Power {self.source_power}\n"
                f"Start Frequency {self.start_frequency}\n"
                f"Stop Frequency {self.stop_frequency}\n"
                f"IF Bandwidth {self.if_bandwidth}\n"
                f"Sweep Points {self.sweep_points}\n"
                f"Averaging Points {self.averaging_points}\n")

    def to_dict(self):
        return {
            "s_parameter" : self.s_parameter,
            "source_power": self.source_power,
            "start_frequency": self.start_frequency,
            "stop_frequency": self.stop_frequency,
            "if_bandwidth": self.if_bandwidth,
            "sweep_points": self.sweep_points,
            "averaging_points": self.averaging_points,
        }
