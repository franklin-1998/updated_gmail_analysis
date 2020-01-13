from urllib.parse import quote, urlencode
import base64
import json
import time
import pandas as pd
import flask
import requests
import uuid
from time import sleep
import dateutil.parser
from dateutil import parser as date_parser
from flask import request, jsonify
from pandas.io.json import json_normalize
from flask_cors import CORS
import webbrowser
import time

#initialize the global variables
skipINCREMENT = 1000
skipValue = 0
data_frame_excel = pd.DataFrame()
huge_messages = []
stopValue = 5000


# Redirect_uri is used to get the token and it is created by admin of this app and he will create azure app and register the details of permissions for getting all user's data
redirect_uri = 'http://localhost:8000/tutorial/gettoken/'

# Client ID and secret
graph_endpoint = 'https://graph.microsoft.com/v1.0{0}'
app = flask.Flask(__name__)
app.config["DEBUG"] = True

# this id and secret is admin which will create an app in azure
client_id = '19757c90-9580-4c95-b5da-6101553756cd'
client_secret = 'JpA]?O=.NWOAzKKGYgPhM4ogoU7aK2s3'

# Constant strings for OAuth2 flow
# The OAuth authority
authority = 'https://login.microsoftonline.com'

# The authorize URL that initiates the OAuth2 client credential flow for admin consent
authorize_url = '{0}{1}'.format(authority, '/common/oauth2/v2.0/authorize?{0}')

# The token issuing endpoint
token_url = '{0}{1}'.format(authority, '/common/oauth2/v2.0/token')

# The scopes required by the app
scopes = [ 'openid',
           'User.Read',
           'Mail.Read' ]
access_token=''

# sign in form from the microsoft and after user sign_in with his credentials and allow permissions to access his data

def get_signin_url(redirect_uri):
    # Build the query parameters for the signin url
    params = { 'client_id': client_id,
                'redirect_uri': redirect_uri,
                'response_type': 'code',
                'scope': ' '.join(str(i) for i in scopes)
                }

    signin_url = authorize_url.format(urlencode(params))
    return signin_url


# getting token using auth_code and redirect_uri
def get_token_from_code(auth_code, redirect_uri):
    # Build the post form for the token request
    post_data = { 'grant_type': 'authorization_code',
                    'code': auth_code,
                    'redirect_uri': redirect_uri,
                    'scope': ' '.join(str(i) for i in scopes),
                    'client_id': client_id,
                    'client_secret': client_secret
                }

    r = requests.post(token_url, data = post_data)

    try:
        return r.json()
        
    except:
        print("\n text type :" , type(r.text),'\n')
        r=eval(r.text)
        
        return r

# getting auth code and redirect uri to combine to get the token
# getting token from the respect user id with his permissions

def gettoken(request):
    auth_code = request.args.get('code')
    print("#########@!$@#$@!#@!###########V           ",auth_code)
    token = get_token_from_code(auth_code,redirect_uri)
    access_token = token['access_token']
    print("\n access token : {0}\n".format(access_token))
    return access_token
    
  
# Generic API Sending
def make_api_call(method, url, token, payload = None, parameters = None):
    # Send these headers with all API calls
    headers = { 'User-Agent' : 'python_tutorial/1.0',
                'Authorization' : 'Bearer {0}'.format(token),
                'Accept' : 'application/json' }

    # Use these headers to instrument calls. Makes it easier
    # to correlate requests and responses in case of problems
    # and is a recommended best practice.
    request_id = str(uuid.uuid4())
    instrumentation = { 'client-request-id' : request_id,
                        'return-client-request-id' : 'true' }

    headers.update(instrumentation)

    response = None

    if (method.upper() == 'GET'):
        response = requests.get(url, headers = headers, params = parameters)
    elif (method.upper() == 'DELETE'):
        response = requests.delete(url, headers = headers, params = parameters)
    elif (method.upper() == 'PATCH'):
        headers.update({ 'Content-Type' : 'application/json' })
        response = requests.patch(url, headers = headers, data = json.dumps(payload), params = parameters)
    elif (method.upper() == 'POST'):
        headers.update({ 'Content-Type' : 'application/json' })
        response = requests.post(url, headers = headers, data = json.dumps(payload), params = parameters)

    return response


# getting user name of the respect credentials user id
def get_me(access_token):
    get_me_url = graph_endpoint.format('/me')

    # Use OData query parameters to control the results
    #  - Only return the displayName and mail fields
    query_parameters = {'$select': 'displayName,mail'}

    r = make_api_call('GET', get_me_url, access_token, "", parameters = query_parameters)

    if (r.status_code == requests.codes.ok):
        return r.json()
    else:
        return "{0}: {1}".format(r.status_code, r.text)



