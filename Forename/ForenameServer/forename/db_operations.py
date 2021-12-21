from pathlib import Path
import json

def get_forenames(db):
    command = "MATCH (n) RETURN n LIMIT 100;"
    forenames = db.execute_and_fetch(command)

    forename_objects = []
    for user in forenames:
        u = user['n']
        data = {"value": u.properties['value'],
                "componentId": u.properties['componentId'],
                "degree": u.properties['degree'],
                "betweenness": u.properties['betweenness']
                }
        forename_objects.append(data)

    return json.dumps(forename_objects)

def get_realtionships(db):
    command = "MATCH (n1)-[r]-(n2) WHERE TYPE(r) CONTAINS 'SIMIL' RETURN n1,n2,r LIMIT 10;"
    relationships = db.execute_and_fetch(command)

    relationship_objects = []
    for relationship in relationships:
        n1 = relationship['n1']
        n2 = relationship['n2']
        r = relationship['r']

        data = {"forenameOne": n1.properties['value'],
                "forenameTwo": n2.properties['value'],
                "score": r.properties['score'],
                "type": r.type
                }
        relationship_objects.append(data)

    return json.dumps(relationship_objects)

def get_graph(db):
    command = "MATCH (n1)-[e]-(n2) WHERE TYPE(e) CONTAINS 'SIMIL' RETURN n1,n2,e LIMIT 100;"
    relationships = db.execute_and_fetch(command)

    link_objects = []
    node_objects = []
    added_nodes = []
    for relationship in relationships:
        e = relationship['e']
        data = {"source": e.nodes[0], "target": e.nodes[1]}
        link_objects.append(data)

        n1 = relationship['n1']
        if not (n1.id in added_nodes):
            data = {"id": n1.id, "value": n1.properties['value']}
            node_objects.append(data)
            added_nodes.append(n1.id)

        n2 = relationship['n2']
        if not (n2.id in added_nodes):
            data = {"id": n2.id, "value": n2.properties['value']}
            node_objects.append(data)
            added_nodes.append(n2.id)
    data = {"links": link_objects, "nodes": node_objects}

    return json.dumps(data)


def get_graph_cluster(db, params, nodeProperty, relationProperty):
    command = """
    MATCH (n1:Forename {componentId: $componentId})-[e]->(n2:Forename {componentId: $componentId}) RETURN n1, n2, e;
    """

    relationships = db.execute_and_fetch_params(command, params)

    link_objects = []
    node_objects = []
    added_nodes = []
    for relationship in relationships:
        e = relationship['e']
        if relationProperty == 'bridge':
            if not e.properties.__contains__(relationProperty):
                value = 0
            else:
                value = 1
            data = {"from": e.nodes[0], "to": e.nodes[1], "value": value, "title": relationProperty + ': ' + str(value), "color": "#7f7f7f"}
        else:
            data = {"from": e.nodes[0], "to": e.nodes[1], "value": e.properties['score'], "title": e.type + ': ' + str(e.properties['score']), "color": "#7f7f7f"}
        
        link_objects.append(data)

        n1 = relationship['n1']
        if not (n1.id in added_nodes):
            if n1.properties.__contains__('gender'):
                if n1.properties['gender'] == 'M':
                    color = "#4ba6ba"
                if n1.properties['gender'] == 'F':
                    color = "#f4d166"
            else:
                color = "#7f7f7f"

            if nodeProperty == 'valid':
                if not n1.properties.__contains__(nodeProperty):
                    value = 0
                else:
                    value = 1
                data = {"id": n1.id, "value": value, "title": nodeProperty + ': ' + str(value), "label": n1.properties['value'], "color": color}                
            else:
                data = {"id": n1.id, "value": n1.properties[nodeProperty], "title": nodeProperty + ': ' + str(n1.properties[nodeProperty]), "label": n1.properties['value'], "color": color}
            
            node_objects.append(data)
            added_nodes.append(n1.id)

        n2 = relationship['n2']
        if not (n2.id in added_nodes):
            if n2.properties.__contains__('gender'):
                if n2.properties['gender'] == 'M':
                    color = "#4ba6ba"
                if n2.properties['gender'] == 'F':
                    color = "#f4d166"
            else:
                color = "#7f7f7f"

            if nodeProperty == 'valid':
                if not n2.properties.__contains__(nodeProperty):
                    value = 0
                else:
                    value = 1
                data = {"id": n2.id, "value": value, "title": nodeProperty + ': ' + str(value), "label": n2.properties['value'], "color": color}
            else:
                data = {"id": n2.id, "value": n2.properties[nodeProperty], "title": nodeProperty + ': ' + str(n2.properties[nodeProperty]), "label": n2.properties['value'], "color": color}
            
            node_objects.append(data)
            added_nodes.append(n2.id)

    data = {"links": link_objects, "nodes": node_objects}

    return json.dumps(data)


