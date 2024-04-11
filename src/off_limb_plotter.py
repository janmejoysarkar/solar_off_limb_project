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
import glob

def create_circular_mask(h, w, col, row, radius): 
    '''
    *** creates circular mask of desired size ***
    - h, w: height and width of canvas
    - col, row: column and row of circle center
    - radius= radius of circle
    '''
    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - col)**2 + (Y-row)**2)
    mask = dist_from_center <= radius
    return mask #can be circular mask of any size

def image_generator(path): 
    '''
    *** generates limb enhanced images ***
    path: path of the input file
    '''
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
    print(path[-64:]+' Done')
    return(offdisk*outermask) #returns limb enhanced images

def savfig(arrayinput, fname, sav): 
    '''
    *** plots and saves png with matplotlib ***
    arrayinput:Input array to be plotted
    fname: Filename of the sun image
    sav: Save folder for png files
    '''
    plt.figure(figsize=(12,8))
    plt.imshow(arrayinput, origin='lower', cmap='hot')
    plt.title(fname[-37:-5])
    plt.savefig(sav+fname[-64:-5]+'_cor.png'); print(fname[-64:-5]+'_cor.png'+' Saved!')
    plt.close()
    
if __name__=='__main__':
    #### USER-DEFINED ####
    project_path= os.path.expanduser('~/Dropbox/Janmejoy_SUIT_Dropbox/SUIT_publicity/solar_off_limb_project/')
    path= project_path+'data/raw/*' #source folder for the data
    sav=project_path+'products/' #save path for png files
    ######################
    
    filepath_list= glob.glob(path)
    
    for file in filepath_list:
        output= image_generator(file)
        savfig(output, file, sav)
