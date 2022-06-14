# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 13:13:52 2020

@author: William Egbert
"""
from scipy.signal import stft 
import numpy as np
import mne

from pandas import read_csv as csv



def main (params, file):
    data = importCSV(file)
    data = bandPass(data, params[0], params[2], params[3], params[4])
    freqs, time, data = stFourierTrans(data, params[0], params[1])
    return (freqs, time, data)
    
def importCSV(file):
    data = csv(file, header=None)
    data = data.fillna(value=0).transpose().to_numpy()
    print(data.shape)
    return data

def bandPass(dat, sf, ch, lo, hi):
    filtered = mne.filter.filter_data(dat[0:ch], 
        sf, l_freq=lo, h_freq = hi, verbose = False)
    return filtered

def stFourierTrans(dat, sf, ws):
    bins, times, fts = stft(dat, sf, nperseg = ws)
    return (bins, times, fts)

