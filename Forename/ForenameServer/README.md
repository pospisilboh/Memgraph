# Flask application

[**Flask**](https://flask.palletsprojects.com/en/2.0.x/) is a micro web framework written in Python and we used it for implementing services that are consumed by Tableau or Tableau Public dashboards. To be able visualize a graph a JavaScript library [**D3.js**](https://www.d3-graph-gallery.com/network) was used.

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

#  Flask application on the IBM cloud foundry environment
Description how to deploy our Python Flask application on the IBM cloud foundry environment.

## Flask application (app.py)
```py
from flask import Flask, render_template, request, jsonify, make_response, send_from_directory
from forename.database import Memgraph
from forename import db_operations
from forename.recommendation import RecommendationForm

import json
import csv
import os
import datetime

app = Flask(__name__)

...

# Port number is required to fetch from env variable
cf_port = os.getenv("PORT")

if __name__ == '__main__':
	if cf_port is None:
		app.run(host='0.0.0.0', port=5000, debug=True)
	else:
		app.run(host='0.0.0.0', port=int(cf_port), debug=True)
```


## Flask application (memgraph.py)
```py
import os
from typing import Any, Dict, Iterator
from forename.database.connection import Connection

__all__ = ('Memgraph',)


MG_HOST = os.getenv('MG_HOST', '127.0.0.1')
MG_PORT = int(os.getenv('MG_PORT', '7687'))
MG_USERNAME = os.getenv('MG_USERNAME', '')
MG_PASSWORD = os.getenv('MG_PASSWORD', '')
MG_ENCRYPTED = os.getenv('MG_ENCRYPT', 'false').lower() == 'true'
```

## Add Flask library to file “requirements.txt”
Add Flask library to file `requirements.txt`.  If you want other libraries, just add them.
```
certifi==2020.12.5
click==7.1.2
Flask==1.1.2
itsdangerous==1.1.0
Jinja2==2.11.3
MarkupSafe==1.1.1
numpy==1.19.2
pandas==1.2.3
python-dateutil==2.8.1
pytz==2021.1
six==1.15.0
Werkzeug==1.0.1
wincertstore==0.2
Flask-WTF>=0.14.2
gevent
pymgclient
```

## Manifest(manifest.yml)
This is so simple application that it does not need much resources.  Please make sure don’t allocate much resources.
```yml
applications:
  - name: Foremame
    random-route: true
    memory: 128M
    buildpacks:
    - python_buildpack
```

## Commands run the application(Procfile)
Here just write down a command, which runs `app.py` application.
```py
web: python app.py
```

## Deploy the application to cloud foundry
```
ibmcloud cf push
```

## Define environment variables

User defined variables are:
- `MG_HOST`, 
- `MG_PASSWORD`, 
- `MG_PORT`, 
- `MG_USERNAME`





