import sys
import numpy as np

def gaussian_hill_dem(width, bounds = [-2.5, 2.5, -2.5, 2.5]):
    xmin, xmax = bounds[0], bounds[1]
    ymin, ymax = bounds[2], bounds[3]
    xb = np.arange(xmin, xmax, width)
    yb = np.arange(ymin, ymax, width)
    xr, yr = xb[:-1]+width/2., yb[:-1]+width/2.
    x, y = np.meshgrid(xr, yr)
    r = np.sqrt(x*x + y*y)
    z = np.exp(-r*r)
    return (xb, yb, z)
    
def sphere_dem(width, bounds = [-2.5, 2.5, -2.5, 2.5]):
    xmin, xmax = bounds[0], bounds[1]
    ymin, ymax = bounds[2], bounds[3]
    xb = np.arange(xmin, xmax, width)
    yb = np.arange(ymin, ymax, width)
    xr, yr = xb[:-1]+width/2., yb[:-1]+width/2.
    x, y = np.meshgrid(xr, yr)
    r = np.sqrt(x*x + y*y)
    r0 = y.max()
    th = np.arccos(r/r0)
    z = r0 * np.sin(th)
    rc = r0 - 2 * width
    z[r > rc] = np.nan
    return (xb, yb, z)

def main():
    from matplotlib import pyplot as pl

    xb, yb, z = gaussian_hill_dem(0.1)
    pl.pcolormesh(xb, yb, z)
    pl.colorbar()
    pl.show()

    xb, yb, z = sphere_dem(0.1)
    z = np.ma.masked_invalid(z)
    pl.pcolormesh(xb, yb, z)
    pl.colorbar()
    pl.show()

if __name__ == '__main__':
    main()

