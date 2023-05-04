# Last Update: 05/03/2023
# Purpose: To have a single function file to create OwnerClassificationCV field.


# Needed Libraries
############################################################################
import re
import pandas as pd



# Owner Type Lists
########################################################################################################################
########################################################################################################################
# Generic
# ---------------------------------------------------------------------
unList = ["unspecified", "wade unspecified", "unknown"]
nalist = ["tribe", "tribes", "nation", "nations", "indians"]

# Government
# ---------------------------------------------------------------------
usoalist = ["united states of america", "united states america", "usa"]
ushudlist = ["housing and urban development", "housing & urban development", "ushud"]
usfaalist = ["usfaa", "federal aviation administration"]
usgsalist = ["usgsa", "general services administration"]
bialist = ["bureau of indian aff", "bureau of indian", "indian affairs", "usbia"]

# Military
# ---------------------------------------------------------------------
millist = ["us army", "u s army", "usarmy", "usa army", "national guard", "corps of engineer", "corps of engineers", "army corp", "army corps", "army corp of", "usa department of the army", "uscbp", "border patrol", "border protection", "customs service ", "customs office", "department of defense", "dept of defense", "dhs", "homeland security", "marine corps",  "usaf", "usafb", "afb", "air force", "airforce", "aire force", "air national guard"]

# Natural Resources
# ---------------------------------------------------------------------
usblmlist = ["usblm", "blm", "bureau of land mgmt", "bureau of land management", "bureau of land mgmnt", "bureau of land mgt", "bureau of land managment", "bureau of land managenemt"]
usbrlist = ["usbr", "bureau of reclam", "bureau of reclamation", "bureau reclamation"]
usdalist = ["u s  dept of agriculture", "u s agriculture", "us agriculture dept", "us department agriculture", "us dept of agriculture", "usa  department of agriculture", "usa  dept of agriculture", "usda"]
usdoelist = ["department of energy", "u s department of energy", "u s dept  of energy lanl", "u s  department of energy", "u s  department of energy", "u s department of energy", "united states department of energy", "us department energy", "us department of energy", "us doe", "usa department of energy"]
epalist = ["environmental protection agency", "epa", "e p a"]
fwlist = ["u s department of the interior fish and wildlife service","u s dept of fish & wildlife","u s dept of the interior fish and wildlife","u s fish & wildlife","u s fish and wildlife","united states fish and wildlife","united states of america fish and wildlife","us department fish & wildlife","us department of fish & wildlife","us dept of interior fish and wildlife","us dept of the interior fish and wildlif","us fish & wild life","us fish & wildlife","us fish and wildlife","us interior dept fish & wildlife","usa department of interior fish and wildlife","usa dept of interior fish & wildlife","usa fish & wildlife","usa fish and wildlife","usdi fish & wildlife","usdi fish and wildlife","usdoi fish & wildlife","fish and wildlife","usfws"]
usfslist = ["forest service united states","forest service usda","u s d a forest service","u s forest service","u s forest","united states forest service","us forest service","usa forest service","usda forest service","forest service","usfs"]
usgslist = ["u s geological survey","us geological survey","usa geological survey"]
usnplist = ["national park", "natl park serv", "national forest", "nat forest", "natl forest"]

# Non-Federal List
# ---------------------------------------------------------------------
priList = ["corporation", "company", "commission", "co", "inc", "llc", "limited", "ltd"]


# Making the dictionary
########################################################################################################################
########################################################################################################################

listDictionary = {} # create list dictioarny.

# Generic List
# ---------------------------------------------------------------------
listDictionary["WaDE Unspecified"] = unList
listDictionary["Native American"] = nalist

# Government List
# ---------------------------------------------------------------------
listDictionary["United States of America"] = usoalist
listDictionary["Department of Housing and Urban Development (USHUD)"] = ushudlist
listDictionary["Federal Aviation Administration (USFAA)"] = usfaalist
listDictionary["General Services Administration (USGSA)"] = usgsalist
listDictionary["Bureau of Indian Affairs (USBIA)"] = bialist

# Military List
# ---------------------------------------------------------------------
listDictionary["Military"] = millist

# Natural Resources List
# ---------------------------------------------------------------------
listDictionary["National Park Service (USNPS)"] = usnplist
listDictionary["Bureau of Land Management (USBLM)"] = usblmlist
listDictionary["Bureau Reclamation (USBR)"] = usbrlist
listDictionary["Department of Agriculture (USDA)"] = usdalist
listDictionary["Department of Energy (USDOE)"] = usdoelist
listDictionary["Environmental Protection Agency (USEPA)"] = epalist
listDictionary["Fish and Wildlife Service (USFWS)"] = fwlist
listDictionary["Forest Service (USFS)"] = usfslist
listDictionary["Geological Survey (USGS)"] = usgslist

# Non-Federal List
# ---------------------------------------------------------------------
listDictionary["Private"] = priList


# Assign OwnerClassification value.
# Uses the re library, but requires for loop.
# Order that the lists are inputed into dictoinary is important, want to overide generic search with a more specific search.
########################################################################################################################
########################################################################################################################

def CreateOwnerClassification(val):
    val = str(val).strip()
    if val == '' or pd.isnull(val):
        outString = "WaDE Unspecified"
    else:
        outString = "WaDE Unspecified "  # Default Value

        # Cleaning text / simple search format
        val = re.sub("[$@&.`;',/\)(-]", "", val).strip()
        val = val.lower().strip()
        val = " " + val + " "

        for x in listDictionary:
            valueList = listDictionary[x]
            for words in valueList:
                if re.search(" " + words + " ", val): outString = x

    return outString