# WaDE Owner Classification Type Project Overview
This readme details the process that was applied by the staff of the [Western States Water Council (WSWC)](http://wade.westernstateswater.org/) to categorizing water right's owners into easily distinguishable groups for the purpose of data filtering and dashboard visualizations.

## Summary of Data Prep
The WaDE **OwnerClassificationTypeCV** field was assigned by utilizing a keyword search algorithm using the state provided water right owner (e.g., **AllocationOwner** field in WaDE) terminology.  The keyword search starts with a generic term search, but then is overridden with a more term specific search (e.g. a water right owner listed as *USA Real Estate Corp* would  first be labeled as an "United States of America" owner type by the word "USA", but then overwritten to a "Private" owner type by the use of the word "Real Estate" & "Corp)"

Water right records can possess multiple owners.  Records within WaDE with multiple **AllocationOwner** entries were given a single best fist term for **OwnerClassificationTypeCV**, as WaDE only allows for a single entry.  

Owner name terminology that is either blank or unknown is given a value of **Unspecified**.

A default value of "Private" is given to all water right owner name terminologies not categorized at this time.

For a list of specific keywords used for categorization group, see & download [Notes_OwnerClassification.xlsx](https://github.com/WSWCWaterDataExchange/MappingStatesDataToWaDE2.0/blob/master/5_CustomFunctions/OwnerClassification/Notes_OwnerClassification.xlsx)


