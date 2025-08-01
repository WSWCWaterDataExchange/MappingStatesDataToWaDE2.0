# Last Update: 07/16/2025
# Purpose: To have a single function file to create OwnerClassificationCV field.

import re
import pandas as pd

# -----------------------------
# 1. Load your classification data
# -----------------------------
datadf = pd.read_excel(
    "C:/Users/rjame/Documents/WSWC Documents/MappingStatesDataToWaDE2.0/5_CustomFunctions/OwnerClassification/Notes_OwnerClassification.xlsx",
    sheet_name="TrackWordsByGroup",
    skiprows=1
)


# -----------------------------
# 2. Clean and build regex patterns
# -----------------------------
def CleanWordFunc(w):
    w = str(w).lower()
    w = re.sub(r"[$@&.`;',/\)(-]", "", w)
    return w.strip()

# Pre-compile category DataFrame into regex patterns, store in dictionary. Use re.compile() to build one regex pattern per class.
pattern_dict = {}
for columnName, columnData in datadf.items():
    terms = columnData.dropna().tolist()
    # Clean terms
    terms = [CleanWordFunc(term) for term in terms]
    if terms:
        # Join into regex
        pattern_str = r'\b(' + '|'.join(map(re.escape, terms)) + r')\b'
        # Precompile
        pattern_dict[columnName] = re.compile(pattern_str, re.IGNORECASE)


# -----------------------------
# 3. Create the classification function
# -----------------------------
def CreateOwnerClassification(val):
    if pd.isnull(val) or not str(val).strip():
        return "Unspecified"

    # Default
    outString = "Private"

    # Clean input value
    val = str(val)
    val = re.sub(r"[$@&.`;',/\)(-]", "", val).strip()
    val = val.lower()

    # Add spaces to enforce word boundaries
    val_padded = f" {val} "

    # Search through pattern_dict
    for className, pattern in pattern_dict.items():
        if pattern.search(val_padded):
            outString = className

    return outString