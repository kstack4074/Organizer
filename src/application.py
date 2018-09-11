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
    table = DynamoTable('Organizer')
    return Response(json.dumps({'Words': table.getEverything()}), mimetype = 'application/json', status = 200)

@application.route('/update', methods = ['POST'])
def update_item():
    table = DynamoTable('Organizer')
    response = table.updateItem('Bike', 'Test1', {'Test2Key': 'Test2Val'})
    return Response(json.dumps(response, status = 200))

@application.route('/create', methods = ['POST'])
def create_item():
    req_dict = request.data
    req_dict = json.loads(req_dict)

    table_name = req_dict.get("Type")
    asset_table = DynamoTable("Asset")
    
    #Check if table name is real
    if table_name == None:
        #Bad request
        print("Bad request")

    table_info = req_dict.get("Info")
    table = DynamoTable(table_name)
    table.create_item(table_info)
    return Response(json.dumps(table_info))


if __name__ == '__main__':
    flaskrun(application)
