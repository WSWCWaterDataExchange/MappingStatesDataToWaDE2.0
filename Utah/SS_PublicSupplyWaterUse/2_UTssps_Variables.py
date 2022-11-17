# Last Updated: 11/15/2022
# Purpose: To create UT site specific public supply variable use information and populate dataframe for WaDE_QA 2.0.
# Notes: 1) Used a list approach.  Needed to have five rows for VaribleCVs.


# Needed Libraries
############################################################################
import os
import numpy as np
import pandas as pd


# Inputs
############################################################################
print("Reading inputs...")
workingDir = "G:/Shared drives/WaDE Data/Utah/SS_PublicSupplyWaterUse"
os.chdir(workingDir)

#WaDE columns
columnslist = [
    "VariableSpecificUUID",
    "AggregationInterval",
    "AggregationIntervalUnitCV",
    "AggregationStatisticCV",
    "AmountUnitCV",
    "MaximumAmountUnitCV",
    "ReportYearStartMonth",
    "ReportYearTypeCV",
    "VariableCV",
    "VariableSpecificCV"]


# Custom Site Functions
############################################################################

#WaterSourceUUID
def assignVariableSpecificUUID(colrowValue):
    string1 = str(colrowValue)
    outstring = "UTssps_V" + string1
    return outstring

# Creating output dataframe (outdf)
############################################################################
print("Populating dataframe...")
outdf = pd.DataFrame(columns=columnslist)
# outdf = outdf.append(pd.Series(), ignore_index = True)  # This approach requires a blank row to be appended into the outbound dataframe.

outdf.VariableCV = [
"Delivered Water Use",
"Delivered Water Use",
"Delivered Water Use",
"Delivered Water Use",
"Delivered Water Use",
"Delivered Water Use",
"Delivered Water Use",
"Delivered Water Use",
"Delivered Water Use",
"Delivered Water Use",
"Delivered Water Use",
"Delivered Water Use",
"Delivered Water Use",
"Delivered Water Use",
"Delivered Water Use",
"Delivered Water Use",
"Delivered Water Use",
"Return",
"Return",
"Return",
"Return",
"Return",
"Return",
"Return",
"Return",
"Return",
"Return",
"Return",
"Return",
"Return",
"Return",
"Return",
"Return",
"Transfer In",
"Transfer In",
"Transfer In",
"Transfer In",
"Transfer In",
"Transfer In",
"Transfer In",
"Transfer In",
"Transfer In",
"Transfer In",
"Transfer In",
"Transfer In",
"Transfer In",
"Transfer In",
"Transfer In",
"Transfer In",
"Transfer In",
"Transfer In",
"Transfer In",
"Transfer In",
"Transfer In",
"Transfer In",
"Transfer In",
"Transfer In",
"Transfer In",
"Transfer In",
"Transfer In",
"Transfer Out",
"Transfer Out",
"Transfer Out",
"Transfer Out",
"Transfer Out",
"Transfer Out",
"Transfer Out",
"Transfer Out",
"Transfer Out",
"Transfer Out",
"Transfer Out",
"Transfer Out",
"Transfer Out",
"Transfer Out",
"Transfer Out",
"Transfer Out",
"Transfer Out",
"Transfer Out",
"Transfer Out",
"Transfer Out",
"Transfer Out",
"Transfer Out",
"Transfer Out",
"Transfer Out",
"Transfer Out",
"Transfer Out",
"Transfer Out",
"Transfer Out",
"Transfer Out",
"Transfer Out",
"Transfer Out",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal",
"Withdrawal"]

