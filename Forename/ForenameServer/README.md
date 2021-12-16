# Flask

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
