# TopoMetricUncertainty
Uncertainties in topographic metrics due to truncation errors and elevation uncertainty.

Link to discussion paper: https://www.earth-surf-dynam-discuss.net/esurf-2018-96/

Code used to create the synthetic surfaces used in the paper can be found in "surfaces.py"

Code used to calculate truncation error and propagated elevation uncertainty can be found in "uncertainty.py"

A detailed description of several gridding methods for lidar data, including the ones used in this paper, can be found here: 

Lidar data source for lidar.npz, and the lidar data used in the paper: http://opentopo.sdsc.edu/datasetMetadata?otCollectionID=OT.082012.26911.1

"optimize_grid_spacing.py" is one potential method of finding the optimal grid spacing directly from a lidar dataset. 
