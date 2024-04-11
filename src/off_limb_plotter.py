#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  9 18:43:55 2024
- Used to generate SUIT coronagraphic images from 2k 2k images.
- Requirements: 2k level 1 images with embedded sun center info.
@author: janmejoyarch
"""

import matplotlib.pyplot as plt
import numpy as np
from astropy.io import fits
import os

def create_circular_mask(h, w, col, row, radius): #creates circular mask
    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - col)**2 + (Y-row)**2)
    mask = dist_from_center <= radius
    return mask

def image_generator(path): #generates limb enhanced images
    file=os.path.expanduser(path)
    amp=10 #off disk amplification factor
    
    hdu=fits.open(file)[0]
    data= hdu.data #open desired file
    h,w= data.shape 
    col, row, radius= hdu.header['CRPIX1'], hdu.header['CRPIX2'], (hdu.header['R_SUN'])
    
    mask= np.ones((h,w))*create_circular_mask(h, w, col, row, radius)
    mask=np.where(mask<1, amp, mask) #contains amplification factor (amp) for off disk feature
    offdisk= data*mask
    outermask= np.ones((h,w))*create_circular_mask(h, w, col, row, radius+50) #controls the size of outer mask
    return(offdisk*outermask)

def plotting(output): #plots with matplotlib
    plt.figure(figsize=(12,8))
    plt.imshow(output, origin='lower', cmap='hot')
    plt.show()

if __name__=='__main__':
    path='~/sftp_drive/suit_data/level1fits/2024/01/24/normal_2k/SUT_T24_0196_000040_Lev1.0_2024-01-24T17.11.08.249_0972NB04.fits'
    output= image_generator(path)
    plotting(output)
