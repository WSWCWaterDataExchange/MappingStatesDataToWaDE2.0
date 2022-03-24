#Date Created: 03/24/2022
#Purpose: To extract WY methods use information and populate dataframe for WaDE_QA 2.0.
#Notes: 1) Two different data sets, groundwater vs surface water.


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd


# Inputs
############################################################################
print("Reading inputs...")
workingDir = "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/Wyoming/WaterAllocation"
os.chdir(workingDir)

#WaDE columns
columnslist = [
    "MethodUUID",
    "ApplicableResourceTypeCV",
    "DataConfidenceValue",
    "DataCoverageValue",
    "DataQualityValueCV",
    "MethodDescription",
    "MethodName",
    "MethodNEMILink",
    "MethodTypeCV"]


# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe...")
inpVals = [
    "WYwr_M1",
    "Surface Ground Water",
    "",
    "",
    "",
    # "Water allocations points of diversions for surface water springs and ground water wells.",
    """Type
    File Geodatabase Feature Class
    
    Tags
    Water, State of Wyoming, Water Development Office, Wells, e-Permit.
    
    Summary
    This dataset provides the Wyoming Water Development Office a statewide dataset of water right locations for groundwater wells.   April, 2020. GCS_North_American_1983. 1:24,000.
    
    Description
    These data represent ground water wells with greater than 500 gallons per minute (GPM) permitted capacity, and which do not have stock watering or coalbed methane as their only beneficial use. All data are sourced from the Wyoming State Engineer's Office (SEO), e-Permit download of 03/02/2019.
    These data may be linked to other water rights-based datasets, including SEO water rights data and Wyoming Water Development Office (WDO) place of use (POU) feature classes, via attribute WR_Number. 
    
    Credits
    Created by Confluence Consulting Inc of Bozeman, Montana.
    Wyoming State Engineer's Office, e-permit download data.
    
    Use limitations
    These GIS data were compiled from Wyoming Water Development Commission (WWDC) funded projects, Wyoming State Engineer’s Office (SEO) records, and/or other sources for the use and convenience of the public.  These data may not be complete or accurately represent the conditions  on the ground, and no decision involving a risk of economic loss or physical injury should be made in reliance thereon. The WWDC and the Water Resources Data System (WRDS) do not endorse or recommend the use of these data for any other purpose than originally developed and are providing these data "as is," and disclaim any and all warranties, whether expressed or implied, including (without limitation) any implied warranties of merchantability or fitness for a particular purpose. Users of this information assume the entire risk to the use of these data and should review or consult the primary data and information sources to ascertain the reliability or usability of the information. Comprehensive water rights information is only available through researching the water rights on file with the SEO and Board of Control. The State of Wyoming and its agencies assume no liability associated with the use or misuse of this information and specifically retain sovereign immunity and all defenses available to them by law.  
    
    Extent
    West   -111.044988      East  -104.049287 
    North   44.996573      South  41.002113 
    
    Scale Range
    Maximum (zoomed in)   1:5,000 
    Minimum (zoomed out)   1:625,000 """,
    "Adjudicated",
    "http://library.wrds.uwyo.edu/wrp/90-17/",
    "Adjudicated"]

outdf = pd.DataFrame([inpVals], columns=columnslist)


# Check required fields are not null
############################################################################
print("Check required is not null...")
#Check all 'required' (not NA) columns have value (not empty). Replace blank strings by NaN, if there are any
outdf = outdf.replace('', np.nan)
outdf_nullMand = outdf.loc[(outdf["MethodUUID"].isnull()) | (outdf["MethodUUID"] == '') |
                           (outdf["MethodName"].isnull()) | (outdf["MethodName"] == '') |
                           (outdf["MethodDescription"].isnull()) | (outdf["MethodDescription"] == '') |
                           (outdf["ApplicableResourceTypeCV"].isnull()) | (outdf["ApplicableResourceTypeCV"] == '') |
                           (outdf["MethodTypeCV"].isnull()) | (outdf["MethodTypeCV"] == '')]


# Export to new csv
############################################################################
print("Exporting dataframe to csv...")

# The working output DataFrame for WaDE 2.0 input.
outdf.to_csv('ProcessedInputData/methods.csv', index=False)

# Report purged values.
if(len(outdf_nullMand.index) > 0):
    outdf_nullMand.to_csv('ProcessedInputData/methods_mandatoryFieldMissing.csv', index=False)

print("Done.")
