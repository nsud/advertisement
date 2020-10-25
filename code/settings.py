MONGO_HOST = '84.201.155.228'
MONGO_PORT = 27017
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'DELETE']


#DOMAIN = {
message = {
        'schema': {
            'title': {
                'type': 'string'
            },
            'message': {
                'type': 'string'
            },
            'author': {
                'type': 'string'
            },
            'tags': {
                'type': 'list',
            },
            'comments': {
                'type': 'list',
            }
        }
}

DOMAIN = {
    'message': message,
}