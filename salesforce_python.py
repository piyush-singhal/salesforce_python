# Import Packages
import requests
import json

params = {
    "grant_type": "password",
    "client_id": "######", # Consumer Key
    "client_secret": "#####", # Consumer Secret
    "username": "######", # The email you use to login
    "password": "######" # Concat your password and your security token
}
r = requests.post("https://login.salesforce.com/services/oauth2/token", params=params)
print(r.content)
access_token = r.json().get("access_token")
instance_url = r.json().get("instance_url")
print("Access Token:", access_token)
print("Instance URL", instance_url)


def sf_api_call(action, parameters = {}, method = 'get', data = {}):
   
    #Helper function to make calls to Salesforce REST API.
    #Parameters: action (the URL), URL params, method (get, post or patch), data for POST/PATCH.
    
    headers = {
        'Content-type': 'application/json',
        'Accept-Encoding': 'gzip',
        'Authorization': 'Bearer %s' % access_token
    }
    if method == 'get':
        r = requests.request(method, instance_url+action, headers=headers, params=parameters, timeout=30)
    elif method in ['post', 'patch']:
        r = requests.request(method, instance_url+action, headers=headers, json=data, params=parameters, timeout=10)
    else:
        # other methods not implemented in this example
        raise ValueError('Method should be get or post or patch.')
    print('Debug: API %s call: %s' % (method, r.url) )
    if r.status_code < 300:
        if method=='patch':
            return None
        else:
            return r.json()
    els
        raise Exception('API error when calling %s : %s' % (r.url, r.content))


print(json.dumps(sf_api_call('/services/data/v39.0/query/', {
    'q': 'SELECT Account.Name, Name, CloseDate from Opportunity where IsClosed = False order by CloseDate ASC LIMIT 10'
}), indent=2))
