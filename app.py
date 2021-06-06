import time

import redis
from flask import Flask
from flask import render_template,request, jsonify, make_response
from flask_cors import CORS
import boto3
import json
from time import time, ctime

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)
count =0 


CORS(app)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/hello')
def hello():
    count = get_hit_count()
    return 'Hello World! I have been seen ' + str(count)+'times.\n'

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
