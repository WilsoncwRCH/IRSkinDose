
#First import all the relevant functions
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import sys,time

#Import My own functions:
from RunningTheCode import RunTheProgram

#Can also import tkinter and PIL for image and GUI options
from tkinter import messagebox, ttk
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import re
import os


'''
Now to build the App
'''

def openFile():
    #opens files and allows you to search for the export you want to use
    tf = filedialog.askopenfilename(
        initialdir = "C",
        title = "Select file",
        filetypes = [('Excel file', "*.xlsx"),('Csv file', "#.csv")])
    pathh.insert(END, tf)
    ft = tf[::-1]
    fft = ft.partition('/')[0]
    name = fft[::-1]
    filename = tf
    
def getaccess():
    ACC = AccessionNo.get()
    return ACC

def IndividualExam():
    ac = AccessionNo.get()
    accession = re.split(r"and|[\s,-]+" , ac)
    filename = pathh.get()
    file = f'{filename}'
    PatientData = RunTheProgram(file).IndividualsData(accession, GreaterAccuracy=True)
    PatientData.ToSkin()
    result.set(PatientData.String)
    
def ExportEntiredataset():
    filename = pathh.get()
    file = f'{filename}'
    result.set('The file is being processed, this may take a while')
    Dataset = RunTheProgram(file).EntireDataset()
    file2 = file[0:-5]
    export = f'{file2} processed.csv'
    Dataset.to_csv(export, encoding='utf-8', index=False )
    result.set('Export has been saved in original file location')
    
       
    
'''Define the Window'''  
ws = Tk()
ws.title('Skin Dose Calculator')
ws.geometry("450x250")
ws['bg'] = 'DodgerBlue4'


Label1 = Label(ws, text="First Select a File. Then input any Accession Numbers.")
Label1.place(relx = .5, rely = .2, anchor = CENTER)

'''Accession Number talk'''
AccessionNo = Entry(ws, width= 35)
AccessionNo.place(relx= .3, rely= .5, anchor= CENTER)
Button(ws, text= "Confirm Accession No./s", command= getaccess).place(relx= .95, rely= .5, anchor= E)    

'''Select The File'''
pathh = Entry(ws, width= 35)
pathh.place(relx= .3, rely= .38, anchor= CENTER)
Button(ws,
       text = 'Select File',
       command=openFile).place(relx= .95, rely= .38, anchor= E)

'''Individual Patient'''
Button(ws, text= "IndividualPatient", command= IndividualExam).place(relx= .2, rely= .75, anchor= W)
Button(ws, text= "ExportProcesseddataset", command= ExportEntiredataset).place(relx= .8, rely= .75, anchor= E)

result = StringVar()
result.set('Peak Skin Dose Appears here...')
resultbar = Entry(textvariable = result, state = DISABLED, width= 50, justify= CENTER)
resultbar.place(relx = .5, rely = .9, anchor = CENTER)


ws.mainloop()

    
