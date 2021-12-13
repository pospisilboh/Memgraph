# Creating a Custom Query Module

Cypher has some basic functions to work with text but a lot of useful functions for string manipulation, comparison, and filtering are missing.

levenshteinSimilarity ... Calculate the similarity (a value within 0 and 1) between two texts based on Levenshtein distance. 

jaroDistance ... Compute Jaro string similarity metric of two strings.
The Jaro string similarity metric is intended for short strings like personal last names. It is 0 for completely different strings and 1 for identical strings.

jaroWinklerDistance ... Compute Jaro string similarity metric of two strings.
The Jaro-Winkler string similarity metric is a modification of Jaro metric giving more weight to common prefix, 
as spelling mistakes are more likely to occur near ends of words.
The prefix weight is inverse value of common prefix length sufficient to consider the strings *identical*. 
If no prefix weight is specified, 1/10 is used.

compareStr ... Compares the two strings and returns 1 if the two strings are equal, 0 otherwise.
However, the function is case-insensitive. In addition, it ignores any non-letters in the string.

normalizeStr ... Generate normalized string

getNumbersFromStr ... Get all numbers from string

uuid_generate ... Generate string UUIDs which can be stored as properties on nodes or edges. 
The underlying implementation makes use of the uuid library.

substring ... Returns a substring of the original string.
start: The starting index of the substring. The character at this index is included in the substring. 
If start is not included, it is assumed to equal to 0.
end: The terminating index of the substring. The character at this index is NOT included in the substring. 
If end is not included, or if the specified value exceeds the string length, it is assumed to be equal to the length of the string by default.
step: Every ‘step’ character after the current character to be included. The default value is 1. 
If the step value is omitted, it is assumed to equal to 1.
 
Memgraph supports extending the query language with user-written procedures. These procedures are grouped into modules (Query Modules), which can then be loaded on startup or later on. We are going to create such a procedure to work with the text.

To get started, we need to create and mount a volume to access the query_modules directory. This directory contains all of the built-in query modules and it’s where we can save new custom query modules. Create an empty directory modules on your host machine and execute the following command:

```sh
docker volume create --driver local --opt type=none --opt device=~modules --opt o=bind modules
```

Now, you can start Memgraph and mount the created volume:
```sh
docker run -it --rm -v c:/modules:/mage/dist -p 7687:7687 -e MEMGRAPH="-query-execution-timeout-sec=0" memgraph
```
 
<p align="center">
   <img src="https://github.com/g-despot/images/blob/master/sng_demo_screenshot.png?raw=true" alt="Data Model" width="900"/>
<p/>