from urllib.parse import quote, urlencode
import base64
import json
import time
import pandas as pd
import flask
import requests
import uuid
from flask import request, jsonify
from pandas.io.json import json_normalize
from flask_cors import CORS
import webbrowser
import time

redirect_uri = 'http://localhost:8000/tutorial/gettoken/'
# Client ID and secret
graph_endpoint = 'https://graph.microsoft.com/v1.0{0}'
app = flask.Flask(__name__)
app.config["DEBUG"] = True

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


def get_signin_url(redirect_uri):
  # Build the query parameters for the signin url
  params = { 'client_id': client_id,
             'redirect_uri': redirect_uri,
             'response_type': 'code',
             'scope': ' '.join(str(i) for i in scopes)
            }

  signin_url = authorize_url.format(urlencode(params))
  return signin_url




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





def get_my_messages(access_token):
  get_messages_url = graph_endpoint.format('/me/messages')

  # Use OData query parameters to control the results
  #  - Only first 10 results returned
  #  - Only return the ReceivedDateTime, Subject, and From fields
  #  - Sort the results by the ReceivedDateTime field in descending order
  query_parameters = {'$top': '100000',
                      '$select': 'receivedDateTime,subject,from,ToRecipients,BodyPreview,ReplyTo,ConversationId',
                      '$orderby': 'receivedDateTime DESC'}

  r = make_api_call('GET', get_messages_url, access_token, parameters = query_parameters)

  if (r.status_code == requests.codes.ok):
    return r.json()
  else:
    return "{0}: {1}".format(r.status_code, r.text)


print(get_signin_url('http://localhost:8000/tutorial/gettoken/'))
webbrowser.open(get_signin_url('http://localhost:8000/tutorial/gettoken/'))
def splitting(messages):
  global data_frame_excel
  From = []
  To = []
  Sub = []
  Body = []
  Thread_id = []
  Date = []
  for each_mes in messages['value']:
    # print("\n values     :     {0}   \n".format(each_mes['toRecipients'][0]['emailAddress']['address']))
    To.append(each_mes['toRecipients'][0]['emailAddress']['address'])
    From.append(each_mes['from']['emailAddress']['address'])
    Sub.append(each_mes['subject'])
    Body.append(each_mes['bodyPreview'])
    Thread_id.append(each_mes['conversationId'])
    Date.append(each_mes['receivedDateTime'])
  # print(len(From),"   ",len(To),"   ",len(Sub),"    ",len(Body),"   ",len(Thread_id),"   ",len(Date))
  # dump all the list value in the dataframe
  data_frame_excel = pd.DataFrame({'TimeDate':Date,'From':From,'To':To,'Subject':Sub,'Body':Body,'Thread_Id':Thread_id})

  # sorting the time to fetch first stimuli and first response and converting timedate formate str to datetime
  data_frame_excel = (data_frame_excel.sort_values(by='TimeDate',ascending=True)).reset_index(drop=True)
  print(data_frame_excel)
  return data_frame_excel


cors = CORS(app, resources={r"/tutorial/gettoken/out": {"origins": "*"}})
@app.route('/tutorial/gettoken/out', methods=['GET','POST'])
def api_all13():
  try:
    print("returned")
    print(data_frame_excel)
    return (data_frame_excel).to_json()
  except:
    print("something error")
    return "something error"

cors = CORS(app, resources={r"/tutorial/gettoken/": {"origins": "*"}})
@app.route('/tutorial/gettoken/', methods=['GET','POST'])
def api_all12():
  print(request)
  access_token =  gettoken(request)
  print("\n access token 2 :{0} \n".format(access_token))
  messages = get_my_messages(access_token)
  splitting(messages)
  api_all13()
  return "This authentication process is get overed you can move on to your tab"

app.run(port='8000',use_reloader=False)




# try:
#     r = requests.get('https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=19757c90-9580-4c95-b5da-6101553756cd&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Ftutorial%2Fgettoken%2F&response_type=code&scope=openid+User.Read+Mail.Read')
#     print(HttpResponse('https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id=19757c90-9580-4c95-b5da-6101553756cd&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Ftutorial%2Fgettoken%2F&response_type=code&scope=openid+User.Read+Mail.Read'))
#     print()
#     # prints the int of the status code. Find more at httpstatusrappers.com :)
# except requests.ConnectionError:
#     print("failed to connect")