# getting messages using the accessing tokens for the respect email id based on url

def get_my_messages(access_token,skipValue):
    get_messages_url = graph_endpoint.format('/me/messages')

    # For Checking 
    print(skipValue)

    # Use OData query parameters to control the results
    #  - Only first 10 results returned
    #  - Only return the ReceivedDateTime, Subject, and From fields
    #  - Sort the results by the ReceivedDateTime field in descending order
    query_parameters = {'$top': '1000',
                        '$select': 'sentDateTime,subject,from,ToRecipients,BodyPreview,ReplyTo,ConversationId,ccRecipients,isDraft',
                        '$orderby': 'sentDateTime DESC',
                        '$skip': str(skipValue)}

    r = make_api_call('GET', get_messages_url, access_token, parameters = query_parameters)

    if (r.status_code == requests.codes.ok):
        return r.json()
    else:
        return "{0}: {1}".format(r.status_code, r.text)



# Function which extract messages into "From,To,Subject,Body,Thread_Id"

def extractingMessages(messages):  
    global data_frame_excel
    From = []
    To = []
    Sub = []
    Body = []
    Thread_id = []
    Date = []
    count = 0
    for huge_msg in huge_messages:
        for each_mes in huge_msg['value']:
            count = count+1
            print(count)
            if each_mes['isDraft'] == False:
                try:
                    To.append(each_mes['toRecipients'][0]['emailAddress']['address'])
                except KeyError:
                    To.append("UnkownEmailId")
                except IndexError:
                    To.append("UnkownEmailId")
                try:
                    From.append(each_mes['from']['emailAddress']['address'])
                except KeyError:
                    From.append("UnkownEmailId")
                except IndexError:
                    From.append("UnkownEmailId")
                try:
                    Sub.append(each_mes['subject'])
                except KeyError:
                    Sub.append("No Subject")
                except IndexError:
                    Sub.append("No Subject")
                try:
                    Body.append(each_mes['bodyPreview'])
                except KeyError:
                    Body.append("No Body Content")
                except IndexError:
                    Body.append("No Body Content")
                try:
                    Thread_id.append(each_mes['conversationId'])
                except KeyError:
                    Thread_id.append("No Thread_Id")
                except IndexError:
                    Thread_id.append("No Thread_Id")
                try:
                    Date.append(date_parser.parse(each_mes['sentDateTime'],fuzzy=True).replace(tzinfo=None))
                except KeyError:
                    Date.append("No DateTime")
                except IndexError:
                    Date.append("No DateTime")

    # dump all the list value in the dataframe
    data_frame_excel = pd.DataFrame({'TimeDate':Date,'From':From,'To':To,'Subject':Sub,'Body':Body,'Thread_Id':Thread_id})

    # sorting the time to fetch first stimuli and first response and converting timedate formate str to datetime
    data_frame_excel = (data_frame_excel.sort_values(by='TimeDate',ascending=True)).reset_index(drop=True)

    try:
        data_frame_excel['TimeDate'] = data_frame_excel['TimeDate'].dt.strftime('%Y-%m-%d %H:%M:%S')
    except AttributeError:
        data_frame_excel['TimeDate'] = data_frame_excel['TimeDate'].astype(str)

    # for reference to save as csv file 
    data_frame_excel.to_csv("huge.csv")
    return data_frame_excel



# Function is getting token from the microsoft authority and getting huge number of messages and extracting to form the dataframe for columns like "From,To,Subject,Body,Thread_Id"

cors = CORS(app, resources={r"/tutorial/gettoken/": {"origins": "*"}})
@app.route('/tutorial/gettoken/', methods=['GET','POST'])
def api_all12():
    # for checking purpose
    print(request)
    global skipValue
    global skipINCREMENT
    global huge_messages
    global stopValue
    

    access_token =  gettoken(request)
    print("\n access token 2 :{0} \n".format(access_token))

    while(True):
        messages = get_my_messages(access_token,skipValue)
        huge_messages.append(messages)
        skipValue = skipValue + skipINCREMENT
        if skipValue == stopValue:
            break

    extractingMessages(huge_messages)
    return "The authentication flow has completed. You may close this window."

#flask process to host
cors = CORS(app, resources={r"/outlook_run": {"origins": "*"}})

@app.route('/outlook_run', methods=['GET','POST'])
def outlook_main():
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++=")
    webbrowser.open(get_signin_url('http://localhost:8000/tutorial/gettoken/'))
    while data_frame_excel.empty:
        continue

    print("*********************Data Had Been Stored********************************")  
    output_dict = {'data_frame':(data_frame_excel).to_json()}
    return json.dumps(str(output_dict))




app.run(port='8000',use_reloader=False)
