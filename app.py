import time

import redis
from flask import Flask
from flask import render_template

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)
count =0 

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
    count = get_hit_count()
    return render_template("index.html")

@app.route('/hello')
def hello():
    return 'Hello World! I have been seen {} times.\n'.format(count)