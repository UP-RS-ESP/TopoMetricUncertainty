# TopoMetricUncertainty
Codes and data associated with the paper: "Determining the Optimal Grid Resolution for Topographic Analysis on an Airborne Lidar Dataset" by Taylor Smith, Aljoscha Rheinwalt, and Bodo Bookhagen

Link to discussion paper: https://www.earth-surf-dynam-discuss.net/esurf-2018-96/

Code used to create the synthetic surfaces used in the paper can be found in "surfaces.py"

Code used to calculate truncation error and propagated elevation uncertainty can be found in "uncertainty.py"

A detailed description of several gridding methods for lidar data, including the ones used in this paper, can be found here: https://github.com/BodoBookhagen/Lidar_PC_interpolation

A full example and script for choosing the optimal grid resolution is included in the 'example' directory. This directory contains elevation and elevation standard deviation estimates for a subset of SCI from 2m to 30m resolution. Running the included script will generate a simple figure showing the optimal grid resolution for that region, given that error model.

"optimize_grid_spacing.py" is one other potential method of finding the optimal grid spacing directly from a lidar dataset. This method was not used in the above linked paper.

Lidar data source for lidar.npz, and the lidar data used in the paper: http://opentopo.sdsc.edu/datasetMetadata?otCollectionID=OT.082012.26911.1
