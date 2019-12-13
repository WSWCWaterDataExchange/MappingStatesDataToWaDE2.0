"""
may need to modify capitalization
"""
beneficialUseDictionary = {
    "I":"Irrigation",
    "S":"Stockwatering",
    "D":"Domestic",
    "M":"Municipal",
    "X":"Mining",
    "P":"Power",
    "O":"Other"
}

beneficialUseDictionaryNM = {
    "AGR":"Agriculture other than irrigation",
    "AUG":"Augmentation well",
    "BPW":"Brine production well",
    "CEM":"Cemetery",
    "CLS":"Closed file",
    "COM":"Commercial",
    "CON":"Construction",
    "CPS":"Cathodic protection well",
    "DAI":"Dairy operation",
    "DCN":"Domestic construction",
    "DEW":"Dewatering well",
    "DOL":"72-12-1 domestic and livestock watering",
    "DOM":"72-12-1 domestic one household",
    "EXP":"Exploration",
    "FCD":"Flood control",
    "FGP":"Fish and game propogation",
    "FPO":"Feed pen operation",
    "GEO":"Geothermal boreholes",
    "HWY":"Highway construction",
    "IND":"Industrial",
    "INJ":"Injection",
    "IRR":"Irrigation",
    "MDW":"Community type use - mdwca, private or commercial supplied",
    "MFG":"Manufacturing",
    "MIL":"Military - military installations",
    "MIN":"Mining or milling or oil",
    "MOB":"Mobile home parks",
    "MON":"Monitoring well",
    "MPP":"Meat packing plant",
    "MUL":"72-12-1 multiple domestic households",
    "MUN":"Municipal - city or county supplied water",
    "N07":"No pre-1907 water right exists on this land",
    "NON":"Non-profit organizational use",
    "NOT":"No use of right or POD",
    "NRT":"No right",
    "OBS":"Observation",
    "OFM":"Oil field maintenance",
    "OIL":"Oil production",
    "PDL":"Non 72-12-1 domestic and livestock watering",
    "PDM":"Non 72-12-1 domestic one household",
    "PLS":"Non 72-12-1 livestock watering",
    "PMH":"Non 72-12-1 multiple domestic households",
    "POL":"Pollution control well",
    "POU":"Poultry and egg operation",
    "PPP":"Petroleum processing plant",
    "PRO":"72-12-1 Prospecting or development of natural resource",
    "PUB":"72-12-1 Construction of public works",
    "REC":"Recreation",
    "SAN":"72-12-1 Sanitary in conjunction with a commercial use",
    "SCH":"School use - public, private, parochial, & universities",
    "SRO":"Secondary recovery of oil",
    "STK":"72-12-1 livestock watering",
    "STO":"Storage",
    "STR":"Strategic water reserve",
    "SUB":"Subdivision",
    "SWR":"Stacked water right",
    "TBD":"To be determined",
    "UTL":"Public utility"
}

###-- Blank for Rights that do NOT have a Status
AllocationLegalStatusDictionary={
    "ADEC":"Adjudication Decree",
    "APP":"Approved",
    "CERT":"Certificated",
    "DIS":"Disallowed",
    "EXP":"Expired",
    "FORF":"Forfeited",
    "LAP":"Lapsed",
    "LAPD":"Lapsed(Destroyed), Currently NOT Used",
    "NPR":"No Proof Required",
    "NUSE":"Nonuse",
    "PERF":"Perfected",
    "REJ":"Rejected",
    "REJD":"Rejected(Destroyed), Currently Not Used",
    "RNUM":"Renumbered",
    "TERM":"Terminated",
    "UNAP":"Unapproved",
    "WD":"Withdrawn",
    "WDD":"Withdrawn(Destroyed), Currently Not Used",
    "WUC":"Water User`s Claim"
}

AllocationLegalStatusDictionaryNM = {
    "ADJ":"Adjudicated",
    "ADM":"Administrative",
    "APP":"Application",
    "APR":"Application Being Protested",
    "CAN":"Cancelled",
    "CLS":"Closed File",
    "DCL":"Declaration",
    "DED":"Dedicated",
    "DEN":"Denied",
    "EXP":"Expired",
    "HS ":"Hydrographic Survey",
    "LIC":"Licensed",
    "NOI":"Notice of Intention",
    "NOT":"Not implies that there is no status",
    "OMS":"Owner Management Status",
    "OOJ":"Offer of Judgment",
    "PBU":"Proof of Beneficial Use",
    "PMT":"Permit",
    "PRG":"Purged Conversion Record",
    "REN":"Renumbered",
    "RET":"Retired",
    "TRN":"Transferred",
    "WMS":"Water Master Status",
    "WTD":"Withdrawn"    
}

AllocationTypeCVDictionary={
"ADEC":"Adjudication Decree",
"ADV":"Adverse Use",
"APPL":"Application to Appropriate",
"DEC":"Decree",
"DIL":"Diligence Claim",
"FEDR": "Federal Reserved Water Right",
"FIXD":"Fixed-Time Application",
"PAC":"Pending Adjudication Claim",
"SHAR":"Water Company Shares",
"TEMP":"Temporary Application",
"UGWC":"Underground Water Claim"
}

#Blank to “unknown”
WaterSourceTypeCVDictionary = {
"A":"Abandoned",
"D":"Drain",
"C":"Sewage",
"F":"Sewage",
"N":"Sewage",
"P":"Sewage",
"G":"groundwaterspring",
"R":"Point of Rediversion",
"S":"Surface Water",
"T":"Point of Return",
"U":"groundwaterall"
}

groundwaterSourceType = {
    "A":"Groundwater/Artesian",
    "D":"Groundwater/Dry",
    "M":"Groundwater/Mixed",
    "S":"Groundwater/Shallow"
}

coordinateMethodType = {
    "UN":"Unknown Source",
    "PA":"Provided by Applicant",
    "PD":"Provided by Driller",
    "UA":"Updated by Applicant",
    "EA":"OSE In-office Geospatial Application",
    "EM":"OSE Aerial Photography/Map",
    "EG":"OSE On-site Inspection/GPS",
    "ES":"OSE Hydrographic Survey",
    "G":"PLSS",
    "N":"None",
    "D":"Disclaimer"    
}

coordinateMethodAccuracy = {
    "L":"Large-scale map or aerial photo source",
    "M":"Medium-scale map or aerial photo source",
    "S":"Small-scale map or aerial photo source"
}
