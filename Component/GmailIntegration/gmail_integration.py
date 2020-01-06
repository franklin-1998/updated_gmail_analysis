
from __future__ import print_function
from pandas import DataFrame
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from httplib2 import Http
from oauth2client import file, client, tools
import base64
from datetime import date
import email
import os.path
from os import path
import pickle
import urllib
import datetime
import pandas as pd
import urllib.request
import wget
import time
import webbrowser
import shutil
import re
from dateutil import parser as date_parser
from googleapiclient.http import BatchHttpRequest


#its automatically finds the download file path in any windows program
def get_download_path():
    """Returns the default downloads path for linux or windows"""
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
            location = winreg.QueryValueEx(key, downloads_guid)[0]
        return location
    else:
        return os.path.join(os.path.expanduser('~'), 'downloads')


#its a url provided for google API
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'


#function to fetch gmail mail based on no_of_days since which you want
def gmailIntegration(mails_Under_given_days):
    #delete the token.pickle which is unique for different users
    if(path.exists('token.pickle')):
        os.remove('token.pickle')
    #if the credentials.json is not present then only we go for a new one. if it is present we can use for n number of times.
    if(not path.exists('credentials.json')):
        #this gives the path where the credentials will be download
        src = get_download_path()
        #varialble to store the credentials path
        cred_path=''

        
        cred_path = src+'\credentials.json'
        #URL to open google page to enable GOOGLE API
        url='https://developers.google.com/gmail/api/quickstart/dotnet'

        #its for open in new tab
        webbrowser.open_new_tab(url)
        #wait before going to next step untill the credentials downloaded
        while(not path.exists(cred_path)):
            continue
        #move the downloaded credentials to the current dirrectory
        shutil.move(cred_path , os.getcwd())
        
    creds = None
    
    #these are all the steps to download token.pickle file (up to line 87)
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)


    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    # return creds
    # # request for service from gmail
    service = build('gmail', 'v1', credentials=creds)

      

    #list to extend(store) messages in corresponding pages
    messages = []

    # Call the Gmail API to fetch INBOX
    # get initialy upto 500 messages
    results = service.users().messages().list(userId='me',maxResults=1000).execute()
    print("first res-----------------       :          ",len(results))
    #extract messages to messages varialbe from result becaue we use "result" varialbe for n times
    messages.extend(results['messages'])

    batch = BatchHttpRequest()
    message_batch=[]

    def callback(request_id, response, exception):
        
        if exception is not None:
            pass
        else:
            message_batch.append(response)
            
    for mes in messages:
        batch.add(service.users().messages().get(userId='me', id=mes['id']),callback = callback)
    batch.execute()
    #collect all messages based on pagetoken wise
    batch_count = 1
    while('nextPageToken' in results):
        batch_count =batch_count + 1
        print("Batch_Count------------------------:",batch_count)
        messages = []
        page_token = results['nextPageToken']
        results = service.users().messages().list(userId='me',pageToken=page_token,maxResults=1000).execute()
        messages.extend(results['messages'])
        print("messages length -----------------------------: ",len(messages))
        print("result length ------------------------------------------: ",len(results))
        for mes in messages:
            batch.add(service.users().messages().get(userId='me', id=mes['id']),callback = callback)
        batch.execute()
        batch = BatchHttpRequest()
        print("batch {0} ended".format(batch_count))
    

    
    
    #its the variale used to fetch all detail about threads (for future use)
    # threads = service.users().threads().list(userId='me').execute().get('threads', [])

    # these are all the list to store each colomn data 
    From = []
    To = []
    Sub = []
    Body = []
    Thread_id = []
    Date = []
    

    #thes varialbe is used as a flag to integate whether we reach the given number of input days
    terminator = 0
    
    
    for message in message_batch:
        
        if(terminator>0):
            break
        #get complete data of each message
        
        
        #these are variables are used as flags which helps us in time of missing or unprovide null values
        To_flag = 0
        Sub_flag = 0
         #iterate through the message content to get the each colomn value
        for part in message['payload']['headers']:
            #to fetch date
            if(part['name'] == 'Date'):
                #to check the limited days
                if(((datetime.datetime.now() - (date_parser.parse(part['value'],fuzzy=True).replace(tzinfo=None))).days) > mails_Under_given_days):
                    print('finished')
                    #change the flag state if the limits exceeded
                    terminator = 1
                Date.append(date_parser.parse(part['value'],fuzzy=True).replace(tzinfo=None))
            if part['name'] == 'From':
                From.append(','.join(re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",part['value'])))
            if part['name'] == 'To':
                To.append(','.join(re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",part['value'])))
                To_flag=1

            if(part['name'] == 'Subject'):
                Sub.append(part['value'])
                Sub_flag=1
        #if there is no any part value is as 'To' then the flag doesnt change so we encode 'None' value as Anonymous 
        if(To_flag == 0):
            To.append('No Recepient Address')
        if(Sub_flag == 0):
            Sub.append("No Content")
        Thread_id.append(message['threadId'])
        Body.append(message['snippet'])

    # dump all the list value in the dataframe
    data_frame_excel = pd.DataFrame({'TimeDate':Date,'From':From,'To':To,'Subject':Sub,'Body':Body,'Thread_Id':Thread_id})

    # sorting the time to fetch first stimuli and first response and converting timedate formate str to datetime

    data_frame_excel = (data_frame_excel.sort_values(by='TimeDate',ascending=True)).reset_index(drop=True)

    return data_frame_excel
   

