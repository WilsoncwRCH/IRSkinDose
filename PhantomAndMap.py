
#First import all the relevant functions
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import sys,time


class Phantom:
    ''' Defines Phantom geometry.
    - If Angles are defined, then the  coordinates are outputted 
    - Option to predefine CR or FW (This can improve processing time)'''
    
    def __init__(self, Height, Weight, PrimaryAngle = None, SecondaryAngle = None, CurvatureRadius = None, Flattenedwidth = None):
        self.Height = Height 
        self.Weight = Weight
        self.PrimaryAngle = PrimaryAngle
        self.SecondaryAngle = SecondaryAngle
        self.CurvatureRadius = CurvatureRadius
        self.Flattenedwidth = Flattenedwidth
        if CurvatureRadius is None:
            self.ShapeParameters()
        
        self.PrimaryDisplacement = None
        self.SecondaryDisplacement = None
        self.CentreToBeamEntry = None
        if PrimaryAngle is not None:
            self.SkinCoordinates()
        
     
    def ShapeParameters(self):
        '''Takes Inputted Height/Weight and returns phantom parameters'''
        referenceradius = 12 #10
        referenceheight = 175 #178.6
        referenceweight = 72 #73
        referencewidth = 15 #14.4
 
        CurvatureRadius = referenceradius / np.sqrt(self.Height/referenceheight) * np.sqrt(self.Weight/referenceweight)
        Flattenedwidth  = CurvatureRadius / referenceradius * referencewidth
        self.CurvatureRadius = CurvatureRadius
        self.Flattenedwidth = Flattenedwidth
        
        
    def SkinCoordinates(self):
        '''Uses Primary/Secondary Angles to Generate coordinates on the Phantom'''
        Angle = self.PrimaryAngle
        
        #First ensure correct angle i.e. between -180 and 180 degrees
        if 180 < Angle < 360:
            Angle = Angle - 360
        if -360 < Angle < -180:
            Angle = Angle + 360
       
        #Now get the absolute Angle and convert to radians to save time
        Degrees = abs(Angle) * 3.14159/180
        theta = Degrees
        if Degrees > 3.14159/2:
            theta = 3.14159 - Degrees 
            
        #On the bottom of the phantom.
        edgeofphantom = np.arctan(self.Flattenedwidth / self.CurvatureRadius / 2)
        
        if theta <= edgeofphantom: #if its on the flat
            skindisplacement = self.CurvatureRadius * np.tan(theta)
            skinheight = self.CurvatureRadius * -1
            skinwidth = self.CurvatureRadius * np.tan(theta)
            
        if edgeofphantom < theta <= 3.14159/2 : #if its on the curve
            phi = theta - np.arcsin((self.Flattenedwidth/2 * np.tan(3.14159/2 - theta) *np.sin(3.14159 - theta))/self.CurvatureRadius)
        
            skindisplacement = self.Flattenedwidth/2  + phi * self.CurvatureRadius
            skinheight = self.CurvatureRadius * np.cos(phi) * -1
            skinwidth = self.Flattenedwidth/2 + self.CurvatureRadius * np.sin(phi)
        
        #Now convert back to where on the phantom
        if Degrees > 3.14159/2:
            skinheight = skinheight * -1
            skindisplacement =  self.Flattenedwidth + 3.14159* self.CurvatureRadius - skindisplacement 
        if Angle < 0:
            skindisplacement = skindisplacement * -1
            skinwidth = skinwidth *-1
        
        
        #Now work wiht secondaryangle
        SA = self.SecondaryAngle
        if 85 < SA < 95:
            SA = 85
            print('Some odd angles here???')
        
        IsocentretoSurface = np.sqrt(skinheight**2 + skinwidth**2)
        SecondaryDisplacement = IsocentretoSurface*np.tan(SA * 3.14159/180)
        IsocentretoBeamentry = np.sqrt(IsocentretoSurface**2 + SecondaryDisplacement**2)
        
        self.CentreToBeamEntry = IsocentretoBeamentry
        self.PrimaryDisplacement = skindisplacement
        self.SecondaryDisplacement = SecondaryDisplacement
        

    def __str__(self):
        return f'A Patient of Height {self.Height} cm and Weight {self.Weight} kg. \nDefined by Curve Radius = {round(self.CurvatureRadius,2)}, Flat Width = {round(self.Flattenedwidth,2)}'
    
    
    
    
    
def EmptyHumanskin(Ps,Ss):
        '''Produces an empty dataframe to represent the skin that will be mapped onto.
        Once again returns a dataframe'''
        PRIMARY = np.linspace(-1*Ps,Ps,2*Ps+1)
        SECONDARY = np.linspace(-1*Ss,Ss,2*Ss+1)
        frame = pd.DataFrame(index = PRIMARY, columns=SECONDARY)
        frame = frame.fillna(0)
        return frame
    
    
    

