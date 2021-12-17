from flask import Flask, render_template, request, jsonify, make_response, send_from_directory
from forename.database import Memgraph
from forename import db_operations

from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, FloatField, SubmitField
from wtforms.validators import DataRequired

from forename.recommendation import RecommendationForm

import json
import csv
import os
import datetime

app = Flask(__name__)

# Flask-WTF requires an encryption key - the string can be anything
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'

# http://127.0.0.1:5000/get-cluster-recommendation?componentId=
@app.route('/get-cluster-recommendation', methods=["POST", "GET"])
def get_cluster_recommendation():

    componentId = request.args.get('componentId', default = 0, type = int)
    
    db = Memgraph()
    response = make_response(
        jsonify(db_operations.get_cluster_recommendation(db, {'componentId': componentId})), 200)
    return response

# http://127.0.0.1:5000/get-forename-recommendation?forename=
@app.route('/get-forename-recommendation')
def get_forename_recommendation():
    forename = request.args.get('forename', default = '', type = str)
    method = request.args.get('method', default = 'levenshteinSimilarity', type = str)
    similarityMin = request.args.get('similarityMin', default = 0.7, type = float)
    degree = request.args.get('degree', default = 2, type = int)

    db = Memgraph()
    response = make_response(
        jsonify(db_operations.get_forename_recommendation(db, {'method': method, 'similarityMin': similarityMin, 'forename': forename, 'degree': degree})), 200)
    return response

# http://127.0.0.1:5000/forename-recommendation-form
@app.route('/forename-recommendation-form', methods=['GET', 'POST'])
def forename_recommendation_form():
    form = RecommendationForm()
    message = ""
    if form.validate_on_submit():
        forename = form.forename.data
        method = form.method.data
        similarityMin = form.similarityMin.data 
        degree = request.args.get('degree', default = 2, type = int)

        db = Memgraph()
        recommendations = db_operations.get_forename_recommendation(db, {'method': method, 'similarityMin': similarityMin, 'forename': forename, 'degree': degree})

        return render_template('forename-recommendation.html', form=form, forename=forename, recommendations=recommendations)

    return render_template('forename-recommendation.html', form=form)

# http://127.0.0.1:5000/get-forename-detail?id=
@app.route('/get-forename-detail')
def get_forename_detail():
    id = request.args.get('id', default = 1, type = int)
    db = Memgraph()

    return render_template('forename_detail.html', title='Forename details', forename = db_operations.get_forename_detail(db, {'id': id}))

# http://127.0.0.1:5000/set-forename-rule?rid=
@app.route('/set-forename-rule', methods=["GET"])
def set_forename_rule():
    rid = request.args.get('rid', default = -1, type = int)
    db = Memgraph()

    return render_template('forename_rule.html', title='Forename replace rule', rule = db_operations.set_forename_rule(db, {'rid': rid}))

# http://127.0.0.1:5000/get-forename-rule?id=
@app.route('/get-forename-rule', methods=["GET"])
def get_forename_rule():
    id = request.args.get('id', default = 1, type = int)
    db = Memgraph()

    return render_template('forename_rule.html', title='Forename replace rule', rule = db_operations.get_forename_rule(db, {'id': id}))

# http://127.0.0.1:5000/delete-forename-rule?id=   - doesn't work
@app.route('/delete-forename-rule', methods=["GET"])
def delete_forename_rule():
    id = request.args.get('id', default = 1, type = int)
    db = Memgraph()

    db_operations.delete_forename_rule(db, {'id': id})

    return render_template('forename_rule.html', title='Forename replace rule', rule = db_operations.get_forename_rule(db, {'id': id}))

