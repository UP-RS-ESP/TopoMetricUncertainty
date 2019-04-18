''' 
This script takes a directory of DEMs and determines the optimal grid resolution.
Used as a toy example for the paper "Determining the Optimal Grid Resolution for Topographic Analysis on an Airborne Lidar Dataset" by T Smith, A Rheinwalt and B Bookhagen
Developed by Taylor Smith, April 18, 2019 
'''

import numpy as np
import matplotlib.pyplot as plt
import gdalnumeric

from surfaces import trunc_err_slope, trunc_err_aspect, peu_slope_field, peu_aspect_field

def QR(z, spacing, std, mask):
    '''
    Function that takes an elevation, grid spacing, elevation std, and a mask
    to return the Quality Ratio for both slope and aspect calculations
    '''
    trunc_slp = trunc_err_slope(z, spacing) 
    trunc_asp = trunc_err_aspect(z, spacing) / 4. 
    trunc_slp[mask] = np.nan
    trunc_asp[mask] = np.nan
    peu_slp = peu_slope_field(z, spacing, std) 
    peu_asp = peu_aspect_field(z, spacing, std) / 4.
    peu_slp[mask] = np.nan
    peu_asp[mask] = np.nan
    
    QRslp = (1 / (1 + np.abs(trunc_slp))) * (1 / (1 + np.abs(peu_slp)))
    QRasp = (1 / (1 + np.abs(trunc_asp))) * (1 / (1 + np.abs(peu_asp)))
    QRslp[mask] = np.nan
    QRasp[mask] = np.nan
    
    return QRslp, QRasp

#Loop through each DEM resolution
base_dir = '~/example/'
spacings = range(1, 31)[::-1]
qr_s, qr_a = [], []
for i in spacings:
    dem = base_dir + 'DEM/Pozo_UTM11_NAD83_g_' + str(i) + 'm.tif'
    uncertainty = base_dir + 'STD/Pozo_UTM11_NAD83_g_' + str(i) + 'm_std.tif'
    
    #Load the data as arrays
    elev = gdalnumeric.LoadFile(dem).astype(float)
    std = gdalnumeric.LoadFile(uncertainty).astype(float)
    
    #Mask out water areas
    mask = np.where(elev < 0)
    elev[mask] = np.nan
    std[mask] = np.nan
    
    #Calculate the Quality Ratios
    QRslp, QRasp = QR(elev, i, std, mask)
    QRslp[mask] = np.nan
    QRasp[mask] = np.nan
    
    #Append the QR mean values to a list
    qr_s.append(np.nanmean(QRslp))
    qr_a.append(np.nanmean(QRasp))
    print(i)

#Plot the QR curves    
plt.close('all')
f, (ax, ax2) = plt.subplots(2)
ax.plot(spacings, qr_s, 'k-')
ax2.plot(spacings, qr_a, 'k-')
ax2.set_xlabel('Grid Resolution (m)', fontsize=16)
ax.set_ylabel('Quality Ratio - Slope', fontsize=16)
ax2.set_ylabel('Quality Ratio - Aspect', fontsize=16)
ax.set_xlim(spacings[-1], spacings[0])
ax2.set_xlim(spacings[-1], spacings[0])

#Get the max
qr_s, qr_a = np.array(qr_s), np.array(qr_a)
ideal_space_slp = spacings[np.where(qr_s == np.nanmax(qr_s))[0][0]]
ideal_space_asp = spacings[np.where(qr_a == np.nanmax(qr_a))[0][0]]

#Add the max to the plot
ym, ya = ax.get_ylim()
ax.plot((ideal_space_slp, ideal_space_slp), (ym, ya), 'r--')
ax.text(ideal_space_slp, (ym + ya)/2, str(ideal_space_slp) + 'm', va='top', rotation='vertical', fontsize=16, color='r')
ax.set_ylim(ym, ya)

ym, ya = ax2.get_ylim()
ax2.plot((ideal_space_asp, ideal_space_asp), (ym, ya), 'r--')
ax2.text(ideal_space_asp, (ym + ya)/2, str(ideal_space_slp) + 'm', va='top', rotation='vertical', fontsize=16, color='r')
ax2.set_ylim(ym, ya)

plt.tight_layout()
plt.show()

