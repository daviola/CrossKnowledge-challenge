import requests
import redis
import json

SERVER = 'localhost'
PORT = '80'
client = redis.Redis(host = SERVER, port = PORT)

def get(url, parameters=None):
    """ Fetches an URL and returns the response """
    # Try to get from cache
    response = from_cache(url, parameters)
    if response:
        print("response from cache")
        return response
    response = requests.get(url, params=parameters).json()
    set_cache(url, parameters, None, response)
    print("response from get")
    return response

def post(url, parameters=None, data=None):
    """ Post data to an URL and returns the response """
    return requests.post(url, params=parameters, data=data).json()

def put(url, parameters=None, data=None):
    """ Put data to an resource and returns the response """
    return requests.put(url, params=parameters, data=data).json()

def patch(url, parameters=None, data=None):
    """ Patches an resource and returns the response """
    return requests.patch(url, params=parameters, data=data).json()

def delete(url, parameters=None, data=None):
    """ Requests the deletion of an resource and returns the response """
    return requests.delete(url, params=parameters, data=data).json()

def from_cache(url, params, data=None):    
    key = url +str(json.dumps(params))+str(data)    
    response = client.get(key)
    if response:
        return response
    else:        
        return None

def set_cache(url, params, data, value):    
    key = url +str(json.dumps(params))+str(data)
    # expires after 5 seconds
    client.set(key, str(value), ex=5)

get('https://api.github.com/events')


        
    