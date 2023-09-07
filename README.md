# IRSkinDose
A simple software to perform Peak Skin Dose calculations for Interventional Radiology. Using the .xlsx export from OpenREM's Fluoroscopy.
Can be used to generate a dosemap for an individual patient, or to review an entire exported dataset.

This should be simple to read and easy to manipulate to your choosing. All imports should be included as standard with your python 3+. 

### What this includes
- Python classes: Phantom, Patientdata and RunTheProgram. (Can be used to calculate Peak Skin Dose for one patient, the same patient who experienced multiple studies, or an entire database of patients)
- Application: A basic GUI has also been created that can be used if you want to build a desktop usable version (see instructions below).
- Foetal dose calculation: A rough work in progress that can assess foetal dose for exams focused on the Uterus or 


## Explanation of whats happening
Comprised of a simple phantom designed as a circle of 12 cm radius split in half and glued to a rectangle of width 15 cm. 
The centre of the phantom is defined as the Isocentre. Data is mapped onto this phantom and returned as a 2D image, dataframe and much more...

![Briefexp](https://github.com/WilsoncwRCH/IRSkinDose/assets/144329591/e8827087-26f3-4cd6-a752-283e121b43af)


## A Brief Overview of the code
For a full example/instructions go to the example walkthrough notebook

```python
'''This is just an overview of the most powerful functions'''
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

## Application Instructions
To see how the app works, run the code for BuildintoApplication.py.
It's self explanatory, 
1. Select the .xlsx export you want to review.
2. Add any individuals accession numbers (can be multiple if you want to sum exams).
3. Press IndividualPatient to view said patients skindosemap and also their PSD.
4. Press ExportProcessedData to calculate PSDs for all patients in the .xlsx export and return a .csv file
 
To build into a desktop application / executable, use pyinstaller (pip install pyinstaller) and follow the instructions online

#
best of luck!




  
