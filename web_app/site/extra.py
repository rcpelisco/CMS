import requests

host = 'localhost'
port = '8080'
domain = 'http://{}:{}'.format(host, port)

def get(route):
    endpoint = domain + route
    return requests.get(endpoint)

def post(route, data):
    endpoint = domain + route
    return requests.post(endpoint, json=data)
