# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 12:00:47 2023

@author: Wilsoncw
"""

#First import all the relevant functions
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import sys,time

def XLSXtoDATAFRAME(file):
    '''TAKE the unedited XLSX FILE AND COMBINE ALL OUTPUTS
    then returns it in the form of a pandas dataframe'''
    xl = pd.ExcelFile(file)
    res = len(xl.sheet_names)
    y = np.linspace(2,res-1,res-2)
    y = [int(i) for i in y]
    df = pd.concat(pd.read_excel(file,sheet_name=y))
    df['Accession number'] = df['Accession number'].map(str)
    df = df.sort_values(by = ['Accession number'])
    df['Height'] = df['Height'].fillna(1.786)
    df['Mass (kg)'] = df['Mass (kg)'].fillna(73)
    df['Height'].replace(0, 1.786)
    df['Mass (kg)'].replace(0, 73)
    return df

def GetConversionValues(File):
    xl = pd.read_csv(File, header = 0, index_col = 0)
    #xl = xl.set_index('Primary Angle')
    return xl

def UseConversionValues(PA, Type, kV):
    #First lets sort out the Angle
    PossibleAngles = [0,30,60,90,135,180]
    
    p = abs(PA)
    if 180 < p < 360:
        p = p - 180
    PrimaryAngle = 0
    for i in range(len(PossibleAngles)):
        if PossibleAngles[i] < p:
            PrimaryAngle = PossibleAngles[i]
            
    PossiblekVs = [70, 80, 100, 125]       
    #Now sort out The Dose
    ThekVp = 70
    for i in range(len(PossiblekVs)):
        if PossiblekVs[i] < kV:
            ThekVp = PossiblekVs[i]
    
    if Type == 'Fluoroscopy':
        letterstring = f'F {ThekVp}'
    else:
        letterstring = f'A {ThekVp}'
    
    return PrimaryAngle, letterstring

def CalculateDose(df, conversionvals):
    RPD = df['Ref point dose (Gy)'].tolist()
    PrimAngle = df['Primary angle'].tolist()
    Type = df['Type'].tolist()
    kV = df['kVp'].tolist()
    
    if len(RPD) != len(PrimAngle) and len(Type) != len(kV):
        print('something fishy yuck')
        
    dose = 0   
    for event in range(len(RPD)):
        pa, strings = UseConversionValues(PrimAngle[event],Type[event],kV[event])
        individualdose = conversionvals.at[pa, strings] *RPD[event]
        dose = individualdose + dose
        #formatteddose = f'{round(dose,3)*1000} mGy'
    return dose

def loopcalc(df, conversionvals):
    df['Accession number'] = df['Accession number'].map(str)
    df = df.sort_values(by=['Accession number'])
    df["Primary angle"] = df["Primary angle"].fillna(0)
    df['Ref point dose (Gy)'] = df['Ref point dose (Gy)'].fillna(0)
    df['Type'] = df['Type'].fillna(0)
    df['kVp'] =df['kVp'].fillna(0)
    AccessionNumbers = df['Accession number'].unique()
    print('Starting Cycle...')
    Age, PatientID, Studydesc, station, date, RPdose, dose = [],[],[],[],[],[],[]
    for i in range(len(AccessionNumbers)):
        dF = df.loc[df['Accession number'] == AccessionNumbers[i]]
        Age.append(dF['Age'].mean())
        RPdose.append(dF['A Dose RP total (Gy)'].iloc[1])
        PatientID.append(dF['Patient ID'].iloc[1])
        Studydesc.append(dF['Study description'].iloc[1])
        station.append(dF['Station name'].iloc[1])
        date.append(dF['Study date'].iloc[1])
        dose.append(CalculateDose(dF, conversionvals))
        if i % 10==0:
            print(f'Progress at {round((i+1)*100/len(AccessionNumbers),1)}%')
    Dataframe = pd.DataFrame(list(zip(AccessionNumbers,PatientID, date, station, RPdose, Studydesc, Age, dose)), columns = ['Accession No', 'Patient', 'Date', 'Room', 'RP dose', 'Study', 'Age', 'Est Uterus dose / Gy'])
    
    return Dataframe



ConversionValues = GetConversionValues('LiverFocusConversionTable.csv')
file = 'Testdata.xlsx'
df = XLSXtoDATAFRAME(file)

DF = loopcalc(df, ConversionValues)
print(DF)
#DF.to_csv('Outputs(Liver).csv', encoding='utf-8', index=False)


        
