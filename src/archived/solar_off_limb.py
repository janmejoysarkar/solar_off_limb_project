#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 14:32:19 2023

@author: janmejoy
-Created to amplify off limb features by 10 times (or custom)
for visualization of prominences in SUIT NB3 and NB4 images.
-Modified: 
2023-12-20
2024-01-10: Added provision to enter sun center information from .suncenter file.
This will automatically fetch the sun image and visualize it.
This is made to work with 2kx2k images only.
sshfs may be installed to mount remote file system to local computer.
2024-01-11: Check for file availability added. Mount location for /scratch added.
"""
import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
import glob

def create_circular_mask(h, w, center, radius):

    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - center[0])**2 + (Y-center[1])**2)

    mask = dist_from_center <= radius
    return mask

def plot(path, sc):
    folder= path+'suit_data/level1fits/'+ sc[0].split(sep='T')[0].replace("-", "/")+'/normal_2k/'
    file=glob.glob(folder+"*"+sc[0]+"*")

    if len(file) != 0:
        file=file[0]
        print("File Exists.... Plotting")
        position, radius= (float(sc[1])/2, (float(sc[3])-20)/2), float(sc[5])/2 # To be imported from sun center and radius finding code.
        amp=10 #off disk amplification factor
        
        data= fits.open(file)[0].data #open desired file
        h,w= data.shape 
        mask= np.ones((h,w))*create_circular_mask(h, w, position, radius)
        mask=np.where(mask<1, amp, mask) #contains amplification factor (amp) for off disk feature
        offdisk= data*mask
        outermask= np.ones((h,w))*create_circular_mask(h, w, position, radius+150) #controls the size of outer mask
        
        plt.figure(figsize=(12,8))
        plt.imshow(offdisk*outermask,vmin=1500, vmax=65000, origin='lower', cmap='hot')
        plt.show()
    else:
        print("File Not available")

path="/home/janmejoyarch/sftp_drive/" #mount location of /scratch folder on SUIT server.
plot(path, input("Sun center information: ").split(sep=','))#enter sun-center prompt
