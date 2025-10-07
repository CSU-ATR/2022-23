import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

##read in data
# data = pd.read_csv('AzimuthElevationHorn.csv')

frequency_constant = 2.4e9
azimuth_constant = 10
elevation_constant = 0

data = pd.read_csv('Scan.csv')

data = data[data['Azimuth'] == azimuth_constant]
# data = data[data['Elevation'] == elevation_constant]
data = data[data['Frequency'] == frequency_constant]

print(data)


elevation_raw = data["Elevation"].values
# elevation_raw = data["Azimuth"].values
magnitude_raw = data["Magnitude"].values
# magnitude_db = 20*np.log10(magnitude_raw)
magnitude_db = magnitude_raw

elevation_polar = np.radians(elevation_raw)

fig = plt.figure()
ax = fig.add_subplot(projection='polar')
c = ax.scatter(elevation_polar, magnitude_db)
plt.show()