# http://127.0.0.1:5000/get-forenames-rules
@app.route('/get-forenames-rules', methods=["GET"])
def get_forenames_rules():
    db = Memgraph()
    rules = db_operations.get_forenames_rules(db)

    timestamp_string = str(datetime.datetime.now().strftime("%Y-%m-%d %H%M%S"))

    # generate some file name   
    filename_sql_rules = 'sql_rules ' + timestamp_string + '.csv'
    document_path = os.getcwd() + '\\download\\' + filename_sql_rules

    with open(document_path, 'w', newline="", encoding='UTF-16') as file:
        csvwriter = csv.writer(file) # create a csvwriter object
        for x in rules:
            csvwriter.writerow([x['sql']]) # write the rest of the data

    filename_cypher_rules = 'cypher_rules ' + timestamp_string + '.csv'
    document_path = os.getcwd() + '\\download\\' + filename_cypher_rules

    with open(document_path, 'w', newline="", encoding='UTF-16') as file:
        csvwriter = csv.writer(file) # create a csvwriter object
        for x in rules:
            csvwriter.writerow([x['cypher']]) # 5. write the rest of the data

    return render_template('forenames_rules.html', rules = rules, filename_sql_rules=filename_sql_rules, filename_cypher_rules=filename_cypher_rules), 200

# http://127.0.0.1:5000/get-forenames-valid
@app.route('/get-forenames-valid', methods=["GET"])
def get_forenames_valid():
    db = Memgraph()
    forenames = db_operations.get_forenames_valid(db)
    
    timestamp_string = str(datetime.datetime.now().strftime("%Y-%m-%d %H%M%S"))

    # generate some file name   
    filename_sql_valid = 'sql_valid ' + timestamp_string + '.csv'
    document_path = os.getcwd() + '\\download\\' + filename_sql_valid
 
    with open(document_path, 'w', newline="", encoding='UTF-16') as file:
        csvwriter = csv.writer(file) # create a csvwriter object
        for x in forenames:
            csvwriter.writerow([x['sql']]) # write the rest of the data

    # generate some file name
    filename_cypher_valid = 'cypher_valid ' + timestamp_string + '.csv'
    document_path = os.getcwd() + '\\download\\' + filename_cypher_valid

    with open(document_path, 'w', newline="", encoding='UTF-16') as file:
        csvwriter = csv.writer(file) # create a csvwriter object
        for x in forenames:
            csvwriter.writerow([x['cypher']]) # write the rest of the data

    return render_template('forenames_valid.html', forenames = forenames, filename_sql_valid=filename_sql_valid, filename_cypher_valid=filename_cypher_valid), 200

@app.route('/download/<filename>')
def export_download(filename):
    return send_from_directory('download', filename)

# http://127.0.0.1:5000/get-graph-cluster/<nodeProperty>/<relationProperty>?componentId=
# http://127.0.0.1:5000/get-graph-cluster/degree/bridge?componentId=18
@app.route("/get-graph-cluster/<nodeProperty>/<relationProperty>", methods=["POST", "GET"])
def get_graph_cluster(nodeProperty=None, relationProperty=None):

    componentId = request.args.get('componentId', default = 0, type = int)

    db = Memgraph()
    data = db_operations.get_graph_cluster(db, {'componentId': componentId}, nodeProperty, relationProperty)

    data = json.loads(data)
    nodes = data['nodes']
    edges = data['links']
    
    return render_template('graph.html', nodeProperty=nodeProperty, relationProperty=relationProperty, nodes=nodes, edges=edges), 200

# http://127.0.0.1:5000/get-graph-gender?id=<id>
@app.route("/get-graph-gender", methods=["POST", "GET"])
def get_graph_gender():

    id = request.args.get('id', default = 1, type = int)
    db = Memgraph()
    
    # Get last two characters from forename defined by id
    data = db_operations.get_forename_detail(db, {'id': id})
    forename = data[0]['value']
    lastTwoChar = data[0]['normalizedValue'][-2:]

    data = db_operations.get_graph_gender(db, forename, lastTwoChar)

    data = json.loads(data)
    nodes = data['nodes']
    edges = data['links']
    
    return render_template('graph_gender.html', nodes=nodes, edges=edges), 200