# Custom Query Module - text_util

Cypher has some basic functions to work with text but a lot of useful functions for string manipulation, comparison, and filtering are missing. Memgraph supports extending the query language with user-written procedures. These procedures are grouped into modules (Query Modules), which can then be loaded on startup or later on. 

We created the query module **text_util.py** because it will contain utility functions that are needed to work with text.

<p align="center">
   <img src="https://github.com/pospisilboh/Memgraph/blob/7980a2d858d23a039229eb467e874cbcd2f7cf79/Forename/Images/Custom%20Query%20Module%20-%20text_util.png?raw=true" alt="Custom Query Module - text_util" width="900"/>
<p/>

## Overview Functions

| Functions      | Description |
| :---        |    :----   |
| text_util.levenshteinSimilarity(text1, text2) | Calculate the similarity (a value within 0 and 1) between two texts based on Levenshtein distance. |
| text_util.jaroDistance(text1, text2) | Compute Jaro string similarity metric of two strings. The Jaro string similarity metric is intended for short strings like personal last names. It is 0 for completely different strings and 1 for identical strings. |
| text_util.jaroWinklerDistance(text1, text2) | The Jaro-Winkler string similarity metric is a modification of Jaro metric giving more weight to common prefix, as spelling mistakes are more likely to occur near ends of words. The prefix weight is inverse value of common prefix length sufficient to consider the strings *identical*. If no prefix weight is specified, 1/10 is used. |
| text_util.compareStr(text1, text2, languageCode) | Compares the two strings and returns 1 if the two strings are equal, 0 otherwise. However, the function is case-insensitive. In addition, it ignores any non-letters in the string.        |
| text_util.normalizeStr(text, languageCode) |  Generate normalized string. |
| text_util.getNumbersFromStr(text) | Get all numbers from string. |
| text_util.uuid_generate() | Generate string UUIDs which can be stored as properties on nodes or edges. The underlying implementation makes use of the uuid library. |
| text_util.substring(text, start, end, step) | Returns a substring of the original string. <p> **start:** The starting index of the substring. The character at this index is included in the substring. If start is not included, it is assumed to equal to 0. <p> **end:** The terminating index of the substring. The character at this index is NOT included in the substring. If end is not included, or if the specified value exceeds the string length, it is assumed to be equal to the length of the string by default. <p> **step:** Every ‘step’ character after the current character to be included. The default value is 1. If the step value is omitted, it is assumed to equal to 1. |

## Text Similarity Functions

Compare the strings with the Levenshtein distance
```sh
CALL text_util.levenshteinSimilarity('Katarina', 'Katerina') YIELD * // 0.875
```
 
Compare the strings with the jaroDistance
```sh
CALL text_util.jaroDistance('Katarina', 'Katerina') YIELD * // 0.8214285714285715
```
 
Compare the strings with the jaroWinklerDistance
```sh
CALL text_util.jaroWinklerDistance('Katarina', 'Katerina') YIELD * // 0.875
```

Compares the two strings with the compareStr
```sh
CALL text_util.compareStr('Kateřina', '1234/*-Kateřina1234/*-') YIELD * // 1
```

## Data Cleaning Functions
Generate normalized string with the normalizeStr
```sh
CALL text_util.normalizeStr('1234/*-Kateřina1234/*-') YIELD * // 'kateina'
 
CALL text_util.normalizeStr('1234/*-Kateřina1234/*-', 'cz') YIELD * // 'kateřina'
```

Get all numbers from string with the getNumbersFromStr
```sh
CALL text_util.getNumbersFromStr('1234/*-Ka5teři6na789/*-') YIELD * // '123456789'
```

## Other Functions
Generate string UUIDs with the uuid_generate
```sh
CALL text_util.uuid_generate () YIELD * // 'd6022f8d-62ff-47e6-8d3a-31fbfdd41f77'
```

> In Memgraph there is a function **uuid_generator.get()**. The underlying implementation makes use of the uuid-dev library. When using the uuid module on Linux systems, the library can be installed by running sudo apt-get install uuid-dev.

```sh
CALL uuid_generator.get() YIELD uuid
```
 
Returns a substring of the original string  with the substring
```sh
CALL text_util.substring('Katarina', -2) YIELD * // 'na'
```
 
> In Memgraph there is a function **substring**. But there is an issue: https://github.com/memgraph/memgraph/issues/307 and it was the reason why we implemented our **text_util.substring**.

## Custom Query Modules Using Docker

To get started, we need to create and mount a volume to access the query_modules directory. This directory contains all of the built-in query modules and it’s where we can save new custom query modules, in our case our **text_util.py** file. 
   
Create an empty directory modules on your host machine and execute the following command:
```sh
docker volume create --driver local --opt type=none --opt device=~modules --opt o=bind modules
```

Now, we can start Memgraph and mount the created volume:
```sh
docker run -it --rm -v c:/modules:/mage/dist -p 7687:7687 -e MEMGRAPH="-query-execution-timeout-sec=0" memgraph
```
   
The file **text_util.py** should be in the **c:/modules** directory.
   
### Utility query module
   
Query procedures that allow the users to gain more insight into other query modules and their procedures are written under our utility mg query module. This module offers following procedures:

Loads or reloads all modules
```sh
CALL mg.load_all()
```

Lists loaded procedures and their signatures.
```sh
CALL mg.procedures() YIELD *
```
