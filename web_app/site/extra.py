import requests

host = 'localhost'
port = '8080'

def get(route):
    endpoint = 'http://{}:{}{}'.format(host, port, route)
    return requests.get(endpoint)
