# Table of Contents

<div class="alert alert-block alert-info" style="margin-top: 20px">

<font size = 3>

1. <a href="#Flask Application Server">Flask Application Server</a>
2. <a href="#Flask Application Server on the local">Flask Application Server on the local</a>
3. <a href="#Flask Application Server on the IBM Cloud Foundry">Flask Application Server on the IBM Cloud Foundry</a>
4. <a href="#Flask Application Server on Amazon Lightsail">Flask Application Server on Amazon Lightsail</a>
5. <a href="#Flask Application Server on the GCP App Engine">Flask Application Server on the GCP App Engine</a>
6. <a href="#Flask Application Server on the DigitalOcean Apps">Flask Application Server on the DigitalOcean Apps</a>	
</font>
</div>

<h1 id="Flask Application Server">Flask Application Server</h1>

[**Flask**](https://flask.palletsprojects.com/en/2.0.x/) is a micro web framework written in Python and we used it for implementing services that are consumed by Tableau or Tableau Public dashboards. To be able visualize a graph a JavaScript library [**D3.js**](https://www.d3-graph-gallery.com/network) was used.

## OpenAPI definition 

An OpenAPI definition can then be used by documentation generation tools to display the API, code generation tools to generate servers and clients in various programming languages, testing tools, and many other use cases. 

The OpenAPI definition of our application server services is available [here](https://github.com/pospisilboh/Memgraph/blob/bfb4d6a65fdef8071eed386b575d9ae9a5dfb030/Forename/ForenameServer/openApi.yaml).

<p align="center">
   <img src="https://github.com/pospisilboh/Memgraph/blob/ecb14f1466e1a5cc865ecf6532d89319dd413cc6/Forename/Images/Open%20Api.png?raw=true" alt="OpenAPI definition "/>
<p/>

## Example results of implemented services
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


<h1 id="Flask Application Server on the local">Flask Application Server on the local</h1>

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

## Add libraries (requirements.txt)
Add libraries to file `requirements.txt`. If you want other libraries, just add them.
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

## Dockerfile (Dockerfile)
```dockerfile
FROM python:3.8

# Install CMake
RUN apt-get update && \
  apt-get --yes install cmake && \
  rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

# Copy the source code
COPY . /app

RUN mkdir -p /app/download

WORKDIR /app

# Set the environment variables
ENV FLASK_ENV=development
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Start the web application
ENTRYPOINT ["python3", "app.py"]
```

## Docker Compose (docker-compose.yml)
Compose is a tool for defining and running multi-container Docker applications. With Compose, you use a YAML file to configure your application's services. 

```yml
version: '3'
services:
  forename:
    build: .
    volumes:
      - .:/app
    ports:
      - "5000:5000"
    environment:
      MG_HOST: 3.70.198.85
      MG_PASSWORD: ***
      MG_PORT: 7687
      MG_USERNAME: ***@***.com
```

Description how to run our Python Flask application server on the local.

```
docker-compose build
```

```
docker-compose up
```

<h1 id="Flask Application Server on the IBM Cloud Foundry">Flask Application Server on the IBM Cloud Foundry</h1>

Description how to deploy our Python Flask application server on the IBM cloud foundry environment.

## Manifest (manifest.yml)
This is so simple application that it does not need much resources. Please make sure don???t allocate much resources.
```yml
applications:
  - name: Foremame
    random-route: true
    memory: 128M
    buildpacks:
    - python_buildpack
```

## Commands run the application (Procfile)
Here just write down a command, which runs `app.py` application.
```py
web: python app.py
```

## Deploy the application to cloud foundry
We use the IBM?? Cloud Foundry command-line interface (CLI) to download, modify, and redeploy our Cloud Foundry apps and service instances.

Before you begin, download and install the IBM Cloud [CLI](https://cloud.ibm.com/docs/cli?topic=cli-getting-started).

Log in to IBM Cloud with your IBMid:
```
ibmcloud login
```
To access Cloud Foundry services, we must specify a Cloud Foundry `org` and `space`:
```
ibmcloud target -o <org name> -s <space name>
```
From <your_new_directory>, redeploy your app to IBM Cloud by using the following command:
```
ibmcloud cf push
```
Access our app by browsing to the app URL.

## Define environment variables

User defined variables are:
- `MG_HOST`, 
- `MG_PASSWORD`, 
- `MG_PORT`, 
- `MG_USERNAME`

<p align="center">
   <img src="https://github.com/pospisilboh/Memgraph/blob/3951d2a40f953d6f8d44fb228b9483fc3afc5be3/Forename/Images/Cloud%20foundry%20-%20variables.png?raw=true" alt="User defined variables"/>
<p/>

<h1 id="Flask Application Server on Amazon Lightsail">Flask Application Server on Amazon Lightsail</h1>

Amazon Lightsail is a cloud platform that's cost-effective, fast, & reliable with an easy-to-use interface. It???s ideal for simpler workloads, quick deployments, and getting started on AWS.

Use `docker image push` to share your images to the [Docker Hub](https://hub.docker.com) registry:
```
docker push bobovo/forenameserver_forename:latest
```

Description how to deploy our Python Flask application server on the on Amazon Lightsail environment.

<p align="center">
   <img src="https://github.com/pospisilboh/Memgraph/blob/20c7f53358ab93b01a1ad2e6274ba73d16e4a975/Forename/Images/Amazon%20Lightsail.png?raw=true" alt="Amazon Lightsail"/>
<p/>

<h1 id="Flask Application Server on the GCP App Engine">Flask Application Server on the GCP App Engine</h1>

App Engine is a fully managed, serverless platform for developing and hosting web applications at scale. You can choose from several popular languages, libraries, and frameworks to develop your apps, and then let App Engine take care of provisioning servers and scaling your app instances based on demand.

Description how to deploy our Python Flask application server on the GCP App Engine (Flexible environment) environment.

## Configuration File (app.yml)
You configure your App Engine app's settings in the app.yaml file. The app.yaml file also contains information about your app's code, such as the runtime and the latest version identifier.
```yml
runtime: custom
env: flex
#entrypoint: gunicorn -b :$PORT -b :5000 main:app

env_variables:
  MG_HOST: "3.70.198.85"
  MG_PASSWORD: "***"
  MG_PORT: "7687"
  MG_USERNAME: "***@***.***"
```

## Create a Python app in the App Engine Flexible Environment

In Cloud Shell, configure gcloud to use your project:
```
gcloud config set project forenames
```
Enable App Engine:
```
gcloud app create
```
Instead of creating a new app, clone app from GitHub.
```
git clone https://github.com/pospisilboh/Memgraph.git
```
To explore the app's source files, open the app's directory in the Cloud Shell Editor:
```
cloudshell workspace Memgraph/Forename/ForenameServer/
```
Deploy the app:
```
gcloud app deploy /home/pospisil_boh/Memgraph/Forename/ForenameServer/app.yaml
```
View and monitor the app:
```
gcloud app browse
```

<h1 id="Flask Application Server on the DigitalOcean Apps">Flask Application Server on the DigitalOcean Apps</h1>
App Platform is a Platform-as-a-Service (PaaS) offering that allows developers to publish code directly to DigitalOcean servers without worrying about the underlying infrastructure.

## doctl

[doctl](https://docs.digitalocean.com/reference/doctl/) is the official DigitalOcean command line interface (CLI). `doctl` allows you to interact with the DigitalOcean API via the command line. It supports most functionality found in the control panel. You can create, configure, and destroy DigitalOcean resources like Droplets, Kubernetes clusters, firewalls, load balancers, database clusters, domains, and more.

## YAML File (bobovo-forenameserver-forename.yaml)
As an alternative to configuring your app in the control panel, you can define an app specification using YAML and use `doctl`.

```yml	
alerts:
- rule: DEPLOYMENT_FAILED
- rule: DOMAIN_FAILED
name: bobovo-forenameserver-forename
region: fra
services:
- envs:
  - key: MG_HOST
    scope: RUN_AND_BUILD_TIME
    value: 3.70.198.85
  - key: MG_PASSWORD
    scope: RUN_AND_BUILD_TIME
    value: ***
  - key: MG_PORT
    scope: RUN_AND_BUILD_TIME
    value: "7687"
  - key: MG_USERNAME
    scope: RUN_AND_BUILD_TIME
    value: ***@***com
  http_port: 5000
  image:
    registry: bobovo
    registry_type: DOCKER_HUB
    repository: forenameserver_forename
    tag: latest
  instance_count: 1
  instance_size_slug: basic-xxs
  name: bobovo-forenameserver-forename
  routes:
  - path: /
  source_dir: /
  cors:
    allow_headers:
    - '*'
    allow_methods:
    - GET
    - OPTIONS
    - POST
    - PUT
    - PATCH
    - DELETE
    allow_origins:
    - prefix: '*'
```

[Create](https://docs.digitalocean.com/reference/doctl/reference/apps/create/) an app with the given app spec:
```
octl apps create --spec {path}\bobovo-forenameserver-forename.yaml
```

[List](https://docs.digitalocean.com/reference/doctl/reference/apps/list/) all apps:
```
doctl apps list
```

[Update](https://docs.digitalocean.com/reference/doctl/reference/apps/update/) the specified app with the given app spec:
```
doctl apps update bf8e3538-e5f5-450b-b98b-40ab0d34b32e --spec {path}\bobovo-forenameserver-forename.yaml
```
