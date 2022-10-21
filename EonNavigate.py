### Json to get data from Eon Navigator by Mikael Rönn 2022-10-21 ###
import requests
import json

"""Extract nested values from a JSON tree."""
def json_extract(obj, key):
    """Recursively fetch values from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values

######## Set your login ########################################################
client_id = "client_id=YourID"
client_secret = "client_secret=YourSecret"
grant_type = "grant_type=client_credentials"

######## Api Url ########################################################
baseUrl = "https://navigator-api.eon.se"
tokenUrl = baseUrl +"/connect/token"
measurementUrl = baseUrl +"/api/installations/measurement-series"
installationsUrl = baseUrl +"/api/installations"
measureUrl = baseUrl +"/api/measurements/"

########  Get Bearer token ######################################################
payload = (client_id+'&'+client_secret+'&'+grant_type)
headers = {'content-type': "application/x-www-form-urlencoded",'cache-control': "no-cache",    }
request = requests.post(tokenUrl, data=payload, headers=headers)
response = json_extract(request.json(), 'access_token')
access_token = (response[0])
print('My AccessToken:',access_token)

########  Set Header for Api with Bearer token ######################################################
headersAPI = {'accept': 'application/json','Authorization': 'Bearer '+access_token,}
params = (('offset', '0'),('limit', '20000'),)

########  Show Measurement-series  information ######################################################
request = requests.get(measurementUrl, headers=headersAPI, params=params, verify=True)
api_response = request.json()
print(api_response)

########  Get your ID ######################################################
response = json_extract(request.json(), 'id')
id = (response[1])
print('My ID:',id)

########  Show Installation information ######################################################
request = requests.get(installationsUrl, headers=headersAPI, params=params, verify=True)
api_response = request.json()
print(api_response)

########  Set Url for Api Get information ######################################################
extractUrl = measureUrl + str(id)
monthUrl = extractUrl +"/resolution/month"
dayUrl = extractUrl +"/resolution/day"
hourUrl = extractUrl +"/resolution/hour"
querystring = {"from":"2022-01","includeMissing":"\"true\" -H \"accept: application/json\""}
response_month = requests.get(monthUrl, headers=headersAPI, params=params, verify=True)
response_day = requests.get(dayUrl, headers=headersAPI, params=params, verify=True)
response_hour = requests.get(hourUrl, headers=headersAPI, params=querystring, verify=True)

########  Set what information to show ######################################################
query_response = response_month.json()
print(response_month.text.encode('utf8'))


#file = open("file_location.csv", 'a')
#save = f"{response_day.text.encode('utf8')}"
#file.write(save)
#file.close()
