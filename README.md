# Required setup - need to do this once and a web connection is required:

1. Open a terminal window

2. From the command line: Create a directory and clone the public github repository https://github.com/donsweeney4/UHI-data into the directory

3. From the command line: pip install -r requirements.txt --> this will install all the python packages necessary

# When new data is collected or earlier data is re-evaluated:

1. Go to the directory created for the cloned repository - let's refer to this as the top directory.
2. Create a subdiretory with a name like 'InputData_Sept3' But you can name it anything you want.
3. Put each sensor unit raw data with a file of name like 'Unit1_dataLog000nn.TXT' The .TXT extension is required.
   The part 'dataLog000nn.TXT' is the form of the default downloaded file from the ODL. You need to add the unit number. This is not required but is good practice.
4. Copy and paste the file 'parameters.py' into the subdirectory with the input data
5. Edit the file 'parameters.py' as described below.
6. From the top directory run the python script: python ProcessEachRouteWithColorMap.py <name of directory from step 2 above>
7. The final results are placed in a directory specified in the parameters.py file.

# The file 'parameters.py'

Each directory with the sensor units input data (from step 2) needs a parameters.py file. The main code has a number of options and parameters that are unique for each data run. All of the unique values are in this file. Use any editor to edit the file.

# Notes

1. I used python 3.11.0. Earlier versions of python 3 will likely work too. I assume you have python and pip installed.
2. The data processing code will run without a web connection but if you want the stationary sensor temperature values you need a web connection
3. The process on macOS or windows for creating directories, setting file permissions, editing files, etc is up to you.
4. The primary python script to pre-process the input data is: ProcessEachRouteWithColorMap.py
5. The input data downloaded from the OpenDataLogger (ODL) have an extension .TXT. All the files placed in the subdirectory (step 2) with this extension are pre-processed and appended as the pre-processed output data.
6. I did not use a virtual environment