def get_graph_gender(db, forename, lastTwoChar):
    command = """
    MATCH (n1:Feature)-[e:HAS_LAST_TWO_CHAR]->(n2) RETURN n1, n2, e;
    """

    relationships = db.execute_and_fetch(command)

    link_objects = []
    node_objects = []
    added_nodes = []
    for relationship in relationships:
        e = relationship['e']
        data = {"from": e.nodes[0], "to": e.nodes[1], "value": e.properties['degree'], "title": e.properties['degree']}
        link_objects.append(data)

        n1 = relationship['n1']
        if not (n1.id in added_nodes):

            if n1.properties['value'] == 'M':
                title = 'Male'
                data = {"id": n1.id, "value": 1, "title": title, "label": title, "color": "white", "color": "#4ba6ba", "borderWidth": 5}
            else:
                title = 'Female'
                data = {"id": n1.id, "value": 1, "title": title, "label": title, "color": "white", "color": "#f4d166", "borderWidth": 5}
            
            node_objects.append(data)
            added_nodes.append(n1.id)

        n2 = relationship['n2']
        if not (n2.id in added_nodes):
            if lastTwoChar == n2.properties['value']:
                title = n2.properties['value'] + '\n' + forename
                shape = 'ellipse'
            else:
                title = n2.properties['value']
                shape = 'box'

            if n2.properties['genderDegree'] == 2:
                data = {"id": n2.id, "value": 1, "title": title, "label": title, "color": "#7f7f7f", "shape": shape}
            else:
                if n1.properties['value'] == 'M':
                    data = {"id": n2.id, "value": 1, "title": title, "label": title, "color": "#4ba6ba", "shape": shape}
                else:
                    data = {"id": n2.id, "value": 1, "title": title, "label": title, "color": "#f4d166", "shape": shape}
            node_objects.append(data)
            added_nodes.append(n2.id)
    data = {"links": link_objects, "nodes": node_objects}

    return json.dumps(data)

def get_cluster_recommendation(db, params):
    command = """
    MATCH (i:Forename {componentId: $componentId})
    WITH i AS i, i.componentId AS cluster
    ORDER BY i.valid, i.degree DESC

    RETURN cluster, 
        SIZE(COLLECT(i.value)) AS clusterSize,
        SUM(i.degree) AS clusterDegree,
        COLLECT(i.value) AS forenames,
        COLLECT(i.degree) AS degrees,
        COLLECT(coalesce(i.valid, 'N/A')) AS valid,
        COLLECT(i.value)[0] AS recommendation
    ;"""

    recommendations = db.execute_and_fetch_params(command, params)

    recommendation_objects = []

    for recommendation in recommendations:
        data = {"clusterSize": recommendation['clusterSize'],
                "clusterDegree": recommendation['clusterDegree'],
                "forenames": recommendation['forenames'],
                "degrees": recommendation['degrees'],
                "valid": recommendation['valid'],
                "recommendation": recommendation['recommendation']
        }
        recommendation_objects.append(data)

    #rreturn json.dumps(recommendation_objects)
    return recommendation_objects

def get_forename_recommendation(db, params):

    command = """
    // Recommendation - Forename doesn‘t exist
    CALL text_util.normalizeStr($forename, 'cz') YIELD normalizedStr AS source

    MATCH (f:Forename)
    WHERE f.degree > $degree AND f.valid = true
      AND (SUBSTRING(f.normalizedValue, 0,1) = SUBSTRING(source, 0,1) 
      OR SUBSTRING(f.normalizedValue, 1,1) = SUBSTRING(source, 1,1)
      OR SUBSTRING(f.normalizedValue, 2,1) = SUBSTRING(source, 2,1))
    WITH f AS f, source

    CALL text_util.$method(f.normalizedValue, source) YIELD *
    WITH *
    WHERE score >= $similarityMin

    RETURN $forename AS source, 
        f.value AS recommendation, 
        f.gender AS gender, 
        f.valid AS valid, 
        score, 
        ToInteger(f.degree) AS degree,
        f.componentId AS componentId,
        f.nickNames AS nickNames

    ORDER BY f.valid, score DESC, f.degree DESC
    LIMIT 10
    """

    command = command.replace('$method', params['method'])

    recommendations = db.execute_and_fetch_params(command, params)

    recommendation_objects = []

    for recommendation in recommendations:
        data = {"forename": recommendation['source'],
                "recommendation": recommendation['recommendation'],
                "gender": recommendation['gender'],
                "valid": recommendation['valid'],
                "score": recommendation['score'],
                "degree": recommendation['degree'],
                "componentId": recommendation['componentId'],
                "nickNames": recommendation['nickNames']
        }
        recommendation_objects.append(data)

    #return json.dumps(recommendation_objects)
    return recommendation_objects


