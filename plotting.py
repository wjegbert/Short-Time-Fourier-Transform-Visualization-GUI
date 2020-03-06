# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 13:13:52 2020

@author: WILLIAM EGBERT
"""

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import math


def plot3D(dat, fname, chs, freqs, times):
    layout = math.ceil(math.sqrt(chs))
    fig = plt.figure()
    fig.suptitle(fname) #title
    for i in range(chs):
        meshx, meshy = np.meshgrid(times, freqs)
        
        ax = fig.add_subplot(layout, layout, i+1, projection='3d')
        ax.plot_surface(
                meshx, meshy, np.abs(dat[i]), 
                rstride=1, cstride=1, cmap=cm.jet, 
                linewidth=0, antialiased=False)
        ax.set_title("Channel "+ str(i+1))
        

def plotPColor(dat, fname, chs, freqs, times):
    layout = math.ceil(math.sqrt(chs))
    fig = plt.figure()
    fig.suptitle(fname)
    for i in range(chs):
        ax = fig.add_subplot(layout, layout, i+1)
        ax.pcolormesh(
               times, freqs, 
                np.abs(dat[i]))
        ax.set_title("Channel "+ str(i+1))