outdf.VariableSpecificCV = ["Delivered Water Use_Annual_Commercial_Unspecified",
"Delivered Water Use_Annual_DCII_Unspecified",
"Delivered Water Use_Annual_Domestic_Unspecified",
"Delivered Water Use_Annual_Industrial_Unspecified",
"Delivered Water Use_Annual_Institutional_Unspecified",
"Delivery_Annual_Industrial_Groundwater",
"Delivery_Annual_Water Supplier_Groundwater",
"Delivery_Annual_Water Supplier_Surface Water",
"Delivery_Annual_Water Supplier_Unspecified",
"Delivery_Monthly_Agricultural_Groundwater",
"Delivery_Monthly_Commercial_Groundwater",
"Delivery_Monthly_Domestic_Groundwater",
"Delivery_Monthly_Domestic_Unspecified",
"Delivery_Monthly_Industrial_Groundwater",
"Delivery_Monthly_Irrigation_Surface Water",
"Delivery_Monthly_Water Supplier_Groundwater",
"Delivery_Monthly_Water Supplier_Surface Water",
"Return_Annual_Agricultural_Unspecified",
"Return_Annual_Commercial_Surface Water",
"Return_Annual_Geothermal_Groundwater",
"Return_Annual_Industrial_Groundwater",
"Return_Annual_Industrial_Surface Water",
"Return_Annual_Power (Geothermal)_Groundwater",
"Return_Monthly_Agricultural_Surface Water",
"Return_Monthly_Agricultural_Unspecified",
"Return_Monthly_Geothermal_Groundwater",
"Return_Monthly_Industrial_Groundwater",
"Return_Monthly_Industrial_Surface Water",
"Return_Monthly_Irrigation_Surface Water",
"Return_Monthly_Power (Geothermal)_Groundwater",
"Return_Monthly_Power (Geothermal)_Unspecified",
"Return_Monthly_Power (Hydro-Elec)_Surface Water",
"Return_Monthly_Water Supplier_Surface Water",
"Transfer In_Annual_Commercial_Surface Water",
"Transfer In_Annual_Commercial_Unspecified",
"Transfer In_Annual_Domestic_Unspecified",
"Transfer In_Annual_Industrial_Groundwater",
"Transfer In_Annual_Industrial_Unspecified",
"Transfer In_Annual_Irrigation_Groundwater",
"Transfer In_Annual_Irrigation_Surface Water",
"Transfer In_Annual_Irrigation_Unspecified",
"Transfer In_Annual_Mining_Groundwater",
"Transfer In_Annual_Water Supplier_Groundwater",
"Transfer In_Annual_Water Supplier_Surface Water",
"Transfer In_Annual_Water Supplier_Unspecified",
"Transfer In_Monthly_Agricultural_Unspecified",
"Transfer In_Monthly_Commercial_Surface Water",
"Transfer In_Monthly_Commercial_Unspecified",
"Transfer In_Monthly_Domestic_Groundwater",
"Transfer In_Monthly_Domestic_Unspecified",
"Transfer In_Monthly_Industrial_Groundwater",
"Transfer In_Monthly_Industrial_Unspecified",
"Transfer In_Monthly_Irrigation_Groundwater",
"Transfer In_Monthly_Irrigation_Surface Water",
"Transfer In_Monthly_Irrigation_Unspecified",
"Transfer In_Monthly_Mining_Groundwater",
"Transfer In_Monthly_Power (Fossil-Fuel)_Groundwater",
"Transfer In_Monthly_Water Supplier_Groundwater",
"Transfer In_Monthly_Water Supplier_Surface Water",
"Transfer In_Monthly_Water Supplier_Unspecified",
"Transfer Out_Annual_Agricultural_Surface Water",
"Transfer Out_Annual_Agricultural_Unspecified",
"Transfer Out_Annual_Commercial_Surface Water",
"Transfer Out_Annual_Commercial_Unspecified",
"Transfer Out_Annual_Domestic_Unspecified",
"Transfer Out_Annual_Industrial_Groundwater",
"Transfer Out_Annual_Industrial_Unspecified",
"Transfer Out_Annual_Irrigation_Groundwater",
"Transfer Out_Annual_Irrigation_Surface Water",
"Transfer Out_Annual_Irrigation_Unspecified",
"Transfer Out_Annual_Power (Fossil-Fuel)_Groundwater",
"Transfer Out_Annual_Water Supplier_Groundwater",
"Transfer Out_Annual_Water Supplier_Surface Water",
"Transfer Out_Annual_Water Supplier_Unspecified",
"Transfer Out_Monthly_Agricultural_Surface Water",
"Transfer Out_Monthly_Commercial_Groundwater",
"Transfer Out_Monthly_Commercial_Surface Water",
"Transfer Out_Monthly_Commercial_Unspecified",
"Transfer Out_Monthly_Domestic_Groundwater",
"Transfer Out_Monthly_Domestic_Unspecified",
"Transfer Out_Monthly_Industrial_Groundwater",
"Transfer Out_Monthly_Industrial_Surface Water",
"Transfer Out_Monthly_Industrial_Unspecified",
"Transfer Out_Monthly_Irrigation_Groundwater",
"Transfer Out_Monthly_Irrigation_Surface Water",
"Transfer Out_Monthly_Irrigation_Unspecified",
"Transfer Out_Monthly_Power (Fossil-Fuel)_Groundwater",
"Transfer Out_Monthly_Sewage Treatment_Unspecified",
"Transfer Out_Monthly_Water Supplier_Groundwater",
"Transfer Out_Monthly_Water Supplier_Surface Water",
"Transfer Out_Monthly_Water Supplier_Unspecified",
"Withdrawal_Annual_Agricultural_Groundwater",
"Withdrawal_Annual_Agricultural_Surface Water",
"Withdrawal_Annual_Agricultural_Unspecified",
"Withdrawal_Annual_Commercial_Groundwater",
"Withdrawal_Annual_Commercial_Surface Water",
"Withdrawal_Annual_Domestic_Groundwater",
"Withdrawal_Annual_Domestic_Surface Water",
"Withdrawal_Annual_Geothermal_Groundwater",
"Withdrawal_Annual_Industrial_Groundwater",
"Withdrawal_Annual_Industrial_Surface Water",
"Withdrawal_Annual_Irrigation_Groundwater",
"Withdrawal_Annual_Irrigation_Surface Water",
"Withdrawal_Annual_Irrigation_Unspecified",
"Withdrawal_Annual_Mining_Groundwater",
"Withdrawal_Annual_Mining_Surface Water",
"Withdrawal_Annual_Mining_Unspecified",
"Withdrawal_Annual_Power (Fossil-Fuel)_Groundwater",
"Withdrawal_Annual_Power (Fossil-Fuel)_Surface Water",
"Withdrawal_Annual_Power (Geothermal)_Groundwater",
"Withdrawal_Annual_Power (Geothermal)_Surface Water",
"Withdrawal_Annual_Water Supplier_Groundwater",
"Withdrawal_Annual_Water Supplier_Surface Water",
"Withdrawal_Annual_Water Supplier_Unspecified",
"Withdrawal_Monthly_Agricultural_Groundwater",
"Withdrawal_Monthly_Agricultural_Surface Water",
"Withdrawal_Monthly_Agricultural_Unspecified",
"Withdrawal_Monthly_Commercial_Groundwater",
"Withdrawal_Monthly_Commercial_Surface Water",
"Withdrawal_Monthly_Domestic_Groundwater",
"Withdrawal_Monthly_Domestic_Surface Water",
"Withdrawal_Monthly_Geothermal_Groundwater",
"Withdrawal_Monthly_Industrial_Groundwater",
"Withdrawal_Monthly_Industrial_Surface Water",
"Withdrawal_Monthly_Industrial_Unspecified",
"Withdrawal_Monthly_Irrigation_Groundwater",
"Withdrawal_Monthly_Irrigation_Surface Water",
"Withdrawal_Monthly_Irrigation_Unspecified",
"Withdrawal_Monthly_Mining_Groundwater",
"Withdrawal_Monthly_Mining_Surface Water",
"Withdrawal_Monthly_Power (Fossil-Fuel)_Groundwater",
"Withdrawal_Monthly_Power (Fossil-Fuel)_Surface Water",
"Withdrawal_Monthly_Power (Geothermal)_Groundwater",
"Withdrawal_Monthly_Power (Geothermal)_Surface Water",
"Withdrawal_Monthly_Water Supplier_Groundwater",
"Withdrawal_Monthly_Water Supplier_Surface Water",
"Withdrawal_Monthly_Water Supplier_Unspecified"]

