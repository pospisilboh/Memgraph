# Creating a Custom Query Module
 
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