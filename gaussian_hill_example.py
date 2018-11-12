import numpy as np
import uncertainty as uc
from matplotlib import pyplot as pl

def gaussian_point_cloud(npts = 2e5):
    """
    Generate a uniform randomly distributed
    point cloud with npts points of a Gaussian hill.

    Returns:
    (x, y, z)

    """
    n = int(npts)
    x = 4 * (np.random.random(n) - 0.5)
    y = 4 * (np.random.random(n) - 0.5)
    z = np.exp(-x*x-y*y)
    return (x, y, z)

def grid_point_cloud(x, y, z, width = 0.1):
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
        if len(lsts[i]) < 5:
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
    width = abs(xb[0]-xb[1])
    xr = xb[:-1] + width/2.0
    yr = yb[:-1] + width/2.0
    xc, yc = np.meshgrid(xr, yr)
    rc = np.sqrt(xc*xc+yc*yc)

    fg, ax = pl.subplots(3, 2,
        figsize = (paperwidth, paperwidth*np.sqrt(2)))
    pl.suptitle(title)
    j = 0
    for i in range(3):
        for k in range(2):
            v = var[j]
            v[rc >= 2] = np.nan
            v = np.ma.masked_invalid(v)
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
            cb = fg.colorbar(im, ax = ax[i, k], shrink = 0.72)
            cb.set_label(label[j])
            ax[i, k].set_aspect('equal')
            j += 1

    fg.tight_layout()
    pl.savefig(fname)

def main():
    # measurement noise
    noise = 5e-3

    # grid spacing width
    width = 0.1

    # perfect elevation measurements z of a Gaussian hill
    x, y, z = gaussian_point_cloud()

    # assuming noise on elevations
    z += np.random.normal(0, noise, len(z))

    # aggregate the point cloud
    mean, stdr, xb, yb = grid_point_cloud(x, y, z, width)

    # propagated elevation uncertainty E of aspect
    easp = uc.peu_aspect_field(mean, width, stdr)

    # propagated elevation uncertainty E of slope
    eslp = uc.peu_slope_field(mean, width, stdr)

    # truncation error T for aspect
    tasp = uc.trunc_err_aspect(mean, width)

    # truncation error T for slope
    tslp = uc.trunc_err_slope(mean, width)

    # figure
    title = 'Gaussian hill point cloud example'
    fname = 'gaussian_hill_dem%.2f.png' % width
    field = (mean, stdr,
             easp, eslp,
             tasp, tslp)
    plot_fields(field, xb, yb, title, fname)

if __name__ == '__main__':
    main()