def set_forename_rule(db, params):
    command = """

    MATCH (n1:Forename)-[r]->(n2:Forename)
    WHERE r.id = $rid 

    WITH n1 AS n1, n2 AS n2

    OPTIONAL MATCH (oldrul:Rule)-[:DEFINED_BY {type: 'target'}]->(n2)

    DETACH DELETE oldrul
    
    WITH n1, n2

    MERGE (rule:Rule {type: 'forename_value', property: 'value', source: n1.value, target: n2.value})

    WITH n1, n2, rule AS rule

    MERGE (n1)<-[:DEFINED_BY {type: 'source'}]-(rule)
    MERGE (rule)-[:DEFINED_BY {type: 'target'}]->(n2)

    RETURN rule AS rule
    """

    rules = db.execute_and_fetch_params(command, params)

    rule_objects = []
    for rule in rules:
        detail = rule['rule']

        data = {"source": detail.properties['source'],
                "target": detail.properties['target']
                }
        rule_objects.append(data)

    return rule_objects

def get_forenames_rules(db):
    command = """
    MATCH (n:Rule) 
    RETURN n.source AS source, n.target AS target,
    "UPDATE Forename SET value = '" + n.source + "' WHERE value = '" + n.target + "'" AS sql,
    "MATCH (f:Forename {value: '" + n.target + "'}) SET f.value = '" + n.source + "' RETURN COUNT(*)" AS cypher
    ORDER BY n.source, n.target;
    """
    
    rules = db.execute_and_fetch(command)

    rule_objects = []
    for rule in rules:
        data = {"source": rule['source'],
                "target": rule['target'],
                "sql": rule['sql'],
                "cypher": rule['cypher']
                }
        rule_objects.append(data)

    return rule_objects

def get_forenames_valid(db):
    command = """
    MATCH (f1:Forename)
    WHERE f1.valid = true
    RETURN f1.value AS forename, 
    "UPDATE Forename SET valid = true WHERE value = '" + f1.value + "'" AS sql,
    "MATCH (f:Forename {value: '" + f1.value + "'}) SET f.valid = true RETURN COUNT(*)" AS cypher
    ORDER BY f1.value;
    """

    forenames = db.execute_and_fetch(command)

    forename_objects = []
    for forename in forenames:
        data = {"forename": forename['forename'],
                "sql": forename['sql'],
                "cypher": forename['cypher']
                }
        forename_objects.append(data)

    return forename_objects

def get_forename_detail(db, params):
    command = "MATCH (n:Forename) WHERE n.id = $id RETURN n;"
    forenames = db.execute_and_fetch_params(command, params)

    forename_objects = []
    for forename in forenames:
        u = forename['n']
        data = {
                "value": u.properties['value'],
                "normalizedValue": u.properties['normalizedValue'],
                "componentId": u.properties['componentId'],
                "degree": u.properties['degree'],
                "betweenness": u.properties['betweenness'],
                "pageRank": u.properties['pageRank']
                }
        forename_objects.append(data)

    return forename_objects

def get_forename_rule(db, params):
    command = "MATCH (rule:Rule)-[:DEFINED_BY {type: 'target'}]->(n:Forename) WHERE n.id = $id RETURN rule;"
    forenames = db.execute_and_fetch_params(command, params)

    forename_objects = []
    for forename in forenames:
        u = forename['rule']
        data = {"source": u.properties['source'],
                "target": u.properties['target']
                }
        forename_objects.append(data)

    return forename_objects

def delete_forename_rule(db, params):
    command = """
    MATCH (rule:Rule)-[:DEFINED_BY {type: 'target'}]->(n:Forename)
    WHERE n.id = $id
    DETACH DELETE rule
    RETURN COUNT(*);
    """
    
    a = db.execute_and_fetch_params(command, params)