outdf.AggregationInterval = "1"

outdf.AggregationIntervalUnitCV = "Annual"

outdf.AggregationStatisticCV = "Unspecified"

outdf.AmountUnitCV = "G"

outdf.MaximumAmountUnitCV = "G"

outdf.ReportYearStartMonth = "1"

outdf.ReportYearTypeCV = "CalendarYear"


############################################################################
print("Assign WaterSourceUUID") # has to be one of the last.
outdf = outdf.reset_index(drop=True)
dftemp = pd.DataFrame(index=outdf.index)
dftemp["Count"] = range(1, len(dftemp.index) + 1)
outdf['VariableSpecificUUID'] = dftemp.apply(lambda row: assignVariableSpecificUUID(row['Count']), axis=1)


# Check required fields are not null
############################################################################
print("Check required is not null...")
# #Check all 'required' (not NA) columns have value (not empty). Replace blank strings by NaN, if there are any
outdf = outdf.replace('', np.nan) #replace blank strings by NaN, if there are any
outdf_nullMand = outdf.loc[(outdf["VariableSpecificUUID"].isnull()) | (outdf["VariableSpecificUUID"] == '') |
                           (outdf["AggregationInterval"].isnull()) | (outdf["AggregationInterval"] == '') |
                           (outdf["AggregationIntervalUnitCV"].isnull()) | (outdf["AggregationIntervalUnitCV"] == '') |
                           (outdf["AggregationStatisticCV"].isnull()) | (outdf["AggregationStatisticCV"] == '') |
                           (outdf["AmountUnitCV"].isnull()) | (outdf["AmountUnitCV"] == '') |
                           (outdf["MaximumAmountUnitCV"].isnull()) | (outdf["MaximumAmountUnitCV"] == '') |
                           (outdf["ReportYearStartMonth"].isnull()) | (outdf["ReportYearStartMonth"] == '') |
                           (outdf["ReportYearTypeCV"].isnull()) | (outdf["ReportYearTypeCV"] == '') |
                           (outdf["VariableCV"].isnull()) | (outdf["VariableCV"] == '') |
                           (outdf["VariableSpecificCV"].isnull()) | (outdf["VariableSpecificCV"] == '')]


# Export to new csv
############################################################################
print("Exporting dataframe to csv...")

# The working output DataFrame for WaDE 2.0 input.
outdf.to_csv('ProcessedInputData/variables.csv', index=False)

# Report purged values.
if(len(outdf_nullMand.index) > 0):
    outdf_nullMand.to_csv('ProcessedInputData/variables_missing.csv', index=False)

print("Done.")
