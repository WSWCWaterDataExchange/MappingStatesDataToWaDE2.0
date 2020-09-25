"""
may need to modify capitalization
"""
beneficialUseDictionary_CO = {
    "0":"STORAGE",
    "1":"IRRIGATION",
    "2":"MUNICIPAL",
    "3":"COMMERCIAL",
    "4":"INDUSTRIAL",
    "5":"RECREATION",
    "6":"FISHERY",
    "7":"FIRE",
    "8":"DOMESTIC",
    "9":"STOCK",
    "A":"AUGMENTATION",
    "B":"EXPORT FROM BASIN",
    "C":"CUMULATIVE ACCRETION TO RIVER",
    "D":"CUMULATIVE DEPLETION FROM RIVER",
    "E":"EVAPORATIVE",
    "F":"FEDERAL RESERVED",
    "G":"GEOTHERMAL",
    "H":"HOUSEHOLD USE ONLY",
    "K":"SNOW MAKING",
    "M":"MINIMUM STREAMFLOW",
    "N":"NET EFFECT ON RIVER",
    "P":"POWER GENERATION",
    "Q":"OTHER",
    "R":"RECHARGE",
    "S":"EXPORT FROM STATE",
    "T":"TRANSMOUNTAIN EXPORT",
    "W":"WILDLIFE",
    "X":"ALL BENEFICIAL USES"
}

beneficialUseDictionary_UT = {
    "I":"Irrigation",
    "S":"Stockwatering",
    "D":"Domestic",
    "M":"Municipal",
    "X":"Mining",
    "P":"Power",
    "O":"Other"
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