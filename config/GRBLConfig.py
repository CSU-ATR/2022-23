from dataclasses import dataclass

@dataclass
class Axis_Components:
    """Helper data class to hold the values for each axis"""
    start: float = 0.0
    stop: float = 0.0
    resolution: float = 0.0
    gCodeName: str = None
    axisName: str = None
    
    # Custom print for the data in an axis
    def __repr__(self):
        return (
                f"----------------------------------\n"
                f"Axis: {self.axisName}\n"
                f"Start: {self.start}\n"
                f"Stop: {self.stop}\n"
                f"Resolution: {self.resolution}\n"
                f"GCodeName {self.gCodeName}")

@dataclass
class Axes:
    """Data class that holds all of the positional requirements from the user"""
    X: Axis_Components
    Y: Axis_Components
    Z: Axis_Components
    Polar: Axis_Components
    Azimuth: Axis_Components
    Elevation: Axis_Components

    def __init__(self):
        # Initialize the components if they aren't already initialized
        self.X = Axis_Components()
        self.Y = Axis_Components()
        self.Z = Axis_Components()
        self.Polar = Axis_Components()
        self.Elevation = Axis_Components()
        self.Azimuth = Axis_Components()
        
        # Hardcode the G-code names after instantiation
        self.X.gCodeName = "X"
        self.X.axisName = "X"
        
        self.Y.gCodeName = "Y"
        self.Y.axisName = "Y"
        
        self.Z.gCodeName = "Z"
        self.Z.axisName = "Z"
        
        self.Polar.gCodeName = "A"
        self.Polar.axisName = "Polar"
        
        self.Azimuth.gCodeName = "B"
        self.Azimuth.axisName = "Azimuth"
        
        self.Elevation.gCodeName = "C"
        self.Elevation.axisName = "Elevation"
        
    # Make Axii iterable by returning components as a list of axes
    def __iter__(self):
        return iter([self.X, self.Y, self.Z, self.Polar, self.Azimuth, self.Elevation])

    # Custom printout of all the axes in the datastructure
    def __repr__(self):
        return (f"Movement Settings\n"
                f"{self.X}\n"
                f"{self.Y}\n"
                f"{self.Z}\n"
                f"{self.Polar}\n"
                f"{self.Azimuth}\n"
                f"{self.Elevation}\n")
    
    def to_dict(self):
        axes_dict = {}
        for axis_name, axis_obj in self.__dict__.items():
            if axis_obj.start != axis_obj.stop:
                single_axis_dict = {
                    "Start": axis_obj.start,
                    "Stop": axis_obj.stop,
                    "Resolution": axis_obj.resolution
                }

                axes_dict[axis_name] = single_axis_dict
        
        return axes_dict

    def getGCodeName(self):
        return self.gCodeName
