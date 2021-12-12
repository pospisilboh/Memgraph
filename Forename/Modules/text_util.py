# https://rawgit.com/ztane/python-Levenshtein/master/docs/Levenshtein.html#Levenshtein-jaro_winkler

import mgp
from Levenshtein import *
import uuid

# Compute absolute Levenshtein distance of two strings.
@mgp.read_proc
def levenshteinSimilarity(ctx: mgp.ProcCtx,
                   stringOne: str,
                   stringTwo: str) -> mgp.Record(score=float):
    
    w1 = stringOne
    w2 = stringTwo

    score = 1 - distance(w1, w2) / max(len(w1), len(w2))

    return mgp.Record(score=float(score))

# Compute Jaro string similarity metric of two strings.
# The Jaro string similarity metric is intended for short strings like personal last names. 
# It is 0 for completely different strings and 1 for identical strings.
@mgp.read_proc
def jaroDistance(ctx: mgp.ProcCtx,
                   stringOne: str,
                   stringTwo: str) -> mgp.Record(score=float):
    
    w1 = stringOne
    w2 = stringTwo

    score = jaro(w1, w2)

    return mgp.Record(score=float(score))

# Compute Jaro string similarity metric of two strings.
# The Jaro-Winkler string similarity metric is a modification of Jaro metric giving more weight to common prefix, 
# as spelling mistakes are more likely to occur near ends of words.
# The prefix weight is inverse value of common prefix length sufficient to consider the strings *identical*. 
# If no prefix weight is specified, 1/10 is used.
@mgp.read_proc
def jaroWinklerDistance(ctx: mgp.ProcCtx,
                   stringOne: str,
                   stringTwo: str) -> mgp.Record(score=float):
    
    w1 = stringOne
    w2 = stringTwo

    score = jaro_winkler(w1, w2)

    return mgp.Record(score=float(score))

# Compares the two strings and returns 1 if the two strings are equal, 0 otherwise.
# However, the function is case-insensitive. In addition, it ignores any non-letters in the string.
@mgp.read_proc
def compareStr(ctx: mgp.ProcCtx,
                   stringOne: str,
                   stringTwo: str,
                   languageCode: mgp.Nullable[mgp.Any] = None) -> mgp.Record(score=float):
    
    w1 = stringOne.lower()
    w2 = stringTwo.lower()

    new_w1 = ''
    new_w2 = ''
    
    if languageCode == 'cz':
        specialCodes = [225,269,271,233,283,237,328,243,345,353,357,250,367,253,382]
    else:
        specialCodes = []

    for i in range(len(w1)):
        if (ord(w1[i]) >= 97 and ord(w1[i]) <= 122) or ord(w1[i]) in specialCodes:
            new_w1 += w1[i]
 
    for i in range(len(w2)):
        if (ord(w2[i]) >= 97 and ord(w2[i]) <= 122) or ord(w2[i]) in specialCodes:
            new_w2 += w2[i]
 
    if new_w1 == new_w2:
        return mgp.Record(score=float(1))
    else:
        return mgp.Record(score=float(0))

# Generate normalized string
@mgp.read_proc
def normalizeStr(ctx: mgp.ProcCtx,
                   stringOne: str,
                   languageCode: mgp.Nullable[mgp.Any] = None) -> mgp.Record(normalizedStr=str):
        
    w1 = stringOne.lower()

    new_w1 = ''

    if languageCode == 'cz':
        specialCodes = [225,269,271,233,283,237,328,243,345,353,357,250,367,253,382]
    else:
        specialCodes = []

    for i in range(len(w1)):
        if (ord(w1[i]) >= 97 and ord(w1[i]) <= 122) or ord(w1[i]) in specialCodes:
            new_w1 += w1[i]

    return mgp.Record(normalizedStr=new_w1)


# Get all numbers from string
@mgp.read_proc
def getNumbersFromStr(ctx: mgp.ProcCtx,
                   stringOne: str) -> mgp.Record(numbers=str):
        
    w1 = stringOne

    new_w1 = ''

    specialCodes = [48,49,50,51,52,53,54,55,56,57]

    for i in range(len(w1)):
        if ord(w1[i]) in specialCodes:
            new_w1 += w1[i]

    return mgp.Record(numbers=new_w1)


# Generate string UUIDs which can be stored as properties on nodes or edges. 
# The underlying implementation makes use of the uuid library.
@mgp.read_proc
def uuid_generate(ctx: mgp.ProcCtx) -> mgp.Record(uuid=str):
    result = uuid.uuid4()
    uuid_string = str(result)
    return mgp.Record(uuid=uuid_string)


# Returns a substring of the original string.
# start: The starting index of the substring. The character at this index is included in the substring. 
# If start is not included, it is assumed to equal to 0.
# end: The terminating index of the substring. The character at this index is NOT included in the substring. 
# If end is not included, or if the specified value exceeds the string length, it is assumed to be equal to the length of the string by default.
# step: Every ‘step’ character after the current character to be included. The default value is 1. 
# If the step value is omitted, it is assumed to equal to 1.
@mgp.read_proc
def substring(ctx: mgp.ProcCtx,
                   original: str,
                   start: mgp.Nullable[mgp.Any] = None,
                   end: mgp.Nullable[mgp.Any] = None,
                   step: mgp.Nullable[mgp.Any] = None) -> mgp.Record(substring=str):
        
    w1 = original

    new_w1 = w1[start:end:step]

    return mgp.Record(substring=new_w1)
