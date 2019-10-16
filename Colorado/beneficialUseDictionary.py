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