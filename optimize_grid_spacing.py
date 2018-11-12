import numpy as np
import uncertainty as uc
from matplotlib import pyplot as pl

def read_point_cloud(fname = 'lidar.npz'):
    global x, y, z
    """
    Returns:
    (x, y, z)

    """
    f = np.load(fname)
    x = f['x']
    y = f['y']
    z = f['z']
    f.close()

def grid_point_cloud(width = 1):
    """
    Aggregates a point cloud (x, y, z) to a
    grid with grid cell spacing width.

    Returns:
    (mean, std, xbounds, ybounds)

    """
    from scipy.spatial import cKDTree as kdtree

    xmin, xmax = x.min(), x.max()
    ymin, ymax = y.min(), y.max()
    xb = np.arange(xmin, xmax+width, width)
    yb = np.arange(ymin, ymax+width, width)
    xr = xb[:-1] + width/2.0
    yr = yb[:-1] + width/2.0
    xc, yc = np.meshgrid(xr, yr)
    shape = xc.shape
    xc = xc.ravel()
    yc = yc.ravel()
    tree = kdtree(np.transpose((x, y)))
    grid = kdtree(np.transpose((xc, yc)))
    lsts = grid.query_ball_tree(tree, r = width/np.sqrt(2))
    n = len(lsts)
    m = np.zeros(n)
    s = np.zeros(n)
    for i in range(n):
        if len(lsts[i]) < 3:
            m[i] = np.nan
            s[i] = np.nan
        else:
            j = lsts[i]
            m[i] = z[j].mean()
            s[i] = z[j].std()
    m.shape = shape
    s.shape = shape
    return (m, s, xb, yb)

def plot_fields(var, xb, yb, title, fname, paperwidth = 10):
    """
    Produces a DIN paper PNG figure with all six fields.

    """
    label = (r'Mean elevation [m]', r'Elevation STD [m]',
             r'Aspect PEU [deg]', r'Slope PEU [deg]',
             r'Aspect truncation error [deg]', r'Slope truncation error [deg]')
    cmaps = (pl.cm.viridis, pl.cm.magma_r,
             pl.cm.Purples, pl.cm.Purples,
             pl.cm.seismic, pl.cm.seismic)

    fg, ax = pl.subplots(3, 2,
        figsize = (paperwidth, paperwidth*np.sqrt(2)))
    pl.suptitle(title)
    j = 0
    for i in range(3):
        for k in range(2):
            v = np.ma.masked_invalid(var[j])
            if 0 > v.min():
                vmin = np.nanpercentile(v, 2)
                vmax = -vmin
            else:
                vmin = v.min()
                vmax = np.nanpercentile(v, 98)
            im = ax[i, k].pcolormesh(xb, yb, v,
                    vmin = vmin,
                    vmax = vmax,
                    cmap = cmaps[j])
            cb = fg.colorbar(im, ax = ax[i, k], shrink = 0.75)
            cb.set_label(label[j])
            ax[i, k].set_aspect('equal')
            j += 1

    fg.tight_layout()
    pl.savefig(fname)

def median_slope_uncertainty(width):
    mean, stdr, _, _ = grid_point_cloud(width)
    eslp = uc.peu_slope_field(mean, width, stdr)
    tslp = np.abs(uc.trunc_err_slope(mean, width))
    return np.nanmedian(eslp+tslp)

def median_aspect_uncertainty(width):
    mean, stdr, _, _ = grid_point_cloud(width)
    easp = uc.peu_aspect_field(mean, width, stdr)
    tasp = np.abs(uc.trunc_err_aspect(mean, width))
    return np.nanmedian(easp+tasp)

def optimize_grid_spacing(wmin, wmax):
    from scipy.optimize import minimize_scalar

    print('minimize aspect uncertainty:')
    rasp = minimize_scalar(median_aspect_uncertainty,
                bounds = (wmin, wmax), method = 'bounded')
    print(rasp)
    print('minimize slope uncertainty:')
    rslp = minimize_scalar(median_slope_uncertainty,
                bounds = (wmin, wmax), method = 'bounded')
    print(rslp)
    wasp, wslp = rasp.x, rslp.x
    return (wasp, wslp)

def main():
    global x, y, z

    # read part of a real lidar point cloud
    read_point_cloud()
    xmin, ymin = x.min(), y.min()
    x -= xmin
    y -= ymin

    # get optimal grid spacing for aspect and slope
    wmin, wmax = 0.5, 10
    wasp, wslp = optimize_grid_spacing(wmin, wmax)

    # its better to have to large grid spacings than to small
    width = max(wasp, wslp)

    # aggregate the point cloud
    mean, stdr, xb, yb = grid_point_cloud(width)
    xb += xmin
    yb += ymin

    # propagated elevation uncertainty E of aspect
    easp = uc.peu_aspect_field(mean, width, stdr)

    # propagated elevation uncertainty E of slope
    eslp = uc.peu_slope_field(mean, width, stdr)

    # truncation error T for aspect
    tasp = uc.trunc_err_aspect(mean, width)

    # truncation error T for slope
    tslp = uc.trunc_err_slope(mean, width)

    # figure
    title = 'Optimal lidar point cloud example'
    fname = 'lidar_dem%.2f_optimal.png' % width
    field = (mean, stdr,
             easp, eslp,
             tasp, tslp)
    plot_fields(field, xb, yb, title, fname)

if __name__ == '__main__':
    main()
