# Flask

[**Flask**](https://flask.palletsprojects.com/en/2.0.x/) is a micro web framework written in Python and we used it for implementing services that are consumed by Tableau dashboards. To be able visualize a graph a JavaScript library [**D3.js**](https://www.d3-graph-gallery.com/network) was used.

Implemented services are:
- http://127.0.0.1:5000/get-cluster-recommendation?componentId=

```json
[
  {
    "clusterDegree": 8371, 
    "clusterSize": 4, 
    "degrees": [
      8314, 
      43, 
      11, 
      3
    ], 
    "forenames": [
      "Hana", 
      "hana", 
      "HANA", 
      "HAna"
    ], 
    "recommendation": "Hana", 
    "valid": [
      true, 
      "N/A", 
      "N/A", 
      "N/A"
    ]
  }
]
```

- http://127.0.0.1:5000/get-forename-recommendation?forename=

```json
[
  {
    "componentId": 372, 
    "degree": 30, 
    "forename": "Bohu", 
    "gender": null, 
    "nickNames": null, 
    "recommendation": "Bohu\u0161", 
    "score": 0.8, 
    "valid": true
  }, 
  {
    "componentId": 2204, 
    "degree": 4, 
    "forename": "Bohu", 
    "gender": null, 
    "nickNames": null, 
    "recommendation": "Bohus", 
    "score": 0.8, 
    "valid": true
  }
]
```

- http://127.0.0.1:5000/forename-recommendation-form

<p align="center">
   <img src="https://github.com/pospisilboh/Memgraph/blob/b23b6e8d4c05e8db0ddd653196ef70645a9edac8/Forename/Images/forename-recommendation-form.png?raw=true" alt="forename-recommendation-form"/>
<p/>

- http://127.0.0.1:5000/get-forename-detail?id=

<p align="center">
   <img src="https://github.com/pospisilboh/Memgraph/blob/b23b6e8d4c05e8db0ddd653196ef70645a9edac8/Forename/Images/get-forename-detail.png?raw=true" alt="get-forename-detail"/>
<p/>

- http://127.0.0.1:5000/get-forenames-valid

<p align="center">
   <img src="https://github.com/pospisilboh/Memgraph/blob/a626dcf3851f3b5e59410e6ca4d551530faec147/Forename/Images/get-forenames-valid.png?raw=true" alt="get-forenames-valid"/>
<p/>

- http://127.0.0.1:5000/get-graph-cluster/degree/bridge?componentId=

<p align="center">
   <img src="https://github.com/pospisilboh/Memgraph/blob/b23b6e8d4c05e8db0ddd653196ef70645a9edac8/Forename/Images/get-graph-cluster.png?raw=true" alt="get-graph-cluster"/>
<p/>

- http://127.0.0.1:5000/get-graph-gender?id=

<p align="center">
   <img src="https://github.com/pospisilboh/Memgraph/blob/b23b6e8d4c05e8db0ddd653196ef70645a9edac8/Forename/Images/get-graph-gende.png?raw=true" alt="get-graph-gender"/>
<p/>

- http://127.0.0.1:5000/set-forename-rule?rid=
- http://127.0.0.1:5000/get-forename-rule?id=

<p align="center">
   <img src="https://user-images.githubusercontent.com/64272508/146419941-9cc01cd8-4ef5-4263-b2b2-5512cd106f6e.png?raw=true" alt="set-forename-rule"/>
<p/>

- http://127.0.0.1:5000/get-forenames-rules

<p align="center">
   <img src="https://github.com/pospisilboh/Memgraph/blob/a626dcf3851f3b5e59410e6ca4d551530faec147/Forename/Images/get-forenames-rules.png?raw=true" alt="get-forenames-rules"/>
<p/>

> Parameter `componentId` is unique identificator of cluster.

> Parameter `id` is unique identificator of node.

> Parameter `rid` is unique identificator of edge.

> By the web service http://127.0.0.1:5000/set-forename-rule?rid= is possible to create rule in the database.
