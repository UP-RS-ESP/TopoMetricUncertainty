# TopoMetricUncertainty
The related paper can be found here:
Smith, T., Rheinwalt, A., and Bookhagen, B.: Determining the optimal grid resolution for topographic analysis on an airborne lidar dataset, Earth Surf. Dynam., 7, 475–489, https://doi.org/10.5194/esurf-7-475-2019, 2019.

V1.0 of the sofware can be cited as:
Smith, Taylor; Rheinwalt, Aljoscha; Bookhagen, Bodo (2019): TopoMetricUncertainty - Calculating Topographic Metric Uncertainty and Optimal Grid Resolution. V. 1.0. GFZ Data Services. http://doi.org/10.5880/fidgeo.2019.017

# Code Description
Code used to create the synthetic surfaces used in the paper can be found in "surfaces.py"

Code used to calculate truncation error and propagated elevation uncertainty can be found in "uncertainty.py"

A detailed description of several gridding methods for lidar data, including the ones used in this paper, can be found here: https://github.com/BodoBookhagen/Lidar_PC_interpolation

A full example and script for choosing the optimal grid resolution is included in the 'example' directory. This directory contains elevation and elevation standard deviation estimates for a subset of SCI from 2m to 30m resolution. Running the included script will generate a simple figure showing the optimal grid resolution for that region, given that error model.

"optimize_grid_spacing.py" is one other potential method of finding the optimal grid spacing directly from a lidar dataset. This method was not used in the above linked paper.

# Source Data
Lidar data source for lidar.npz, and the lidar data used in the paper: http://opentopo.sdsc.edu/datasetMetadata?otCollectionID=OT.082012.26911.1
