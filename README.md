# IRSkinDose
A simple software to perform Peak Skin Dose calculations for Interventional Radiology. Using the .xlsx export from OpenREM's Fluoroscopy.
Can be used to generate a dosemap for an individual patient, or to review an entire exported dataset.

This should be simple to read and easy to manipulate to your choosing. All imports should be included as standard with your python 3+. 

## Explanation
Comprised of a simple phantom designed as a circle of 12 cm radius split in half and glued to a rectangle of width 15 cm. 
The centre of the phantom is defined as the Isocentre.
![image](https://github.com/WilsoncwRCH/IRSkinDose/assets/144329591/ce5ce95a-37be-4043-9671-cf31709f5c4a)

## Brief Overview of the code
```python
import pandas as pd
from RunningTheCode import RunTheProgram
from PhantomAndMap import Phantom, PatientData

#Define the location of the OpenREM export
TestDataset = 'TestDataset.xlsx'

''' We have a simple Phantom model '''
#return Phantom parameters based on Patient size
Height = 170 #cm
Weight = 70 #kg
P = Phantom(Height, Weight)
CR = P.CurvatureRadius
FW = P.Flattenedwidth

#Can also get co-ordinates of the beam on the phantom if we include Primary and Secondary Angles
P2 = Phantom(Height, Weight, PrimaryAngle = 30, SecondaryAngle = 10)
PrDisp = P2.PrimaryDisplacement
ScDisp = P2.SecondaryDisplacement
ICB = P2.CentreToBeamEntry

'''We can use the Phantom as we please depending on how we manipulate the dataset'''
#We can first get the data from out file using RunTheProgram.Dataframe
UseTestdata = RunTheProgram(TestDataset)
SourceData = UsetTestdata.Dataframe #we can simply use the pandas dataframe on the phantom, or this is mostlly done for you.

#Lets use one patients
AccessionNumber = ['REFNu1']
PData = UseTestdata.IndividualsData(AccessionNumber) # pdata contains loads of information about the patient.

#Or we can review the entire file and export 
EntireSet = UseTestdata.Entiredataset() #EntireSet is a dataframe containing PSD estimates for every accession in the book
```





  
