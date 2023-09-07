# IRSkinDose
A simple software to perform Peak Skin Dose calculations for Interventional Radiology. Using the .xlsx export from OpenREM's Fluoroscopy.
Can be used to generate a dosemap for an individual patient, or to review an entire exported dataset.

This should be simple to read and easy to manipulate to your choosing. All imports should be included as standard with your python 3+. 

#
Comprised of a simple phantom designed as a circle of 12 cm radius split in half and glued to a rectangle of width 15 cm. 
The centre of the phantom is defined as the Isocentre.

```python
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
UseTestdata = RunTheProgram(TestDataset)
The


```





  
