import ast

from pymongo import MongoClient
from redis import Redis
from flask import Flask, request, jsonify
from pymemcache.client.base import Client
import os
import sys


app = Flask(__name__)
REDIS_HOST = os.environ.get('REDIS_HOST', '84.201.155.228')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
MONGO_HOST = os.environ.get('MONGO_HOST', '84.201.155.228')
app.config["MONGO_URI"] = "mongodb://{mongo_host}:27017/flask".format(mongo_host=MONGO_HOST)
app.config['MONGO_DBNAME'] = 'dashboard'
mongo = MongoClient(app)
cache = Redis(host=REDIS_HOST, port=REDIS_PORT)
#config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': 'redis://{redis_host}:6379/0'.format(redis_host=REDIS_HOST)})


@app.route('/message/<message_id>', methods=['GET'])
def index_get(message_id):
    res = cache.get(message_id)
    if res is None:
        res = mongo.db.dashboard.find_one_or_404(message_id)
    return jsonify({'ok': True, 'message': 'Message found  % s ' % res}), 200


@app.route('/message', methods=['POST'])
def index_post():
    data = request.args
    if request.method == 'POST':
        if data.get('text'):
            res = mongo.db.dashboard.insert_one(dict(data))
            cache.set(res)
            return jsonify({'ok': True, 'message': 'Message created successfully % s ' % res.inserted_id}), 200
        else:
            return jsonify({'ok': False, 'message': 'Text should present'}), 400


@app.route('/tag/<ObjectId:message_id>', methods=['POST'])
def add_tag_to_message(message_id):
    data = request.args
    if request.method == 'POST':
        if data.get('text'):
            res = mongo.db.dashboard.update_one({"_id": message_id}, {"$addToSet": {"tags": dict(data)}})
            cache.set(res)
            return jsonify({'ok': True, 'message': 'Tag inserted successfully % s ' % res}), 200
        else:
            return jsonify({'ok': False, 'message': 'Text should present'}), 400


@app.route('/comment/<ObjectId:message_id>', methods=['POST'])
def add_comment_to_message(message_id):
    data = request.args
    if request.method == 'POST':
        if data.get('text'):
            res = mongo.db.dashboard.update_one({"_id": message_id}, {"$add": {"comments": dict(data)}})
            cache.set(res)
            return jsonify({'ok': True, 'message': 'Comment inserted successfully % s ' % res}), 200
        else:
            return jsonify({'ok': False, 'message': 'Text should present'}), 400


@app.route('/stats/<ObjectId:message_id>', methods=['GET'])
def stats_by_id(message_id):
    if request.method == 'GET':
        res = mongo.db.dashboard.find_one_or_404(message_id)
        tags = 0
        comments = 0
        if 'tags' in res.keys():
            tags = len(ast.literal_eval(res['tags']))
        if 'comments' in res.keys():
            comments = len(ast.literal_eval(res['comments']))
        return jsonify({'ok': True, 'message': f'Message has {tags} tags and {comments} comments'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0')