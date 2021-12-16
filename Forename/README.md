# Forename

## Table of Contents

<div class="alert alert-block alert-info" style="margin-top: 20px">

<font size = 3>

1. <a href="item1">Description of the solution</a>

2. <a href="item2">Solution architecture</a>
   
3. <a href="item3">Data model</a>

</font>
</div>

## Description of the solution

By very simple data (forename and their degree) we created a framework that in near future will help us to solve cases as are:
- Customer 360
- Entity resolutions / Record linkage
- ...

By the framework we are able now to:
- compare strings and calculate their similarity by different algorithms
- ...

<p align="center">
   <img src="https://github.com/pospisilboh/Memgraph/blob/88e54a68807e45fd13daec48638f63ed0f1f2ea4/Forename/Images/Dashboards.png?raw=true" alt="Dashboards" width="900"/>
<p/>

## Solution architecture

<p align="center">
   <img src="https://github.com/pospisilboh/Memgraph/blob/491da55e8a3a345c7391b0de435b1b712ea4583c/Forename/Images/Architecture.png?raw=true" alt="Architecture" width="900"/>
<p/>

#### Eternal system
From an external system, we extract `forenames` and their `degree`. Data for import are available as a *.csv file.
```csv
degree,forename
759,Drahomíra
10807,Jaroslav
8314,Hana
...
```

