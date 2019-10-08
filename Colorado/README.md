# DataMigrationScripts
Python codes to prepare inputs for the WaDE database in csv format. The codes take data on States water rights such as DWR_Water_Right_-_Net_Amounts.csv for Colorado as inputs 
and generate csv files for water allocations, site specific information, variable names, etc.

# Python source codes in this directory: 
1. sites.py: reads the water rights file (DWR_Water_Right_-_Net_Amounts.csv) and writes out the fields for the sistes.csv file
2. methods.py, variables.py, watersources.py: ditto for methods.csv, variables.csv, and watersources.csv respectively.
3. waterallocations_par.py: runs in parllel (mpi4py) to ouput waterallocations.csv.
4. beneficialUseDictionary.py: It holds mapping rule between beneficial use ID and beneficial use category. 
This is used in waterallocations_par.py code to map 'decreed uses' in DWR_Water_Right_-_Net_Amounts.csv to corresponding beneficial use categories.

# Dependencies (Required packages/libraries):
pandas 

numpy

mpi4py 

MPI library (for mpi4py): For windows use Microsoft MPI from https://docs.microsoft.com/en-us/message-passing-interface/microsoft-mpi

# To run the codes
Before running the code, inside the source file, specify the working drectory, where the input and output csv files are located.

The sites.py, methods.py, variables.py, and watersources.py can be run from python commond line or windows command line, 
e.g., to run methods.py:
python methods.py

To run waterallocations_par.py: 

1. Make sure to install MPI package. 

2. From the command line call 

mpiexec -n num_procs python waterallocations_par.py

where num_procs is the number of processes 

# Sample files
NewColoradoDataFiles.zip contains csv files prepared using these scripts. 




