import requests
from redis import Redis
from flask import Flask, request
import os, json


app = Flask(__name__)
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
MONGO_API = os.environ.get('MONGO_API')
cache = Redis(host=REDIS_HOST, port=REDIS_PORT)


@app.route('/message/<message_id>', methods=['GET'])
def index_get(message_id):
    res_tmp = cache.get(message_id)
    if res_tmp is not None:
        res = json.loads(res_tmp)
        add = {'from_cash': 'yes'}

    elif res_tmp is None:
        res = requests.get(f'{MONGO_API}/message/{message_id}').json()
        cache.set(message_id, json.dumps(res))
        add = {'from_cash': 'no'}
    res.update(add)
    return res, 200


### Посмотреть полный список объявлений
@app.route('/message/', methods=['GET'])
def index_debug():
    res = requests.get(f'{MONGO_API}/message/').json()
    add = {'from_cash': 'no'}
    res.update(add)
    return res, 200


@app.route('/message', methods=['POST'])
def index_post():
    data = request.json
    if data.get('text'):
        res = requests.post(f'{MONGO_API}/message/', json=data.get('text')).json()
        return res, 200
    else:
        return {'message': 'the item hasnt been added'}, 400


@app.route('/tag/<message_id>', methods=['POST'])
def add_tag_to_message(message_id):
    data = request.args
    if data.get('text'):
        info = requests.get(f'{MONGO_API}/message/{message_id}').json()
        etag = info['_etag']
        tags = info.get('tags', [])
        tags.append(data.get('text'))
        res = requests.patch(f'{MONGO_API}/message/{message_id}', json={'tags': tags},
                             headers={'If-Match': etag}).json()
        return res, 200
    else:
        return {'message': 'the item hasnt been added'}, 400


@app.route('/comment/<message_id>', methods=['POST'])
def add_comment_to_message(message_id):
    data = request.args
    if data.get('text'):
        info = requests.get(f'{MONGO_API}/message/{message_id}').json()
        etag = info['_etag']
        tags = info.get('comments', [])
        tags.append(data.get('text'))
        res = requests.patch(f'{MONGO_API}/message/{message_id}', json={'comments': tags},
                             headers={'If-Match': etag}).json()
        return res, 200
    else:
        return {'message': 'the item hasnt been added'}, 400


@app.route('/stats/<message_id>', methods=['GET'])
def stats_by_id(message_id):
    mess, add = 'Message hasnt been found', {}
    res_tmp = cache.get(f"stat_{message_id}")
    if res_tmp is not None:
        mess = res_tmp.decode('utf-8')
        add = {'from_cash': 'yes'}
    else:
        res = requests.get(f'{MONGO_API}/message/{message_id}').json()
        if res.get('_status', 'Done') != 'ERR':
            tags = len(res.get('tags', []))
            comments = len(res.get('comments', []))
            mess = f'Message has {tags} tags and {comments} comments'
            cache.set(f"stat_{message_id}", mess)
            add = {'from_cash': 'no'}

    result = {'message': mess}
    result.update(add)

    return result, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006)
