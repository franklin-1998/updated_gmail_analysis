from urllib.parse import quote, urlencode
import base64
import json
from bs4 import BeautifulSoup
import time
import pandas as pd
import flask
import datetime
import re
import ast
import requests
import uuid
from dateutil.parser import parse
from time import sleep
import dateutil.parser
from dateutil import parser as date_parser
from flask import request, jsonify
from pandas.io.json import json_normalize
from flask_cors import CORS
import webbrowser
import time
import talon

#initializing talon method
talon.init()

from talon import signature



#initialize the global variables
skipINCREMENT = 0
skipValue = 0
data_frame_excel = pd.DataFrame()
stepCount = 0
huge_messages = []
flag = 0
data_frame_FirstSender = pd.DataFrame({})
current_DateTime = 0
testing_dataFrame = pd.DataFrame({})
stopCountValues = 5
labelled_dataFrame = pd.DataFrame({})
stopValue = 20
receivedMessages_Store = pd.DataFrame({})


# Redirect_uri is used to get the token and it is created by admin of this app and he will create azure app and register the details of permissions for getting all user's data
redirect_uri = 'http://localhost:8000/tutorial/gettoken/'
redirect_uri_2 = 'http://localhost:8000/logout' # logout url to unknown address

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


# logout url
logout_url = "https://login.windows.net/common/oauth2/logout?post_logout_redirect_uri="

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


# logout after getting all information data's from the user id
# logout method
def log_out():    
    url = logout_url+redirect_uri_2
    return webbrowser.open(url)


# getting messages using the accessing tokens for the respect email id based on url

def get_my_messages(access_token):
    get_messages_url = graph_endpoint.format('/me/messages')

    # Use OData query parameters to control the results
    #  - Only first 10 results returned
    #  - Only return the ReceivedDateTime, Subject, and From fields
    #  - Sort the results by the ReceivedDateTime field in descending order
    query_parameters = {'$top': '25',
                        '$select': 'sentDateTime,subject,from,ToRecipients,uniqueBody,ReplyTo,ConversationId,ccRecipients,isDraft,body',
                        '$orderby': 'sentDateTime DESC'}

    r = make_api_call('GET', get_messages_url, access_token, parameters = query_parameters)

    if (r.status_code == 200):
        return r.json()
    elif (r.status_code == 504):
        print("{0}: {1}".format(r.status_code, r.text))
        sleep(5)
        get_my_messages(access_token)
    else:
        print("{0}: {1}".format(r.status_code, r.text))
        sleep(5)
        get_my_messages(access_token)



# Function which extract messages into "From,To,Subject,Body,Thread_Id"

def extractingMessages(messages):  
    global data_frame_excel
    From = []
    To = []
    Sub = []
    Body = []
    Thread_id = []
    Date = []
    for each_mes in messages['value']:
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
                body_reading = BeautifulSoup(each_mes['body']['content'], 'html.parser')
                elements = body_reading.find_all("div", id="Signature")
                for element in elements:
                    element.decompose()
                body_content = body_reading.get_text().encode("ascii", "ignore").decode("utf-8")
                body_content = re.sub(r'(\n\s*)+\n+', '\n\n', body_content)
                text, signatures = signature.extract(body_content,sender=each_mes['from']['emailAddress']['address'])
                text1, signatures1 = signature.extract(text,sender=each_mes['from']['emailAddress']['address'])
                text2, signatures2 = signature.extract(signatures,sender=each_mes['from']['emailAddress']['address'])
                Body.append(re.sub("None","",(str(text1)+str(text2))))
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

    return data_frame_excel



# Function is getting token from the microsoft authority and getting huge number of messages and extracting to form the dataframe for columns like "From,To,Subject,Body,Thread_Id"