#### Public web pages
Following public web pages were used for web scraping another information (gender, name day, nick names) using the implementation of a Web Scraping framework of Python called [**Beautiful Soup**](https://www.crummy.com/software/BeautifulSoup/bs4/doc/):
- [https://www.kurzy.cz](https://www.kurzy.cz/kalendar/svatky/abecedni-seznam-jmen/) ... `forename`, `gender`, `name day`
- [http://www.e-horoskopy.cz](http://www.e-horoskopy.cz/vyznam-jmen.asp) ... `forename`, `gender`, `name day` and `nick names`
- [https://www.kdejsme.cz](https://www.kdejsme.cz/seznam/) ... `forename`
- [http://svatky.centrum.cz](http://svatky.centrum.cz/jmenny-seznam/?month=1&order=na) ... `forename`, `gender`, `name day`

> If the forename is found in any web page, this forename is valid for us, we set a node property `valid = true`.

### Jupyter Notebook
Main puspose of [**Jupyter Notebook**](https://github.com/pospisilboh/Memgraph/blob/a3cdd22d5435bcbc51d80a6b5a14965024f03d2f/Forename/Jupyter/Memgraph_Forename.ipynb) is to prepare data for another processing:
- Load forenames and their degree from external system (*.csv file)
- Data scraping from public web pages. Get another information to forenames as are `gender`, `name day`, `nick names`
- Forename anonymization can be important because in forenames there can be email addresses, phone numbers, personal identificator.
- Create similarity relations. We compare forenames by implemented functions in custom Query Module (`text_util.py`) and create relationships with an appropriate similarity score:
   - SIMILAR_FORENAME_COMPARED_STRING
   - SIMILAR_FORENAME_LEVENSHTEIN
   - SIMILAR_FORENAME_JAROWINKLER
   - SIMILAR_FORENAME_JARO
- Create forename clusters. Clusters of forenames are created by the function `weakly_connected_components.get()`. For each node new property `componentId` is created. 
- Create forename gender model. Prepare data model to support forename gender recommendation:
   -  nodes with label `Gender` and `LastTwoChar`
   -  edges with type `HAS_GENDER` and `HAS_LAST_TWO_CHAR`
- Nodes and relations enrichement. By the Mamgraph query modules calculate:
   - `betweenness centrality`, `pageRank` for nodes, 
   - `bridge` for relationships.
- Export for Tableau. Following two files are created:
   - export_forename_nodes.csv
   ```csv
   id;value;normalizedValue;valid;anonymized;componentId;gender;nameDay;nameDayDay;nameDayMonth;origin;degree;betweenness;pageRank
   57278;	Anna;anna;;False;4;;;;;;1;0.0;4.769772040048547e-05
   55551;	Barbora;barbora;;False;170;;;;;;1;0.0;4.602584154108701e-05
   55685;	Beata;beata;;False;591;;;;;;1;0.0;5.605711469747777e-05
   54244;	Dušan;dušan;;False;109;;;;;;1;0.0;4.769772040048547e-05
   ...
   ```
   - export_forename_relations.csv
   ```csv
   id1;id2;value1;value2;normalizedValue1;normalizedValue2;valid1;valid2;anonymized1;anonymized2;componentId1;componentId2;gender1;gender2;degree1;degree2;idr;type;score;bridge
   50735;55939;Natalie;Natăˇlie;natalie;natlie;True;;False;;228;228;;;196;7;4476;SIMILAR_FORENAME_LEVENSHTEIN;0.8571428571428572;
   49387;55926;Bohumír;Bohumă­r;bohumír;bohumr;True;;False;;213;213;M;;140;4;4410;SIMILAR_FORENAME_LEVENSHTEIN;0.8571428571428572;
   49365;57273;Antonín;Antoním;antonín;antoním;True;;False;;205;205;M;;2298;4;4433;SIMILAR_FORENAME_LEVENSHTEIN;0.8571428571428572;
   ...
   ```

### Mamgraph

We used the power and simplicity of the Cypher query language and Memgraph’s extensions for algorithms such as:
- Query Module
   - weakly_connected_components.so
      - [**weakly_connected_components.get()**](https://memgraph.com/docs/mage/query-modules/cpp/weakly-connected-components)
   - betweenness_centrality.so
      - [**betweenness_centrality.get()**](https://memgraph.com/docs/mage/query-modules/cpp/betweenness-centrality)
   - pagerank.so
      - [**pagerank.get()**](https://memgraph.com/docs/mage/query-modules/cpp/pagerank)
   - bridges.so
      - [**bridges.get()**](https://memgraph.com/docs/mage/query-modules/cpp/bridges)
- Custom Query Module
   - [**text_util.py**](https://github.com/pospisilboh/Memgraph/tree/master/Forename/Modules)
      -   text_util.levenshteinSimilarity(text1, text2)
      -   text_util.jaroDistance(text1, text2)
      -   text_util.jaroWinklerDistance(text1, text2)
      -   text_util.compareStr(text1, text2, languageCode)
      -   text_util.normalizeStr(text, languageCode)
      -   text_util.getNumbersFromStr(text)
      -   text_util.uuid_generate()
      -   text_util.substring(text, start, end, step)

### Flask
[**Flask**](https://flask.palletsprojects.com/en/2.0.x/) is a micro web framework written in Python and we used it for implementing web services that are consumed by Tableau dashboards. To be able visualize a graph a JavaScript library [**D3.js**](https://www.d3-graph-gallery.com/network) was used.

Implemented services are:
- http://127.0.0.1:5000/get-cluster-recommendation?componentId=
- http://127.0.0.1:5000/get-forename-recommendation?forename=
- http://127.0.0.1:5000/forename-recommendation-form
- http://127.0.0.1:5000/get-forename-detail?id=
- http://127.0.0.1:5000/get-forenames-valid
- http://127.0.0.1:5000/get-graph-cluster/degree/bridge?componentId=
- http://127.0.0.1:5000/get-graph-gender?id=
- http://127.0.0.1:5000/set-forename-rule?rid=
- http://127.0.0.1:5000/get-forename-rule?id=
- http://127.0.0.1:5000/get-forenames-rules

> Parameter `componentId` is unique identificator of cluster.

> Parameter `id` is unique identificator of node.

> Parameter `rid` is unique identificator of edge.

> By the web service http://127.0.0.1:5000/set-forename-rule?rid= is possible to create rule in the database.

### Tableau

Data sources for Tableau dashboards are mentioned files `export_forename_nodes.csv` and `export_forename_relations.csv` and services provided by application server Flask. 

#### Forename dashboard

The main dashboard gives a base overview of what data are available.

<p align="center">
   <img src="https://github.com/pospisilboh/Memgraph/blob/a0642f172e0fef04566bbce79cfdb96e21c5ee61/Forename/Images/Forename%20dashboard.png?raw=true" alt="Forename dashboard" width="900"/>
<p/>

> The count of valid forenames is low (only 29,51 %) but their degree is high (96,08 %). In another word, there are only 3,92 % of wrong forenames.

> There is a lot of forenames with no definition of gender (97,62 %), but their degree is only 10.68 % from all.

> Most popular male name is Petr, Most popular female name is Jana.

#### Forenames clusters

This dashboard gives the possibility to analyze forenames clusters:
- count and list of forenames in each cluster
- types of relations in the cluster
- existed relations between forenames and their similarity score

<p align="center">
   <img src="https://github.com/pospisilboh/Memgraph/blob/a0642f172e0fef04566bbce79cfdb96e21c5ee61/Forename/Images/Forenames%20clusters.png?raw=true" alt="Forenames clusters" width="900"/>
<p/>

> The biggest cluster consists from 25 forenames.

#### Forenames cluster graf

This dashboard gives the possibility to analyze forenames clusters visually:
- define node property (`betweenness`, `degre`, `pageRank`, `valid`)
- define edge property (`bridge`, `score`)
- scale nodes depending on defined node property
- scale edges depending on on defined edge property
- hover over nodes or edges to get a popup with more information

<p align="center">
   <img src="https://github.com/pospisilboh/Memgraph/blob/a0642f172e0fef04566bbce79cfdb96e21c5ee61/Forename/Images/Forenames%20cluster%20graf.png?raw=true" alt="Forenames cluster graf" width="900"/>
<p/>

> In the graph male forenames are blue, female forenames are yellow and forenames without defined gender are grey.

#### Forename recommedation

This dashboard gives the possibility:
- for a defined forename by the selected method (compareStr, levenshteinSimilarity, jaroDistance, jaroWinklerDistance) get recommended forenames.

<p align="center">
   <img src="https://github.com/pospisilboh/Memgraph/blob/a0642f172e0fef04566bbce79cfdb96e21c5ee61/Forename/Images/Foremame%20recommender.png?raw=true" alt="Forename recommedation" width="900"/>
<p/>

> The defined name may not exist in the database.

> The list of recommended forenames is ordered by valid, score DESC, degree DESC.

#### Forename gender recommedation

This dashboard gives the possibility:
- for a selected forename generate forename gender recommendation graph

<p align="center">
   <img src="https://github.com/pospisilboh/Memgraph/blob/a0642f172e0fef04566bbce79cfdb96e21c5ee61/Forename/Images/Forename%20gender%20recommender.png?raw=true" alt="Forename gender recommedation" width="900"/>
<p/>

> In the graph, there are nodes with the label **LastTwoChar** that represent values of the last two characters from forenames. Some of them are:
> - part of only male forenames (blue),
> - part of only female forenames (yellow),
> - part of male and female forenames too (grey).

> For the selected forename **Dennis** by the generated recommendation graph the recommended gender of forename **Dennis** is male.

#### Forenames similarity

This dashboard gives the possibility:
- for a selected forename create in a database repair rule definition (node with label Rule) by the available Tableau action **Set forename rule**

<p align="center">
   <img src="https://github.com/pospisilboh/Memgraph/blob/a93003f527596fb0b20dd393bca21ff3261b277c/Forename/Images/Forenames%20similarity.png?raw=true" alt="Forenames similarity" width="900"/>
<p/>

> Functionality to export all created repair rules in a form of Sql or Cypher scripts is available via the dashboard **Forename repair rules**.

#### Forename repair rules

This dashboard gives the possibility to:
- list all defined repair rules
- download Sql or Cypher script with repair rules

<p align="center">
   <img src="https://github.com/pospisilboh/Memgraph/blob/a0642f172e0fef04566bbce79cfdb96e21c5ee61/Forename/Images/Forename%20repair%20rules.png?raw=true" alt="Forename repair rules" width="900"/>
<p/>

### Tableau Public
Publish Tableau dashboards to Tableau Public is a way how to share our dashboards with others publicly

> Some functionalities of dashboards are limited, there aren't available web services provided by the Flask application server.

## Data model {item3}
<h2 id="item3">Data model</h2>

<p align="center">
   <img src="https://github.com/pospisilboh/Memgraph/blob/58cbaa5780df48841b542f0e10e77dd080c6eec5/Forename/Images/Data%20model.png?raw=true" alt="Custom Query Module - text_util" width="900"/>
<p/>

### Nodes

| Label      | Property | Description |
| :---        |    :----   | :---- |
| Forename | value | Forename from source system. |
| Forename | degree | Forename degree (how often the forename is used in a source system) from a source system. |
| Forename | valid | true ... if the forename was found in web pages used for scraping. |
| Forename | gender | From web pages used for scraping. M ... Male, F ... Female.  |
| Forename | nameDay | From web pages used for scraping. DD.MM. |
| Forename | nameDayDay | Value of day (DD) extracted from nameDay. |
| Forename | nameDayMonth | Value of month (MM) extracted from nameDay. |
| Forename | nickNames | From web pages used for scraping. List of nicknames for the forename. |
| Forename | origin | From web pages used for scraping. <p> Itálie, Severské země, anglický, anglosaský, aramejský, francouzský, germánský, hebrejský, hebrejský, holandský,	italský, jihoslovanský,	keltský, latinský,	maďarský, nejasný, německý, orientální, perský, polský, ruský |
| Forename | source | Forename was found in web pages used for scraping. Source web pages for scraping are: www.kurzy.cz, www.e-horoskopy.cz, www.kdejsme.cz,  www.svatky.centrum.cz |
| Forename | normalizedValue | CALL text_util.normalizeStr(value, 'cz') |
| Forename | valueNumberCount | CALL text_util.getNumbersFromStr(value) |
| Forename | componentId | The WCC algorithm finds sets of connected nodes in an undirected graph, where all nodes in the same set form a connected component. WCC is often used early in an analysis to understand the structure of a graph. <p> Create clusters by WCC algorithm <p> CALL weakly_connected_components.get() |
| Forename | betweenness | Betweenness centrality is a way of detecting the amount of influence a node has over the flow of information in a graph. It is often used to find nodes that serve as a bridge from one part of a graph to another. <p> CALL betweenness_centrality.get(FALSE,FALSE) |
| Forename | pageRank | The PageRank algorithm measures the importance of each node within the graph, based on the number incoming relationships and the importance of the corresponding source nodes. The underlying assumption roughly speaking is that a page is only as important as the pages that link to it. <p> CALL pagerank.get() |
| Forename | anonymized | false/true |
| Forename | anonymizationRule | Identification of rule based on which it was evaluated that anonymization will be performed. |
| Rule | property | A node property name to which the rule will be applied (property: "value"). |
| Rule | source | Source value (source: "Adéla"). |
| Rule | target | Target value (target: "ADéla"). |
| Rule | type | Name of rule type (type: "forename_value"). |
| Gender | value | Value of gender. Can be M ... Male, F ... Female |
| LastTwoChar | value | Value of two last characters from forename. |
| LastTwoChar | genderDegree | Can be 1 ... the two last characters are part of only male or only female forenames or 2 ... the two last characters are part of male and female forenames too. |

### Relationships

| Type      | Property | Description |
| :---        |    :----   | :---- |
| SIMILAR_FORENAME_COMPARED_STRING | score | 0 ... not similar, 1 ... similar |
| SIMILAR_FORENAME_COMPARED_STRING | bridge | A bridge in the graph can be described as an edge which if deleted, creates two disjoint graph components. <p> CALL bridges.get() |
| SIMILAR_FORENAME_LEVENSHTEIN | score | CALL text_util.levenshteinSimilarity(text1, text2) |
| SIMILAR_FORENAME_LEVENSHTEIN | bridge | A bridge in the graph can be described as an edge which if deleted, creates two disjoint graph components. <p> CALL bridges.get() |
| SIMILAR_FORENAME_JAROWINKLER | score | CALL text_util.jaroWinklerDistance(text1, text2) |
| SIMILAR_FORENAME_JAROWINKLER | bridge | A bridge in the graph can be described as an edge which if deleted, creates two disjoint graph components. <p> CALL bridges.get() |
| SIMILAR_FORENAME_JARO | score | CALL text_util.jaroDistance(text1, text2) |
| SIMILAR_FORENAME_JARO | bridge | A bridge in the graph can be described as an edge which if deleted, creates two disjoint graph components. <p> CALL bridges.get() |
| DEFINED_BY | type | Type can be source or target. |
| HAS_LAST_TWO_CHAR | degree | Nodes with label Forename or Gender can have relation HAS_LAST_TWO_CHAR to node with label LastTwoChar. |
| HAS_GENDER |  | Nodes with label Forename can have relation HAS_GENDER to node with label Gender. |

## Sources

https://docs.google.com/forms/d/e/1FAIpQLSdS1l27pfZ7GYExPuOPbiyhjgCZ7HwuN2U2Aii7Z5fSakWgDw/viewform

https://memgraph.com/docs/memgraph/reference-guide/query-modules/load-call-query-modules

https://towardsdatascience.com/how-to-implement-custom-json-utility-procedures-with-memgraph-mage-and-python-7e66bbb8b8e3

https://memgraph.com/blog/how-to-write-custom-cypher-procedures-with-networkx-and-memgraph

https://memgraph.com/docs/memgraph/database-functionalities/query-modules/implement-query-modules#python-api

https://rawgit.com/ztane/python-Levenshtein/master/docs/Levenshtein.html#Levenshtein-distance

https://memgraph.com/docs/memgraph/database-functionalities/query-modules/implement-query-modules

https://memgraph.com/docs/mage/tutorials/create-a-new-module

https://memgraph.com/blog/how-to-visualize-a-social-network-in-python-with-a-graph-database

https://medium.com/neo4j/tagged/data-visualization

https://blog.miguelgrinberg.com/post/beautiful-interactive-tables-for-your-flask-templates

https://editor.swagger.io/#

https://towardsdatascience.com/node2vec-embeddings-for-graph-data-32a866340fef

https://maelfabien.github.io/machinelearning/graph_5/#graph-embedding

https://codepen.io/hadis-kia/pen/RwNWXje

https://sylhare.github.io/2020/06/10/Advanced-node-network-graph-d3.html

https://medium.com/analytics-vidhya/implement-louvain-community-detection-algorithm-using-python-and-gephi-with-visualization-871250fb2f25

https://www.kaggle.com/lsjsj92/network-graph-with-louvain-algorithm

https://visjs.github.io/vis-network/docs/network/nodes.html

https://stackoverflow.com/questions/34009980/return-a-download-and-rendered-page-in-one-flask-response
