# IRSkinDose
A simple software to perform Peak Skin Dose calculations for Interventional Radiology. Using the .xlsx export from OpenREM's Fluoroscopy.
Can be used to generate a dosemap for an individual patient, or to review an entire exported dataset.

This should be simple to read and easy to manipulate to your choosing. All imports should be included as standard with your python 3+. 

## Explanation of whats happening
Comprised of a simple phantom designed as a circle of 12 cm radius split in half and glued to a rectangle of width 15 cm. 
The centre of the phantom is defined as the Isocentre. Data from an OpenREM export should explain the 

![Briefexp](https://github.com/WilsoncwRCH/IRSkinDose/assets/144329591/e8827087-26f3-4cd6-a752-283e121b43af)

## Brief Overview of the code
For a full example go to the example walkthrough notebook

```python
from RunningTheCode import RunTheProgram

'''Get The Data'''
#Define the location of the OpenREM export
TestDataset = 'TestDataset.xlsx'

#We can first get the data from out file using RunTheProgram.Dataframe
UseTestdata = RunTheProgram(TestDataset)
SourceData = UsetTestdata.Dataframe  #A pandas dataframe containing all the relevant information from the .xlsx


'''We can use the Data as we please depending on what we want to do'''
AccessionNumber = ['REFNu1'] #Patients identifier
PData = UseTestdata.IndividualsData(AccessionNumber) #Plots a map of skin dose and returns object Pdata, which contains loads of information about the patient.

#Or we can review the entire file and export 
EntireSet = UseTestdata.Entiredataset() #EntireSet is a dataframe containing PSD estimates for every different accession in the .xlsx file
```





  
