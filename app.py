import time

import redis
from flask import Flask
from flask import render_template,request, jsonify, make_response
from flask_cors import CORS
import boto3
import json
from time import time, ctime
import os


app = Flask(__name__)
count =0 


CORS(app)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})



@app.route('/')
def index():
    return render_template("index.html")



@app.route("/submitContact", methods=["POST"])
def submitContact():
    jsonFile = open('secrets.json')
    data = json.load(jsonFile)
    dynamodb = boto3.resource('dynamodb',region_name='us-east-1',aws_access_key_id= data["access"], aws_secret_access_key= data["secret"])
    req = request.get_json()
    contact = put_contact(req["email"],req["message"],req["name"],req["number"],dynamodb)
    print("Put movie succeeded:")
    print(req)
    res = make_response(jsonify({"message": contact}), 200)
    return res

### Functions
def put_contact(email, message, name, number, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('Tutorial')
    time_now = time()
    response = table.put_item(
       Item={
            'time': ctime(time_now),
            'name': name,
            'info': {
                'email': email,
                'number': number,
                'message': message,
            }
        }
    )
    return response


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
