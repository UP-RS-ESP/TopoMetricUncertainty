import numpy as np

def circstd(phi, axis = 0):
    p = (phi - 180) * np.pi / 180.
    x = np.mean(np.cos(p), axis = axis)
    y = np.mean(np.sin(p), axis = axis)
    return np.sqrt(-2*np.log(np.sqrt(x*x+y*y)))*180/np.pi

def np_aspect(z, d):
    dy, dx = np.gradient(z, d)
    return np.arctan2(dy, dx)*180/np.pi+180

def np_slope(z, d):
    dy, dx = np.gradient(z, d)
    return np.arctan(np.sqrt(dx*dx+dy*dy))*180/np.pi

def peu_aspect(z, d):
    dy, dx = np.gradient(z, d)
    v = dy / dx
    u = 180 / np.pi
    u /= d * np.sqrt(2 + v*v*2)
    return u / np.abs(dx)

def peu_slope(z, d):
    dy, dx = np.gradient(z, d)
    v = np.sqrt(dx*dx + dy*dy)
    u = 180 / np.pi
    u /= np.sqrt(2) * d * (1 + v*v)
    return u

def peu_aspect_field(z, d, std):
    dy, dx = np.gradient(z, d)
    v = dy / dx
    u = np.cos(np.arctan2(dy, dx))
    u *= u
    u *= 90. / np.pi
    u /= d * np.abs(dx)
    n = std.shape[0]
    m = std.shape[1]
    ex1 = np.hstack((std[:,1:], np.zeros(n)[:, None]))
    ex2 = np.hstack((np.zeros(n)[:, None], std[:,:-1]))
    ey1 = np.vstack((std[1:,:], np.zeros(m)))
    ey2 = np.vstack((np.zeros(m), std[:-1,:]))
    u *= np.sqrt(v*v*(ex1*ex1+ex2*ex2)+ey1*ey1+ey2*ey2)
    return u

def peu_slope_field(z, d, std):
    dy, dx = np.gradient(z, d)
    v = np.sqrt(dx*dx + dy*dy)
    u = 90. / np.pi / d
    u /= v * (1 + v*v)
    n = std.shape[0]
    m = std.shape[1]
    ex1 = np.hstack((std[:,1:], np.zeros(n)[:, None]))
    ex2 = np.hstack((np.zeros(n)[:, None], std[:,:-1]))
    ey1 = np.vstack((std[1:,:], np.zeros(m)))
    ey2 = np.vstack((np.zeros(m), std[:-1,:]))
    u *= np.sqrt(dx*dx*(ex1*ex1+ex2*ex2)+dy*dy*(ey1*ey1+ey2*ey2))
    return u

def trunc_err_slope(z, d):
    n = z.shape[0]
    dy, dx = np.gradient(z, d)
    _, ddx = np.gradient(dx, d)
    ddy, _ = np.gradient(dy, d)
    _, dddx = np.gradient(ddx, d)
    dddy, _ = np.gradient(ddy, d)
    del ddx, ddy
    ex = d * d * dddx / 6.
    ey = d * d * dddy / 6.
    del dddx, dddy
    g2 = dx*dx+dy*dy
    sg = np.arctan(np.sqrt((dx+ex)**2+(dy+ey)**2))
    sg -= np.arctan(np.sqrt((dx-ex)**2+(dy-ey)**2))
    return np.sign(sg)*np.sqrt((dx*dx*ex*ex+dy*dy*ey*ey+2*dx*dy*ex*ey)/g2/(1+g2)/(1+g2))*180/np.pi

def trunc_err_aspect(z, d):
    n = z.shape[0]
    dy, dx = np.gradient(z, d)
    _, ddx = np.gradient(dx, d)
    ddy, _ = np.gradient(dy, d)
    _, dddx = np.gradient(ddx, d)
    dddy, _ = np.gradient(ddy, d)
    del ddx, ddy
    ex = d * d * dddx / 6.
    ey = d * d * dddy / 6.
    del dddx, dddy
    g2 = dx*dx+dy*dy
    u2 = np.cos(np.arctan2(dy, dx))**4
    sg = np.arctan2(dy+ey, dx+ex) - np.arctan2(dy-ey, dx-ex)
    return np.sign(sg)*np.sqrt(u2*(ex*ex*dy*dy/dx/dx+ey*ey-2*dy/dx*ex*ey)/dx/dx)*180/np.pi

