'''Step 1 is to import all the functions we need'''
#First import all the relevant functions
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import sys,time

#Then import my prewritten classes
from RunningTheCode import RunTheProgram
from PhantomAndMap import Phantom, PatientData


#%%
'''Choose a file to use. e.g. TestDataset'''

TestDataset = 'TestDataset.xlsx'

#We can extract the datafrom this file using
UseTestdata = RunTheProgram(TestDataset)

#This returns a message telling you how to use its value
print(UseTestdata)

#%%
#The test data can be returned as a dataframe using:
df = UseTestdata.Dataframe
print('The dataframe appears as follows: \n' , df)
#%%
''' Now lets take a look at our phantom'''

#First lets define a phantom of 170 cm tall and 70kg
P = Phantom(170, 70)

#This has calculates a couple of important values
CR = P.CurvatureRadius
FW = P.Flattenedwidth
print(f'Curve radius = {CR}, Flat Width = {FW}')

#%%
#Now if we look at the phantom from certain angles we can define coordinates on the patient
P2 = Phantom(180, 90, 45, 10)

#Now, as well as CR and FW,  we can extract
PrDisp = P2.PrimaryDisplacement
ScDisp = P2.SecondaryDisplacement
ICB = P2.CentreToBeamEntry
print(f'Primary Displacement = {PrDisp} \nSecondary Displacement = {ScDisp} \nDistance from isocentre to point on skin where beam hits the patient {ICB}')

#Note we can predefine CR and FW and return the function anyway.

#%%
''' Lets map data onto our Phantom using PatientData '''
#We already imported a Test Dataset
#The test data can be returned as a dataframe using:
sourcedata = UseTestdata.Dataframe
print('The source appears as follows: \n' , sourcedata)

#Lets extract just one patients data from the set
AccessionNumber = ['REFNu1']
df = sourcedata.loc[sourcedata['Accession number'].isin(AccessionNumber)]
print('The Patient Data appears as follows: \n' , df)

#%%
#we can discover a lot about the patient using Patient Data
Patient = PatientData(df)
print(Patient)


#%%
#For example:
print(f'The study was a {Patient.Study}, performed on {Patient.Date} \nThe Patient was {Patient.Age} years old , and of sex {Patient.Sex}')

#%%
#we can even view the dose applied to the patient
Patient.PlotMap()

#%%
'''If we want to process the entire dataset we can use'''

entiredataframe = UseTestdata.EntireDataset()
print(entiredataframe)





