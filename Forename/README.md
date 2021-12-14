#

## Architecture

<p align="center">
   <img src="https://github.com/pospisilboh/Memgraph/blob/478e94fd4609ebec00b4890b086281079bac1559/Forename/Images/Architecture.png?raw=true" alt="Architecture" width="900"/>
<p/>

#### Eternal system
From an external system, we extract forenames and their degree. Data are available as a *.csv file.

#### Public web pages
Following public web pages were used for web scraping another information using the implementation of a Web Scraping framework of Python called Beautiful Soup:
- https://www.kurzy.cz/kalendar/svatky/abecedni-seznam-jmen/ (forename, gender, name day)
- http://www.e-horoskopy.cz/vyznam-jmen.asp (forename, gender, name day and nick names)
- https://www.kdejsme.cz/seznam/ (forename)
- http://svatky.centrum.cz/jmenny-seznam/?month=1&order=na (forename, gender, name day)

### Jupyter Notebook
Main puspose of Jupyter Notebook is to prepare data for another processing:
- Load Forenames and their degree from external system (*.csv file)
- Data scraping from public web pages. Get another information to forenames as are gender, name day, nick names
- Forename anonymization can be important because in forenames there can be email addresses, phone numbers, personal identificator.
- Create similarity relations. We compare forenames by implemented functions in custom Query Module (text_util.py) and create relationships with similarity score.
- Create forename clusters. Through the created relationships forename clusters are created.
- Create forename gender model. Prepare database model for forename gender recommendation.
- Nodes and relations enrichement. By the Mamgraph query Module calculate nodes betweenness centrality, pageRank and bridge for relationships.
- Export for Tableau.

### Mamgraph
- Custom Query Module
   - text_util.py
      -   text_util.normalizeStr(value, 'cz')
- Query Module
   - weakly_connected_components.get()
   - betweenness_centrality.get(FALSE,FALSE)
   - pagerank.get()
   - bridges.get()

### Flask
- Web services

### Tableau
- Forename repair rules
- Forename dashboard
- Forenames clusters
- Forenames cluster graf
- Forename recommedation
- Forename gender recommedation
- Forenames similarity
- Forename nameDay

### Tableau Public
Publish Tableau dashboards to Tableau Public is a way how to share our dashboards with others publicly

## Data model

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
| Forename | source | Forename was found in web pages used for scraping. Source web pages for scraping are: www.kurzy.cz, www.e-horoskopy.cz, www.kdejsme.cz, www.svatky.centrum.cz |
| Forename | normalizedValue | CALL text_util.normalizeStr(value, 'cz') |
| Forename | valueNumberCount | CALL text_util.getNumbersFromStr(value) |
| Forename | componentId | The WCC algorithm finds sets of connected nodes in an undirected graph, where all nodes in the same set form a connected component. WCC is often used early in an analysis to understand the structure of a graph. <p> Create clusters by WCC algorithm <p> CALL weakly_connected_components.get() |
| Forename | betweenness | Betweenness centrality is a way of detecting the amount of influence a node has over the flow of information in a graph. It is often used to find nodes that serve as a bridge from one part of a graph to another. <p> CALL betweenness_centrality.get(FALSE,FALSE) |
| Forename | pageRank | The PageRank algorithm measures the importance of each node within the graph, based on the number incoming relationships and the importance of the corresponding source nodes. The underlying assumption roughly speaking is that a page is only as important as the pages that link to it. <p> CALL pagerank.get() |
| Forename | anonymized | false/true |
| Forename | anonymizationRule |  |
| Rule | property |  |
| Rule | source |  |
| Rule | normalizedValue |  |
| Rule | type |  |
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
| DEFINED_BY | type |  |
| HAS_LAST_TWO_CHAR | degree |  |
| HAS_GENDER |  |  |



## Source

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
