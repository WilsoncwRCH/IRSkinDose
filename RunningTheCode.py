# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 10:53:43 2023

@author: Wilsoncw
"""
#First import all the relevant functions
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import sys,time

#Then import my prewritten classes
import PhantomAndMap
from PhantomAndMap import Phantom, PatientData


class RunTheProgram:
    '''
    Reads File from Defined location and converts to a dataset
    Then Can process Individualsdata for a given Accession Number
    Or Can Run through an entiredata
    '''
    def __init__(self, file):
        self.file = file
        self.Dataframe = None
        self.XLSXtoDATAFRAME()
      
        
    def XLSXtoDATAFRAME(self):
        '''TAKE the unedited XLSX FILE AND COMBINE ALL OUTPUTS
        then returns it in the form of a pandas dataframe'''
        file = self.file
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
        df["Primary angle"] = df["Primary angle"].fillna(0)
        df["Secondary angle"] = df["Secondary angle"].fillna(0)
        self.Dataframe = df
        return
    
    
    def IndividualsData(self, AccessionNumber, SDD = 1000, Saved = False, Filetext = None):
        '''Processes Data for Individual Patient'''
        
        self.AccNo = AccessionNumber
        '''AccessionNumber Must take the form of a list'''
        
        SourceData = self.Dataframe
        df = SourceData.loc[SourceData['Accession number'].isin(AccessionNumber)]
        
        PData = PatientData(df, SDD)
        UPdata = PatientData(df, SDD +150)
        DNdata = PatientData(df, SDD -150)
        
        MSD = PData.PeakSkinDose
        uperr = PData.PeakSkinDose - UPdata.PeakSkinDose
        downerr = DNdata.PeakSkinDose - PData.PeakSkinDose
        uncertainty = round((max(uperr,downerr)), 4)
        Uncertaintystring = f'PSD = {round(MSD, 3)} Gy'
        if uncertainty > 0.002:
            Uncertaintystring = f'PSD = {round(MSD, 3)} \u00B1 {uncertainty} Gy'
        
        PData.PlotMap(Saved, Filetext = None)
        print(Uncertaintystring)
        PData.String = Uncertaintystring
        
        return PData
    
    
    def EntireDataset(self, SDD = 1000, Saved = False):
        
        SourceData = self.Dataframe
        AccessionNumbers = SourceData['Accession number'].unique()
        
        Date, StudyDesc, PeakSkinDose, TotalRP, TotalDAP, Age, Sex, Height, Weight, Uncertainty, operator = [],[],[],[],[],[],[],[],[],[],[]
        print('This may take a while. Cycle Starting...')
        starttime= time.time()
        for i in range(len(AccessionNumbers)):
            df = SourceData.loc[SourceData['Accession number'] == AccessionNumbers[i]]
        
            PData = PatientData(df, SDD)
            uperr = PData.PeakSkinDose - PatientData(df, SDD +150).PeakSkinDose 
            downerr = PatientData(df, SDD -150).PeakSkinDose - PData.PeakSkinDose
            uncertainty = round((max(uperr,downerr)), 4)
            
            Date.append(PData.Date)
            StudyDesc.append(PData.Study)
            PeakSkinDose.append(PData.PeakSkinDose)
            TotalRP.append(PData.TRP)
            TotalDAP.append(PData.TDP)
            Age.append(PData.Age)
            Sex.append(PData.Sex)
            Height.append(PData.Height)
            Weight.append(PData.Weight)
            operator.append(PData.Operator)
            Uncertainty.append(uncertainty)
            
            if PData.PeakSkinDose > 1.5:
                PData.PlotMap(Saved)
            
            if i % 18==0:
                print(f'Progress at {round((i+1)*100/len(AccessionNumbers),1)}%')
        endtimer = time.time()
        
        print(f'Progressed to {100}% Completed!')
        print(f'Total time = {(endtimer - starttime)/60} min')
        PROCESSED = pd.DataFrame(list(zip(Date, AccessionNumbers, operator, StudyDesc, Age, Sex, Height, Weight, TotalRP, TotalDAP, PeakSkinDose, Uncertainty)),
                                 columns = ['Date', 'Accession number', 'Operator', 'Study description', 'Age', 'Sex', 'Height', 'Weight', 'RPdose', 'DAP', 'PSD', 'unc'])
        self.TableofResults = PROCESSED
        return PROCESSED

    def __str__(self):
        return f'This module returns a pandas dataset (use .Dataframe) \nYou can then process this dataframe for an individual Accession or over the entire dataset '        
        
        
        
        