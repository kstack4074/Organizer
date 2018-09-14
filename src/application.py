#!flask/bin/python
import json
from flask import Flask, Response, request

from src.flaskrun import flaskrun
from src.Dynamo.dynamo import DynamoTable

application = Flask(__name__)

@application.route('/', methods=['GET'])
def get():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)

@application.route('/', methods=['POST'])
def post():
    return Response(json.dumps({'Output': 'Hello World'}), mimetype='application/json', status=200)

@application.route('/fetchall', methods = ['GET'])
def get_everything():
    table = DynamoTable('Bike')
    return Response(json.dumps({'Words': table.get_everything()}), mimetype = 'application/json', status = 200)

@application.route('/create', methods = ['POST'])
def create_item():
    '''
    Application route to handle the creation of new elements in the database.
    This includes new rows (new key value) and new sub-fields in the nested
    document structure.

    New row is identifiable by 'Path' containing no '.'
    '''
    request_data = json.loads(request.data)

    table_name = request_data.get("Type")
    table = DynamoTable(table_name)
    table_info = request_data.get("Info")
    reponse = table.create_item(table_info["Path"], table_info["Value"])
    return Response(json.dumps(table_info), mimetype = 'application/json', status = 200)

@application.route('/read', methods = ['POST'])
def read_item():
    request_data = json.loads(request.data)
    table_name = request_data.get("Type")
    table = DynamoTable(table_name)
    table_info = request_data.get("Info")
    path = table_info["Path"]

    item = table.read_item(path)
    return Response(json.dumps(item), mimetype = 'application/json', status = 200)

@application.route('/update', methods = ['POST'])
def update_item():
    #Update Item needs to be able to:
    #   1. change the name of a record
    #   2. change the value of a record
    #   3. change the type of a record
    request_data = json.loads(request.data)
    table_name = request_data.get("Type")
    #Assume the table exists for now
    table = DynamoTable(table_name)
    table_info = request_data.get("Info")

    response = table.update_element(table_info["Path"], table_info["Value"])
    return Response(json.dumps(response), mimetype = 'application/json', status = 200)

@application.route('/delete', methods = ['POST'])
def delete_item():
    request_data = json.loads(request.data)
    table_name = request_data.get("Type")
    table = DynamoTable(table_name)
    table_info = request_data.get("Info")
    path = table_info["Path"]

    response = table.delete_element(table_info["Path"])

if __name__ == '__main__':
    flaskrun(application)