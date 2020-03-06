"""
Created on Fri Feb 21 13:13:52 2020

@author: WILLIAM EGBERT
"""

import os 
import fnmatch
from os.path import join
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mbox
import plotting
import stFFT as stft

errors = [
          "Please enter a valid sample frequency. Must be an integer greater than zero.",
          "Please enter a valid window size. Must be an integer greater than zero." ,
          "Please enter a valid channel number. Must be an integer greater than zero.",
          "Band pass filter is invalid. High threshold must be greater than low threshold",
          "Band pass filter inputs are invalid. Please enter positive number values.",
          "There were no csv files in that directory. Please choose another directory.",
          "User must select a graph type: Pseudocolor and/or 3d",        
        ]

params = [256, 128, 4, 10, 100]

path = None
files = []

def whenSelected():

    if getSelection():
        if pcol.get() or p3d.get():
            if (checkValidInt(sf, 0) and checkValidInt(ws, 1) 
            and checkValidInt(ch, 2) and checkBandPass(hi,lo)) :
                for file in files:
                    freqs, time, data =stft.main(params, file)
#                    print(data.shape)
                    if pcol.get():
                        plotting.plotPColor(data, file, params[2], freqs, time)
                    if p3d.get():
                        plotting.plot3D(data, file, params[2], freqs, time)
        else:
            mbox.showerror("No graph type selected", errors[-1])
    
def chooseDir():
    global path
    path = fd.askdirectory()
    if path:
        fs = []
        for item in os.listdir(path):
            if fnmatch.fnmatch(item, "*.csv"):
                fs.append(item)
            
        populateListbox(fs)
    else:
        print("lmao")
        

def populateListbox(csvs):
    listbox.delete(0, tk.END)
    if len(csvs) == 0:
        listbox.insert(tk.END, errors[-2])
    else:
        for item in csvs:
            listbox.insert(tk.END, item) #insert csv item names to end of list

def checkValidInt(value, ind):
    value = value.get()
    try :
        value = int(value)
        if value <= 0:
            mbox.showerror("Invalid Input", errors[ind])
            return False
        else :
            params[ind] = value
            return True
    except (ValueError, TypeError):
        mbox.showerror("Invalid Input", errors[ind])
        return False
        
def checkBandPass(f1, f2):
    f1 = f1.get()
    f2 = f2.get()
    try :
        f1 = float(f1)
        f2 = float(f2)
        if f1 >= f2:
            mbox.showerror("Invalid band pass frequencies", errors[3])  
            return False
        else :
            params[3] = f1
            params[4] = f2
            return True
    except (ValueError, TypeError):      
        mbox.showerror("Invalid band pass frequencies", errors[4])
        return False

def getSelection():
    global files 
    global path
    files = []
    slct = listbox.curselection()
    for i in slct:
        files.append(join(path, listbox.get(i)))
    if errors[-2] in files:
        chooseDir()
        return False
    else:
        
        return True    

def buildEntries():
    tk.Label(win, text="Sampling Frequency").grid(row = 0, column = 5)
    tk.Label(win, text="Size of STFT window").grid(row = 1, column = 5)
    tk.Label(win, text="Number of Channels").grid(row = 2, column = 5)
    tk.Label(win, text="Band pass Lower Bound").grid(row = 0, column = 7)
    tk.Label(win, text="Band pass Upper Bound").grid(row = 1, column = 7)
    
    sampfreq = tk.Entry(win)
    sampfreq.grid(row=0, column=6, padx = 5)
    sampfreq.insert(0, params[0])
    winsize = tk.Entry(win)
    winsize.grid(row=1, column=6, padx = 5)
    winsize.insert(0, params[1])
    chans = tk.Entry(win)
    chans.grid(row=2, column=6, padx = 5)
    chans.insert(0, params[2])
    hipass = tk.Entry(win)
    hipass.grid(row=0, column= 8, padx = 5)
    hipass.insert(0, params[3]) 
    lopass = tk.Entry(win)
    lopass.grid(row=1, column=8, padx = 5)
    lopass.insert(0, params[4]) 
    
    return (sampfreq, winsize, chans, hipass, lopass)
    
win = tk.Tk()
win.title("Short Time Fourier Transform Visualization Tool")

pcol = tk.BooleanVar()
p3d = tk.BooleanVar()
scrollbar = tk.Scrollbar(win, orient=tk.VERTICAL)
scrollbar.grid(row = 0, column = 4, rowspan = 5, sticky = tk.N + tk.S)

listbox = tk.Listbox(win, height = 10, width = 70, selectmode = tk.MULTIPLE, yscrollcommand=scrollbar.set)
listbox.grid(row = 0, column = 0, rowspan = 5 ,columnspan = 1, sticky = tk.N )

scrollbar.config(command=listbox.yview, width = 20)

onlyfiles = chooseDir()

win.focus_force()
sf, ws, ch, hi, lo =buildEntries()

b1 = tk.Button(win, text = "Do the thing", command = whenSelected).grid(row = 3, 
              column = 5, sticky = tk.S)
b2 = tk.Button(win, text="Choose a different directory", 
               command=chooseDir).grid(row = 4, column = 5, sticky = tk.S)
b3 = tk.Button(win, text="Exit", command=win.destroy).grid(row = 4, column = 6,
             sticky = tk.S)

bpcol = tk.Checkbutton(win, text = "Pseudocolor Plot", variable = pcol, onvalue = True, offvalue = False)
bpcol.grid(row = 3, column = 7, sticky = tk.W)
bpcol.select()
b3d = tk.Checkbutton(win, text = "3d Plot", variable = p3d, onvalue = True, offvalue = False).grid(row = 4, column = 7,
             sticky = tk.W)


tk.mainloop()