cors = CORS(app, resources={r"/tutorial/gettoken/": {"origins": "*"}})
@app.route('/tutorial/gettoken/', methods=['GET','POST'])
def requestingDataFromOutlook():
    print(request)
    global skipValue
    global skipINCREMENT
    global huge_messages
    global stopValue
    global receivedMessages_Store
    global labelled_dataFrame
    global stepCount
    global data_frame_FirstSender
    global testing_dataFrame
    global flag
    global current_DateTime

    # finding current datetime
    current_DateTime = datetime.datetime.now()
    
    # access token string
    access_token =  gettoken(request)
    print("\n access token 2 :{0} \n".format(access_token))
    print("User Should Send First Issues with 20 mails Next Non-Issues with 20 mails and then Next 20 mails for Testing to Predict ")
    while(True):
        # initialize to continously to take new mails
        data_frame_FirstSender = pd.DataFrame({})
        receivedMessages_Store = pd.DataFrame({})
        # getting the messages using url
        messages = get_my_messages(access_token)
        # huge_messages.append(messages)
        receivedMessages_new = extractingMessages(messages)
        # converting datetime format
        receivedMessages_new['TimeDate'] = [datetime.datetime.fromtimestamp(receivedMessages_new['TimeDate'][i].timestamp()) for i in range(len(receivedMessages_new))]
        # checking duplicates to avoid data redundancy
        for redundancy_checking in range(len(receivedMessages_new)):
            if parse(str(current_DateTime)) < receivedMessages_new['TimeDate'][redundancy_checking]:
                receivedMessages_Store = receivedMessages_Store.append(receivedMessages_new.iloc[redundancy_checking])
        if not receivedMessages_Store.empty:
            #unique thread_id
            unique_thread_id = receivedMessages_Store['Thread_Id'].unique()
            # loop to sort time date and fetch first conversation
            for loop_1 in range(len(unique_thread_id)):
                individual_thread_id_mailData = receivedMessages_Store.loc[receivedMessages_Store['Thread_Id'] == unique_thread_id[loop_1]]
                # sorting the time to fetch first stimuli 
                individual_thread_id_mailData = (individual_thread_id_mailData.sort_values(by='TimeDate',ascending=True)).reset_index(drop=True)
                
                data_frame_FirstSender = data_frame_FirstSender.append(individual_thread_id_mailData)
            
            data_frame_FirstSender = data_frame_FirstSender.reset_index(drop=True)
            if len(data_frame_FirstSender['From']) == stopCountValues:
                stepCount = stepCount + 1
                if stepCount == 1:
                    data_frame_FirstSender['Label'] = 1
                    labelled_dataFrame = labelled_dataFrame.append(data_frame_FirstSender)
                    print("User Send 20 mails as the issue and Next Continue with non-issues")
                    current_DateTime = datetime.datetime.now()
                    data_frame_FirstSender = pd.DataFrame({})
                    receivedMessages_Store = pd.DataFrame({})
                elif stepCount == 2:
                    data_frame_FirstSender['Label'] = 0
                    labelled_dataFrame = labelled_dataFrame.append(data_frame_FirstSender)
                    labelled_dataFrame = labelled_dataFrame.reset_index(drop=True)
                    print("User Send 20 mails as non-issue and Next Send mixed with these two types as issue and non-issue to test with learning")
                    data_frame_FirstSender = pd.DataFrame({})
                    current_DateTime = datetime.datetime.now()
                    receivedMessages_Store = pd.DataFrame({})
                elif stepCount == 3:
                    testing_dataFrame = testing_dataFrame.append(data_frame_FirstSender)
                    testing_dataFrame = testing_dataFrame.reset_index(drop=True)
                    print("Testing Data Also Received Learning and Testing Process Will be Started")
                    flag = 1 # to stop if required details has received
                    break
        else:
            print("No New Mails Had Been Received.....Send mails to Configure")

        # sleeping time to user to send new message
        sleep(5)

    return "The authentication flow has completed. You may close this window."

#flask process to host
cors = CORS(app, resources={r"/logout": {"origins": "*"}})
@app.route('/logout',methods=['GET','POST'])
def logout_session():
    sleep(3)
    return "Logged Out Successfully. You may close this window."


# function to sign_url and getting messages with user permissions
#flask process to host
cors = CORS(app, resources={r"/outlook_run": {"origins": "*"}})
@app.route('/outlook_run', methods=['GET','POST'])

def outlook_main():
    # global current_DateTime
    print("++++++++++++++++++++++++++++++ Process Begins ++++++++++++++++++++++++++++++++++++++++++++++++++++++=")
    # opening webbrowser to sign_in page for outlook
    webbrowser.open(get_signin_url('http://localhost:8000/tutorial/gettoken/'))
    
    # after getting all data only it will allow to send to some service or component to process
    while flag!=1:
        continue
    # function call for logout
    log_out()

    print("*********************Data Had Been Stored********************************")  
    output_dict = {'training':(labelled_dataFrame).to_json(),'testing':(testing_dataFrame).to_json()}
    return json.dumps(str(output_dict))


app.run(port='8000',use_reloader=False)
