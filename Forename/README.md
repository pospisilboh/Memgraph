# Forename analyzer

## Table of Contents

<div class="alert alert-block alert-info" style="margin-top: 20px">

<font size = 3>

1. <a href="#description">Description of the solution</a>

2. <a href="#architecture">Solution architecture</a>
   
   - [Architecture diagram](https://github.com/pospisilboh/Memgraph/tree/master/Forename#architecture-diagram)
   - [External system](https://github.com/pospisilboh/Memgraph/tree/master/Forename#external-system)
   - [Public web pages](https://github.com/pospisilboh/Memgraph/tree/master/Forename#public-web-pages)
   - [Jupyter Notebook](https://github.com/pospisilboh/Memgraph/tree/master/Forename#jupyter-notebook)
   - [Memgraph database](https://github.com/pospisilboh/Memgraph/tree/master/Forename#memgraph-database)
   - [Memgraph database on Memgraph Cloud](https://github.com/pospisilboh/Memgraph/tree/master/Forename#memgraph-database-on-memgraph-cloud)
   - [Flask Application Server](https://github.com/pospisilboh/Memgraph/tree/master/Forename#flask-application-server)
      - [Flask Application Server on IBM Cloud Foundry](https://github.com/pospisilboh/Memgraph/tree/master/Forename#flask-application-server-on-ibm-cloud-foundry)
      - [Flask Application Server on Amazon Lightsail](https://github.com/pospisilboh/Memgraph/tree/master/Forename#flask-application-server-on-amazon-lightsail)
      - [Flask Application Server on GCP App Engine](https://github.com/pospisilboh/Memgraph/tree/master/Forename#flask-application-server-on-gcp-app-engine)
      - [Flask Application Server on DigitalOcean Apps Platform](https://github.com/pospisilboh/Memgraph/tree/master/Forename#flask-application-server-on-digitalocean-apps-platform)
   - [Tableau dashboards](https://github.com/pospisilboh/Memgraph/tree/master/Forename#tableau-dashboards)
   - [Tableau dashboards on Tableau Public](https://github.com/pospisilboh/Memgraph/tree/master/Forename#tableau-dashboards-on-tableau-public)
   
3. <a href="#data-model">Data model</a>
   - [Data model diagram](https://github.com/pospisilboh/Memgraph/tree/master/Forename#data-model-diagram)
   - [Nodes definition](https://github.com/pospisilboh/Memgraph/tree/master/Forename#nodes-definition)
   - [Relationships definition](https://github.com/pospisilboh/Memgraph/tree/master/Forename#relationships-definition)

4. <a href="#sources">Additional Resources</a>

</font>
</div>

<h2 id="description">Description of the solution</h2>

Using simple data, `forenames` and their `degree`, we built a <a href="#data-model">graph</a> and later a solution, which soon will help us improve data quality and solve cases such as:
- [Customer 360](https://profisee.com/customer-360-what-why-and-how/)
- [Single Customer View](https://en.wikipedia.org/wiki/Single_customer_view)
- [Entity resolutions / Record linkage](https://en.wikipedia.org/wiki/Record_linkage)
- [Master Data Management](https://en.wikipedia.org/wiki/Master_data_management)
- ...

The main `business features` of our solution are:
- <a href="#Forenames clusters analyzer">Forenames clusters analyzer</a>
- <a href="#Forenames clusters graph analyzer">Forenames clusters graph analyzer</a>
- <a href="#Forename recommendation">Forename recommendation</a>
- <a href="#Forename gender recommendation">Forename gender recommendation</a>
- <a href="#Forename repair rules recommendation">Forename repair rules recommendation</a>
- <a href="#Forename repair rules getter">Forename repair rules getter</a>

Live demo is available in [here](https://public.tableau.com/app/profile/bobovo.eu/viz/Forenames_20211216/Forenamedashboard).

<p align="center">
   <img src="https://github.com/pospisilboh/Memgraph/blob/88e54a68807e45fd13daec48638f63ed0f1f2ea4/Forename/Images/Dashboards.png?raw=true" alt="Dashboards" width="900"/>
<p/>

The main `technical abilities` of our solution are:
- Memgraph Custom Query Module [text_util.py](https://github.com/pospisilboh/Memgraph/tree/master/Forename/Modules) that contain utility functions that are needed to work with text
- By [Jupyter Notebook](https://github.com/pospisilboh/Memgraph/blob/a3cdd22d5435bcbc51d80a6b5a14965024f03d2f/Forename/Jupyter/Memgraph_Forename.ipynb):
   - Load data to Memgraph database from *.csv files
   - Scrap data from public web pages and save them to Memgraph database
   - Generate new node and edge properties by Memgraph query modules
   - Create similarity relations
   - Create clusters
   - Create export files for Tableau
- [Application server](https://github.com/pospisilboh/Memgraph/tree/master/Forename/ForenameServer) implemented in Flask that provide services (web pages)
- Embedded the web pages in <a href="#Tableau">dashboards</a> of Tableau and Tableau Public
- Graph visualization by [D3.js](https://www.d3-graph-gallery.com/network)
- Public part of the solution consist of:
   - Application server hostet on:
      - [IBM Cloud Foundry](https://www.ibm.com/cloud/cloud-foundry) or
      - [GCP App Engine](https://cloud.google.com/appengine) or
      - [Amazon Lightsail](https://aws.amazon.com/lightsail/?sc_icampaign=pac_lightsail_root&sc_ichannel=ha&sc_icontent=awssm-1111&sc_iplace=signin&trk=ha_awssm-1111)
   - Memgraph database on [Memgraph Cloud](https://cloud.memgraph.com/login)
   - Tableau dashboards on [Tableau Public](https://public.tableau.com/en-us/s/about)

List of functions available in Memgraph Custom Query Module [text_util.py](https://github.com/pospisilboh/Memgraph/tree/master/Forename/Modules):

<p align="center">
   <img src="https://github.com/pospisilboh/Memgraph/blob/ccb16c9694d8aa85427848c5b59155647d6507a5/Forename/Images/Custom%20Query%20Module%20-%20text_util.png?raw=true" alt=" Memgraph Custom Query Module" width="900"/>
<p/>

<h2 id="architecture">Solution architecture</h2>

The solution is a mix of the following technologies and tools:
- [Amazon Lightsail](https://aws.amazon.com/lightsail/?sc_icampaign=pac_lightsail_root&sc_ichannel=ha&sc_icontent=awssm-1111&sc_iplace=signin&trk=ha_awssm-1111)
- [ArchiMate](https://pubs.opengroup.org/architecture/archimate3-doc/)
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Cypher](https://en.wikipedia.org/wiki/Cypher_(query_language))
- [D3.js](https://www.d3-graph-gallery.com/network)
- [DigitalOcean App Platform](https://docs.digitalocean.com/products/app-platform/)
- [Docker](https://www.docker.com/)
- [Docker Hub](https://hub.docker.com)
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
- [GCP App Engine](https://cloud.google.com/appengine)
- [Jupyter Notebook](https://jupyter.org/)
- [Memgraph](https://memgraph.com/)
- [Memgraph Lab](https://memgraph.com/product/lab)
- [Memgraph Cloud](https://cloud.memgraph.com/login)
- [IBM Cloud Foundry](https://www.ibm.com/cloud/cloud-foundry)
- [Python](https://www.python.org/)
- [SQL](https://cs.wikipedia.org/wiki/SQL)
- [Tableau](https://www.tableau.com/)
- [Tableau Public](https://public.tableau.com/en-us/s/about)
- [Visual Studio Code](https://code.visualstudio.com/)

<h3 id="architecture">Architecture diagram</h3>
<p align="center">
   <img src="https://github.com/pospisilboh/Memgraph/blob/f0cee46084bdc663a981c94d0a05192f7e5a70ec/Forename/Images/Architecture.png?raw=true" alt="Architecture" width="900"/>
<p/>

### External system
From an external system, we extracted `forenames` and their `degree`. Data for import are available as a *.csv file.
```csv
degree,forename
759,Drahomíra
10807,Jaroslav
8314,Hana
...
```

### Public web pages
Following public web pages were used for web scraping additional information (`gender`, `name day`, `nickname`) with the use of a Web Scraping framework by Python called [**Beautiful Soup**](https://www.crummy.com/software/BeautifulSoup/bs4/doc/):
- [https://www.kurzy.cz](https://www.kurzy.cz/kalendar/svatky/abecedni-seznam-jmen/) ... `forename`, `gender`, `name day`
- [http://www.e-horoskopy.cz](http://www.e-horoskopy.cz/vyznam-jmen.asp) ... `forename`, `gender`, `name day` and `nick names`
- [https://www.kdejsme.cz](https://www.kdejsme.cz/seznam/) ... `forename`
- [http://svatky.centrum.cz](http://svatky.centrum.cz/jmenny-seznam/?month=1&order=na) ... `forename`, `gender`, `name day`

> Every `forename` found on any web page is valid for us. We set a node property `valid = true`.

### Jupyter Notebook
The Python script in Jupyter Notebook using a graph database Memgraph. The purpose of [**Jupyter Notebook**](https://github.com/pospisilboh/Memgraph/blob/a3cdd22d5435bcbc51d80a6b5a14965024f03d2f/Forename/Jupyter/Memgraph_Forename.ipynb) is to prepare data for further processing:
- Load `forenames` and their `degree` from an external system (*.csv file)
- Data scrap additional information (`gender`, `name day`, `nicknames`) from public web pages with [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/).
- Forename anonymization should also be considered. Forenames might come with personal information such as email addresses, phone numbers, personal identification.
- Create similarity relations. We compare forenames by implemented functions in custom Query Module [**text_util.py**](https://github.com/pospisilboh/Memgraph/tree/master/Forename/Modules), and by that, we create relationships with an appropriate similarity `score`:
   - SIMILAR_FORENAME_COMPARED_STRING
   - SIMILAR_FORENAME_LEVENSHTEIN
   - SIMILAR_FORENAME_JAROWINKLER
   - SIMILAR_FORENAME_JARO
- Create forename clusters. The forename clusters are created with the function `weakly_connected_components.get()`. For each node, a new property `componentId` is created.
- Create a forename gender model. Prepare the forename gender data model to support forename gender recommendation:
   -  nodes with label `Gender` and `LastTwoChar`
   -  edges with type `HAS_GENDER` and `HAS_LAST_TWO_CHAR`
- Nodes and relations enrichement. With the Memgraph query modules calculate properties:
   - `betweenness centrality`, `pageRank` for nodes, 
   - `bridge` for relationships.
- Create export files for Tableau. The following two files are created:
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

### Memgraph database

#### Setting up Memgraph with Docker
To start implementing and testing our custom query module [**text_util.py**](https://github.com/pospisilboh/Memgraph/tree/master/Forename/Modules) in Memgraph, it is necessary to set up a Docker container first. We need to create and mount a volume to access the query modules directory. This directory contains all of the built-in query modules, and it’s where we can save new custom query modules, in our case, the `text_util.py` file. 
   
Create an empty directory module on your host machine and execute the following command:
```sh
docker volume create --driver local --opt type=none --opt device=~modules --opt o=bind modules
```

Now, we can start Memgraph and mount the created volume:
```sh
docker run -it --rm -v c:/modules:/mage/dist -p 7687:7687 -e MEMGRAPH="-query-execution-timeout-sec=0" memgraph
```
   
The file `text_util.py` should be in the `c:/modules` directory.

<p align="center">
   <img src="https://github.com/pospisilboh/Memgraph/blob/7b5ada238b7ff5487cfbb4555777b3fc4cbbca81/Forename/Images/Docker.png" alt="Memgraph in docker" width="400"/>
<p/>

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

### Memgraph database on Memgraph Cloud

We exported the database from the Memgraph database by Memgraph Lab (exported dataset file `graph.cypherl`) and by Memgraph Lab imported the database to the Memgraph Cloud. The Memgraph Cloud database is used by our Flask application server deployed to IBM Cloud Foundry.

### Flask Application Server
[**Flask**](https://flask.palletsprojects.com/en/2.0.x/) is a micro web framework written in Python and we used it for implementing [application server](https://github.com/pospisilboh/Memgraph/tree/master/Forename/ForenameServer) that provide services (web pages) that are consumed by Tableau dashboards. To be able visualize a graph a JavaScript library [**D3.js**](https://www.d3-graph-gallery.com/network) was used.

Description how to run our Python Flask application server on the local environment is [here](https://github.com/pospisilboh/Memgraph/blob/master/Forename/ForenameServer/README.md).

Implemented services are:
- `http://127.0.0.1:5000/get-cluster-recommendation?componentId=`
- `http://127.0.0.1:5000/get-forename-recommendation?forename=`
- `http://127.0.0.1:5000/forename-recommendation-form`
- `http://127.0.0.1:5000/get-forename-detail?id=`
- `http://127.0.0.1:5000/get-forenames-valid`
- `http://127.0.0.1:5000/get-graph-cluster/degree/bridge?componentId=`
- `http://127.0.0.1:5000/get-graph-gender?id=`
- `http://127.0.0.1:5000/set-forename-rule?rid=`
- `http://127.0.0.1:5000/get-forename-rule?id=`
- `http://127.0.0.1:5000/get-forenames-rules`

> Parameter `componentId` is a unique identificator of cluster.

> Parameter `id` is a unique identificator of node.

> Parameter `rid` is a unique identificator of edge.

> With  http://127.0.0.1:5000/set-forename-rule?rid= service, it is possible to create a repair rule definition in the database.

### Flask Application Server on IBM Cloud Foundry
As an industry-standard platform and a service (PaaS), Cloud Foundry ensures the fastest, easiest, and most reliable deployment of cloud-native applications, and it is the reason why we can deploy our Flask application server to IBM Cloud Foundry. 

Description of how to deploy the Python Flask application server on the IBM cloud foundry environment is [here](https://github.com/pospisilboh/Memgraph/blob/master/Forename/ForenameServer/README.md).

`cloud-provider` = `foremame-balanced-nyala-wk.eu-gb.mybluemix.net`

Available services are:
- https://{cloud-provider}/get-cluster-recommendation?componentId=
- https://{cloud-provider}/get-forename-detail?id=
- https://{cloud-provider}/get-forenames-valid
- https://{cloud-provider}/degree/bridge?componentId=
- https://{cloud-provider}/get-graph-gender?id=
- https://{cloud-provider}/set-forename-rule?rid=
- https://{cloud-provider}/get-forename-rule?id=
- https://{cloud-provider}/get-forenames-rules

> Following services are not supported because there is not possible to deploy our custom query module [**text_util.py**](https://github.com/pospisilboh/Memgraph/tree/master/Forename/Modules) to Memgraph Cloud:
> - https://{cloud-provider}/forename-recommendation-form
> - https://{cloud-provider}/get-forename-recommendation?forename=


> The Flask application server deployed on IBM Cloud Foundry uses the Memgraph Cloud database.

### Flask Application Server on Amazon Lightsail
Amazon Lightsail is a cloud platform that's cost-effective, fast, & reliable with an easy-to-use interface. It’s ideal for simpler workloads, quick deployments, and getting started on AWS.

Description how to deploy our Python Flask application server on the Amazon Lightsail environment is [here](https://github.com/pospisilboh/Memgraph/blob/master/Forename/ForenameServer/README.md).

`cloud-provider` = `forenames.jfm9cea2smhfs.eu-central-1.cs.amazonlightsail.com`

Available services are:
- https://{cloud-provider}/get-cluster-recommendation?componentId=
- https://{cloud-provider}/get-forename-detail?id=
- https://{cloud-provider}/get-forenames-valid
- https://{cloud-provider}/degree/bridge?componentId=
- https://{cloud-provider}/get-graph-gender?id=
- https://{cloud-provider}/set-forename-rule?rid=
- https://{cloud-provider}/get-forename-rule?id=
- https://{cloud-provider}/get-forenames-rules

> Following services are not supported because there is not possible to deploy our custom query module [**text_util.py**](https://github.com/pospisilboh/Memgraph/tree/master/Forename/Modules) to Memgraph Cloud:
> - https://{cloud-provider}/forename-recommendation-form
> - https://{cloud-provider}/get-forename-recommendation?forename=

> The Flask application server deployed on the Amazon Lightsail uses the Memgraph Cloud database.

### Flask Application Server on GCP App Engine
App Engine is a fully managed, serverless platform for developing and hosting web applications at scale. You can choose from several popular languages, libraries, and frameworks to develop your apps, and then let App Engine take care of provisioning servers and scaling your app instances based on demand.

Description how to deploy our Python Flask application server on the GCP App Engine (Flexible environment) environment is [here](https://github.com/pospisilboh/Memgraph/blob/master/Forename/ForenameServer/README.md).

`cloud-provider` = `forenames.ey.r.appspot.com`

Available services are:
- https://{cloud-provider}/get-cluster-recommendation?componentId=
- https://{cloud-provider}/get-forename-detail?id=
- https://{cloud-provider}/get-forenames-valid
- https://{cloud-provider}/degree/bridge?componentId=
- https://{cloud-provider}/get-graph-gender?id=
- https://{cloud-provider}/set-forename-rule?rid=
- https://{cloud-provider}/get-forename-rule?id=
- https://{cloud-provider}/get-forenames-rules

> Following services are not supported because there is not possible to deploy our custom query module [**text_util.py**](https://github.com/pospisilboh/Memgraph/tree/master/Forename/Modules) to Memgraph Cloud:
> - https://{cloud-provider}/forename-recommendation-form
> - https://{cloud-provider}/get-forename-recommendation?forename=

> The Flask application server deployed on the GCP App Engine uses the Memgraph Cloud database.

### Flask Application Server on DigitalOcean Apps Platform
App Platform is a Platform-as-a-Service (PaaS) offering that allows developers to publish code directly to DigitalOcean servers without worrying about the underlying infrastructure.

Description how to deploy our Python Flask application server on the DigitalOcean Apps Platform environment is [here](https://github.com/pospisilboh/Memgraph/blob/master/Forename/ForenameServer/README.md).

`cloud-provider` = `bobovo-forenameserver-forename-m3r47.ondigitalocean.app`

Available services are:
- https://{cloud-provider}/get-cluster-recommendation?componentId=
- https://{cloud-provider}/get-forename-detail?id=
- https://{cloud-provider}/get-forenames-valid
- https://{cloud-provider}/degree/bridge?componentId=
- https://{cloud-provider}/get-graph-gender?id=
- https://{cloud-provider}/set-forename-rule?rid=
- https://{cloud-provider}/get-forename-rule?id=
- https://{cloud-provider}/get-forenames-rules

> Following services are not supported because there is not possible to deploy our custom query module [**text_util.py**](https://github.com/pospisilboh/Memgraph/tree/master/Forename/Modules) to Memgraph Cloud:
> - https://{cloud-provider}/forename-recommendation-form
> - https://{cloud-provider}/get-forename-recommendation?forename=

> The Flask application server deployed on the DigitalOcean Apps Platform uses the Memgraph Cloud database.

<h3 id="Tableau dashboards">Tableau dashboards</h3>

Tableau is a powerful business intelligence and data visualization tool that has an intuitive user interface. In our case, we use Tableau as a user interface. Data sources for Tableau dashboards are:
- previously mentioned imported files `export_forename_nodes.csv` and `export_forename_relations.csv`,  
- services (embedded web pages) provided by Flask Application server.

#### Forename dashboard

The main dashboard gives a base overview of what data are available.

<p align="center">
   <img src="https://github.com/pospisilboh/Memgraph/blob/a0642f172e0fef04566bbce79cfdb96e21c5ee61/Forename/Images/Forename%20dashboard.png?raw=true" alt="Forename dashboard" width="900"/>
<p/>

> The count of valid forenames is low (only 29,51 %), but their degree is high (96,08 %). In other words, there are only `3,92 %` of wrong forenames.

> There are quite a few forenames with no definition of gender (97,62 %), but their degree is only 10.68 %.

> The most popular male name is Petr. The most popular female name is Jana.

<h4 id="Forenames clusters analyzer">Forenames clusters analyzer</h4>

This dashboard gives us a possibility to analyze forenames clusters:
- count and list of forenames in each cluster
- types of relationships in a cluster
- existing relationships between forenames and their similarity score

<p align="center">
   <img src="https://github.com/pospisilboh/Memgraph/blob/a0642f172e0fef04566bbce79cfdb96e21c5ee61/Forename/Images/Forenames%20clusters.png?raw=true" alt="Forenames clusters analyzer" width="900"/>
<p/>

> The count of forenames in the cluster is `20`.
> 
> The count of forename genders in the cluster is `2`.
> 
> The sum of forenames degree is `20 542`.
> 
> The biggest cluster consists of `25` forenames.
> 
> The forename with the highest degree in a cluster is a male forename `Michal`, and the second one is a female forename `Michaela`.

<h4 id="Forenames clusters graph analyzer">Forenames clusters graph analyzer</h4>

This dashboard gives the possibility to analyze forenames clusters visually:
- define node property (`betweenness`, `degre`, `pageRank`, `valid`)
- define edge property (`bridge`, `score`)
- scale nodes depending on defined node property
- scale edges depending on defined edge property
- hover over nodes or edges to get a pop-up with more information

<p align="center">
   <img src="https://github.com/pospisilboh/Memgraph/blob/a0642f172e0fef04566bbce79cfdb96e21c5ee61/Forename/Images/Forenames%20cluster%20graf.png?raw=true" alt="Forenames clusters graph analyzer" width="900"/>
<p/>

> In the graph, male forenames are blue, female forenames are yellow, and forenames without defined gender are grey.

<h4 id="Forename recommendation">Forename recommendation</h4>

This dashboard gives us a possibility to:
- get recommended forenames for a defined forename using the selected methods (compareStr, levenshteinSimilarity, jaroDistance, jaroWinklerDistance).

<p align="center">
   <img src="https://github.com/pospisilboh/Memgraph/blob/a0642f172e0fef04566bbce79cfdb96e21c5ee61/Forename/Images/Foremame%20recommender.png?raw=true" alt="Forename recommedation" width="900"/>
<p/>

> The defined name may not exist in the database.

> The list of recommended forenames is ordered by `valid`, `score` DESC, `degree` DESC.

<h4 id="Forename gender recommendation">Forename gender recommendation</h4>

This dashboard gives us a possibility to:
- generate a forename gender recommendation graph for a selected forename 

<p align="center">
   <img src="https://github.com/pospisilboh/Memgraph/blob/a0642f172e0fef04566bbce79cfdb96e21c5ee61/Forename/Images/Forename%20gender%20recommender.png?raw=true" alt="Forename gender recommedation" width="900"/>
<p/>

> On the graph, there are nodes with the label **LastTwoChar** that represent the last two characters in forenames. Some of them are:
> - part of only male forenames (blue),
> - part of only female forenames (yellow),
> - part of both male and female forenames (grey).

> Using the generated recommendation graph for a selected forename `Dennis`, we get a recommendation that `Dennis` is a `male` forename.

<h4 id="Forename repair rules recommendation">Forename repair rules recommendation</h4>

This dashboard gives the possibility:
- for a selected forename get repair rule definition (node with label Rule) by the Tableau action `Get forename rule`
- for a selected forename create repair rule definition (node with label Rule) by the Tableau action `Set forename rule`

<p align="center">
   <img src="https://github.com/pospisilboh/Memgraph/blob/a93003f527596fb0b20dd393bca21ff3261b277c/Forename/Images/Forenames%20similarity.png?raw=true" alt="Forenames similarity" width="900"/>
<p/>

> By a recommendation:
> - by the similarity relation type `SIMILAR_FORENAME_COMPARED_STRING` we can create forename repair rules that can repair `8 641` forenames in the external system
> - by the similarity relation type `SIMILAR_FORENAME_LEVENSHTEIN` we can create forename repair rules that can repair `2 023` forenames in the external system
> - by the similarity relation type `SIMILAR_FORENAME_JAROWINKLER`) we can create forename repair rules that can repair `4 464` forenames in the external system
> - by the similarity relation type `SIMILAR_FORENAME_JARO`) we can create forename repair rules that can repair `1 885` forenames in the external system

> Functionality to export all created forename repair rules in a form of `Sql` or `Cypher` scripts is available via the dashboard `Forename repair rules getter`.

<h4 id="Forename repair rules getter">Forename repair rules getter</h4>

This dashboard gives the possibility to:
- list all defined forename repair rules
- download `Sql` or `Cypher` script with forename repair rules

<p align="center">
   <img src="https://github.com/pospisilboh/Memgraph/blob/a0642f172e0fef04566bbce79cfdb96e21c5ee61/Forename/Images/Forename%20repair%20rules.png?raw=true" alt="Forename repair rules" width="900"/>
<p/>

### Tableau dashboards on Tableau Public

[Tableau Public](https://public.tableau.com/en-us/s/about) is a free platform to publicly share and explore data visualizations online. Anyone can create visualizations using either Tableau Desktop Professional Edition or the free Public Edition. 

Publish the [dashboards](https://public.tableau.com/app/profile/bobovo.eu/viz/Forenames_20211216/Forenamedashboard) from local Tableau Desktop Professional Edition to a Tableau Public is a way how to share our dashboards with others publicly.

> Some functionalities of dashboards are limited, in Memgraph Cloud database there aren't available functionalities of our custom Query Module [**text_util.py**](https://github.com/pospisilboh/Memgraph/tree/master/Forename/Modules).

<h2 id="data-model">Data model</h2>

### Data model diagram
<p align="center">
   <img src="https://github.com/pospisilboh/Memgraph/blob/58cbaa5780df48841b542f0e10e77dd080c6eec5/Forename/Images/Data%20model.png?raw=true" alt="Custom Query Module - text_util" width="900"/>
<p/>

### Nodes definition

| Label      | Property | Description |
| :---        |    :----   | :---- |
| Forename | value | Forename from source system. |
| Forename | degree | Forename `degree` (how often the forename is used in a source system) from a source system. |
| Forename | valid | true ... if the forename was found in web pages used for scraping. |
| Forename | gender | From web pages used for scraping. M ... Male, F ... Female.  |
| Forename | nameDay | From web pages used for scraping. DD.MM. |
| Forename | nameDayDay | Value of day (DD) extracted from `nameDay`. |
| Forename | nameDayMonth | Value of month (MM) extracted from `nameDay`. |
| Forename | nickNames | From web pages used for scraping. List of nicknames for the forename. |
| Forename | origin | From web pages used for scraping. Forename `origin` can be one of the following values: Itálie, Severské země, anglický, anglosaský, aramejský, francouzský, germánský, hebrejský, hebrejský, holandský,	italský, jihoslovanský,	keltský, latinský,	maďarský, nejasný, německý, orientální, perský, polský, ruský |
| Forename | source | Forename was found in web pages used for scraping. Source web pages for scraping are: www.kurzy.cz, www.e-horoskopy.cz, www.kdejsme.cz,  www.svatky.centrum.cz |
| Forename | normalizedValue | Property created by function `text_util.normalizeStr(value, 'cz')` from [**text_util.py**](https://github.com/pospisilboh/Memgraph/tree/master/Forename/Modules). |
| Forename | valueNumberCount | Property created by function `text_util.getNumbersFromStr(value)` from [**text_util.py**](https://github.com/pospisilboh/Memgraph/tree/master/Forename/Modules) |
| Forename | componentId | The WCC algorithm finds sets of connected nodes in an undirected graph, where all nodes in the same set form a connected component. WCC is often used early in an analysis to understand the structure of a graph. Clusters are created by WCC algorithm `weakly_connected_components.get()`. |
| Forename | betweenness | Betweenness centrality is a way of detecting the amount of influence a node has over the flow of information in a graph. It is often used to find nodes that serve as a bridge from one part of a graph to another. Property created by algorithm `betweenness_centrality.get(FALSE,FALSE)`. |
| Forename | pageRank | The PageRank algorithm measures the importance of each node within the graph, based on the number incoming relationships and the importance of the corresponding source nodes. The underlying assumption roughly speaking is that a page is only as important as the pages that link to it. Property created by algorithm  `pagerank.get()`. |
| Forename | anonymized | Can be false/true |
| Forename | anonymizationRule | Identification of rule based on which it was evaluated that anonymization will be performed. |
| Rule | property | A node property name to which the rule will be applied (property: "value"). |
| Rule | source | Source value (source: "Adéla"). |
| Rule | target | Target value (target: "ADéla"). |
| Rule | type | Name of rule type (type: "forename_value"). |
| Gender | value | Value of gender. Can be M ... Male, F ... Female |
| LastTwoChar | value | Value of two last characters from forename created by function `text_util.substring(text, start, end, step)` from [**text_util.py**](https://github.com/pospisilboh/Memgraph/tree/master/Forename/Modules). |
| LastTwoChar | genderDegree | Can be 1 ... the two last characters are part of only male or only female forenames or 2 ... the two last characters are part of male and female forenames too. |

### Relationships definition

| Type      | Property | Description |
| :---        |    :----   | :---- |
| SIMILAR_FORENAME_COMPARED_STRING | score | 0 ... not similar, 1 ... similar |
| SIMILAR_FORENAME_COMPARED_STRING | bridge | A bridge in the graph can be described as an edge which if deleted, creates two disjoint graph components. Property created by algorithm `bridges.get()`. |
| SIMILAR_FORENAME_LEVENSHTEIN | score | Property created by function `text_util.levenshteinSimilarity(text1, text2)` from [**text_util.py**](https://github.com/pospisilboh/Memgraph/tree/master/Forename/Modules). |
| SIMILAR_FORENAME_LEVENSHTEIN | bridge | A bridge in the graph can be described as an edge which if deleted, creates two disjoint graph components. Property created by algorithm `bridges.get()`. |
| SIMILAR_FORENAME_JAROWINKLER | score | Property created by function `text_util.jaroWinklerDistance(text1, text2)` from [**text_util.py**](https://github.com/pospisilboh/Memgraph/tree/master/Forename/Modules). |
| SIMILAR_FORENAME_JAROWINKLER | bridge | A bridge in the graph can be described as an edge which if deleted, creates two disjoint graph components. Property created by algorithm `bridges.get()`. |
| SIMILAR_FORENAME_JARO | score | Property created by function `text_util.jaroDistance(text1, text2)` from [**text_util.py**](https://github.com/pospisilboh/Memgraph/tree/master/Forename/Modules). |
| SIMILAR_FORENAME_JARO | bridge | A bridge in the graph can be described as an edge which if deleted, creates two disjoint graph components. Property created by algorithm `bridges.get()`. |
| DEFINED_BY | type | Type can be source or target. |
| HAS_LAST_TWO_CHAR | degree | Nodes with label `Forename` or `Gender` can have relation `HAS_LAST_TWO_CHAR` to node with label `LastTwoChar`. |
| HAS_GENDER |  | Nodes with label `Forename` can have relation `HAS_GENDER` to node with label `Gender`. |

<h2 id="sources">Additional Resources</h2>

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