class PatientData:
    
    def __init__(self, df, SDD = 1000, Table = False, BSC = False):
       
        df = df.reset_index()
        #H = df.at[0,'Height']
        #W = df.at[0,'Mass (kg)']
        H = df['Height'].tolist()[0]*100
        W = df['Mass (kg)'].tolist()[0]
        if H < 40 or W < 5:
            H = 175
            W = 72
        self.Height = H
        self.Weight = W
        self.TRP = df['Ref point dose (Gy)'].sum()
        self.TDP = df['DAP (cGy.cm^2)'].sum()
        self.Study = df.at[0,'Study description']
        self.Date = df.at[0, 'Study date']
        self.AccNo = df.at[0, 'Accession number']
        self.Age = df.at[0,'Age']
        self.Sex = df.at[0,'Sex']
        self.Operator = df.at[0,'Operator']
        
        virtualP = Phantom(self.Height, self.Weight, 180, 85)
        self.CurvatureRadius = virtualP.CurvatureRadius
        self.Flattenedwidth = virtualP.Flattenedwidth
        self.SDD = SDD
        self.data = df
        self.SkinRound = [virtualP.PrimaryDisplacement,virtualP.SecondaryDisplacement]
        self.Table = Table
        self.BSC = BSC
        
        self.DoseFrame = None
        self.PeakSkinDose = None
        self.ToSkin()
        
        
    def ToSkin(self):
        
        '''used inside the class, can choose to ignore/not use '''
        
        df = self.data
        
        Ps, Ss = 50,50
        frame = EmptyHumanskin(Ps,Ss)
        RPD = df['Ref point dose (Gy)'].tolist() # these are all self explanatory
        pa = df["Primary angle"].tolist()
        sa = df["Secondary angle"].tolist()
        fs = df['Field size'].tolist() #measured along diagonal
        
        widthoffieldatdetector = [i/np.sqrt(2) for i in fs]
        widthoffieldatRP = [i*60/self.SDD for i in widthoffieldatdetector]
        
        for beam in range(len(RPD)):
            P = Phantom(None, None, pa[beam], sa[beam],self.CurvatureRadius, self.Flattenedwidth)
            
            RPtoSkinSurface = P.CentreToBeamEntry - 15
            Widthoffieldatskin = widthoffieldatRP[beam] * (60 - RPtoSkinSurface)/60
            DosefromRPtoskin = RPD[beam] * (60/(60 - RPtoSkinSurface))**2
            
            PrimaryStart = P.PrimaryDisplacement - Widthoffieldatskin/2
            PrimaryFinish = P.PrimaryDisplacement + Widthoffieldatskin/2
            SecondaryStart = P.SecondaryDisplacement - Widthoffieldatskin/2
            SecondaryFinish = P.SecondaryDisplacement + Widthoffieldatskin/2
        
            for row in np.linspace(-1*Ps,Ps,2*Ps+1): # For each value in primary displacement
                for column in np.linspace(-1*Ss,Ss,2*Ss+1): # for each value in secondary displacement
                
                    if PrimaryStart < row < PrimaryFinish and SecondaryStart < column < SecondaryFinish:
                        currentcellvalue = frame.at[row, column]
                        newcellvalue = currentcellvalue + DosefromRPtoskin
                        frame.at[row,column] = newcellvalue
        
        #note these corrections need cleaning up properly, and have been written as such to be clear and obvious, without              
        if self.BSC ==True:
            for row in np.linspace(-1*Ps,Ps,2*Ps+1):
                for column in np.linspace(-1*Ss,Ss,2*Ss+1):
                    currentcellvalue = frame.at[row, column]
                    newcellvalue = currentcellvalue*1.3
                    frame.at[row,column] = newcellvalue
            
        if self.Table == True:
            for row in np.linspace(-1*Ps,Ps,2*Ps+1):
                for column in np.linspace(-1*Ss,Ss,2*Ss+1):
                    if -2/3 * self.Flattenedwidth  < row < 2 * self.Flattenedwidth / 3:
                        currentcellvalue = frame.at[row, column]
                        newcellvalue = currentcellvalue*0.85
                        frame.at[row,column] = newcellvalue
                        
        
                        
        self.DoseFrame = frame
        self.PeakSkinDose = frame.to_numpy().max()
        
        
    def PlotMap(self, Saved = False, Filetext = None):
        '''
        Parameters
        ----------
        Saved : Saves the Map as a png
            DESCRIPTION. The default is False. 
        Filetext : Name of the saved file
            DESCRIPTION. Default is the Accession number

        Returns
        -------
        None.

        '''
        
        frame = self.DoseFrame
        frame.index = frame.index.map(str)
        frame.columns = frame.columns.map(str)
        
        fig, ax = plt.subplots(figsize = (7,5))
        plt.pcolor(frame)
        plt.xlabel('Secondary displacement / cm')
        plt.ylabel('Primary displacement / cm')
        plt.text(5,15, f'Accession: {self.AccNo}', color = 'white')
        plt.text(5,5, f'PSD = {round(self.PeakSkinDose,2)} Gy', color = 'white')
        ax.set_yticks(np.arange(0.5, len(frame.index), 1), frame.index)
        ax.set_xticks(np.arange(0.5, len(frame.columns), 1), frame.columns)
        
        every_nth = 16 # change this number to edit the number of intervals in the axis
        for n, label in enumerate(ax.yaxis.get_ticklabels()):
            if n % every_nth != 0:
                label.set_visible(False)
        for n, label in enumerate(ax.xaxis.get_ticklabels()):
            if n % every_nth != 0:
                label.set_visible(False)
                
        ax.xaxis.set_ticks_position('none')
        ax.yaxis.set_ticks_position('none')
        plt.colorbar()
        plt.tight_layout()
        if Saved == True:
            text = f'{Filetext}'.jpg if Filetext is not None else f'DoseCheck {self.AccNo}.jpg'
            fig.savefig(text, format = 'jpg', dpi = 250, bbox_inches = 'tight')
        plt.show()
        
        
    def __str__(self):
        return f'Patient {self.AccNo} recieved a peak skin dose of {round(self.PeakSkinDose,2)} Gy'





    
    
    
    

        
