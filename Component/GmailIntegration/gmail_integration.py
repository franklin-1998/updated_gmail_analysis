'''
Component : gmail_Integration

Purpose : to fetch mails automaticaly from gmail

Condition  : 
             1, python 3.8
             2, It only works on windows when the device has default download folder

testcases : 
             1. check whether credentials is present after compilation of the program(gmail_integ.py)
             2. check whether token.pickle is present after compilation of the program(gmail_integ.py) 

libraries : requirements.txt

Input : The input is getting from gmail user's API and user's credentials and token file

Output : And output the will be gmail data of the user's and framed as 'TimeDate','From','To','Subject','Body','Thread_Id'

'''

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
from apiclient.http import BatchHttpRequest


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
def main2():
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
    return creds
    # # request for service from gmail
    # service = build('gmail', 'v1', credentials=creds)

    # #for route to gmail integration
    # webbrowser.open('http://localhost:4200/all')  

    # #list to extend(store) messages in corresponding pages
    # messages = []

    # # Call the Gmail API to fetch INBOX
    # # get initialy upto 500 messages
    # results = service.users().messages().list(userId='me',maxResults=500).execute()
    # #extract messages to messages varialbe from result becaue we use "result" varialbe for n times
    # messages.extend(results['messages'])
    # page_token = results['nextPageToken']
    # results = service.users().messages().list(userId='me',pageToken=page_token,maxResults=500).execute()
    # messages.extend(results['messages'])
    # #collect all messages based on pagetoken wise
    # # while('nextPageToken' in results):
    # #     page_token = results['nextPageToken']
    # #     results = service.users().messages().list(userId='me',pageToken=page_token,maxResults=500).execute()
    # #     messages.extend(results['messages'])

    
    
    # #its the variale used to fetch all detail about threads (for future use)
    # threads = service.users().threads().list(userId='me').execute().get('threads', [])

    # # these are all the list to store each colomn data 
    # From = []
    # To = []
    # Sub = []
    # Body = []
    # Thread_id = []
    # Date = []
    # batch = BatchHttpRequest()
    # count = 0
    # message_batch=[]
    # #thes varialbe is used as a flag to integate whether we reach the given number of input days
    # terminator = 0
    # def callback(request_id, response, exception):
        
    #     if exception is not None:
    #         print(response)
    #     else:
    #         message_batch.append(response)
            
    # for mes in messages:
    #     # print("batching")
    #     batch.add(service.users().messages().get(userId='me', id=mes['id']),callback = callback)
    # batch.execute()
    
    # for message in message_batch:
        
    #     if(terminator>0):
    #         break
    #     #get complete data of each message
        
        
    #     #these are variables are used as flags which helps us in time of missing or unprovide null values
    #     To_flag=0
    #     Sub_flag=0
    #      #iterate through the message content to get the each colomn value
    #     for part in message['payload']['headers']:
    #         #to fetch date
    #         if(part['name']=='Date'):
    #             #print(    (    (datetime.datetime.now()  -    (date_parser.parse(part['value'],fuzzy=True).replace(tzinfo=None)) ).days )    )
    #             #to check the limited days
    #             if(  (    (datetime.datetime.now()  -    (date_parser.parse(part['value'],fuzzy=True).replace(tzinfo=None)) ).days ) > mails_Under_given_days):
    #                 print('finished')
    #                 #change the flag state if the limits exceeded
    #                 terminator = 1
    #             #if((datetime.datetime.now()  -    (date_parser.parse(part['value'],fuzzy=True).replace(tzinfo=None)) )  )
    #             Date.append(date_parser.parse(part['value'],fuzzy=True).replace(tzinfo=None))
    #         if part['name']=='From':
    #             # print(part['value'])
    #             From.append(','.join(re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",part['value'])))
    #         if part['name']=='To':
    #             # print(part['value'])
    #             To.append(','.join(re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",part['value'])))
    #             To_flag=1

    #         if(part['name']=='Subject'):
    #             Sub.append(part['value'])
    #             Sub_flag=1
    #     #if there is no any part value is as 'To' then the flag doesnt change so we encode 'None' value as Anonymous 
    #     if(To_flag==0):
    #         To.append('<unknown@gmail.com>')
    #     if(Sub_flag==0):
    #         Sub.append("No Content")
    #     Thread_id.append(message['threadId'])
    #     Body.append(message['snippet'])
    #     print(count)
    #     count = count+1

    #     #print(count)
    #     #print("\n************\n")
    
    # #     print(message)
    # # print(len(Date))
    # # print(len(From))
    # # print(len(To))
    # # print(len(Sub))
    # # print(len(Body))
    # # print(len(Thread_id))

    # # dump all the list value in the dataframe
    # data_frame_excel = pd.DataFrame({'TimeDate':Date,'From':From,'To':To,'Subject':Sub,'Body':Body,'Thread_Id':Thread_id})

    # # sorting the time to fetch first stimuli and first response and converting timedate formate str to datetime

    # data_frame_excel = (data_frame_excel.sort_values(by='TimeDate',ascending=True)).reset_index(drop=True)

    # return data_frame_excel




# mails_Under_given_days = 30 #3 months
# main2(mails_Under_given_days)














































































# '''
# Component : gmail_Integration

# Purpose : to fetch mails automaticaly from gmail

# Condition  : 
#              1. python 3.7.4
#              2. It only works on windows when the device has default download folder

# testcases : 
#              1. check whether credentials is present after compilation of the program(gmail_integration.py)
#              2. check whether token.pickle is present after compilation of the program(gmail_integration.py)
             
# Libraries : requirements.txt

# Input : The input is getting from gmail user's API and user's credentials and token file

# Output : And output the will be gmail data of the user's and framed as 'TimeDate','From','To','Subject','Body','Thread_Id'

# '''

# from __future__ import print_function
# from pandas import DataFrame
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from httplib2 import Http
# from oauth2client import file, client, tools
# import base64
# from datetime import date
# import email
# import os.path
# from os import path
# import pickle
# import urllib
# import datetime
# import pandas as pd
# import urllib.request
# import wget
# import time
# import webbrowser
# import shutil
# import re
# from dateutil import parser as date_parser



# #its automatically finds the download file path in any windows program
# def get_download_path():
#     """Returns the default downloads path for linux or windows"""
#     if os.name == 'nt':
#         import winreg
#         sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
#         downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
#         with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
#             location = winreg.QueryValueEx(key, downloads_guid)[0]
#         return location
#     else:
#         return os.path.join(os.path.expanduser('~'), 'downloads')


# #its a url provided for google API
# SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'


# #function to fetch gmail mail based on no_of_days since which you want
# def main2(mails_Under_given_days):
#     #delete the token.pickle which is unique for different users
#     if(path.exists('token.pickle')):
#         os.remove('token.pickle')
#     #if the credentials.json is not present then only we go for a new one. if it is present we can use for n number of times.
#     if(not path.exists('credentials.json')):
#         #this gives the path where the credentials will be download
#         src = get_download_path()
#         #varialble to store the credentials path
#         cred_path=''

        
#         cred_path = src+'\credentials.json'
#         #URL to open google page to enable GOOGLE API
#         url='https://developers.google.com/gmail/api/quickstart/dotnet'

#         #its for open in new tab
#         webbrowser.open_new_tab(url)
#         #wait before going to next step untill the credentials downloaded
#         while(not path.exists(cred_path)):
#             continue
#         #move the downloaded credentials to the current dirrectory
#         shutil.move(cred_path , os.getcwd())
        
#     creds = None
    
#     #these are all the steps to download token.pickle file (up to line 87)
#     if os.path.exists('token.pickle'):
#         with open('token.pickle', 'rb') as token:
#             creds = pickle.load(token)


#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         # Save the credentials for the next run
#         with open('token.pickle', 'wb') as token:
#             pickle.dump(creds, token)
#     # request for service from gmail
    
#     service = build('gmail', 'v1', credentials=creds)
    
#     #for route to gmail integration
#     webbrowser.open('http://localhost:4200/all')  
    
#     #list to extend(store) messages in corresponding pages
#     messages = []

#     # Call the Gmail API to fetch INBOX
#     # get initialy upto 500 messages
#     results = service.users().messages().list(userId='me',maxResults=500).execute()
#     #extract messages to messages varialbe from result becaue we use "result" varialbe for n times
#     messages.extend(results['messages'])
#     #collect all messages based on pagetoken wise
#     while('nextPageToken' in results):
#         page_token = results['nextPageToken']
#         results = service.users().messages().list(userId='me',pageToken=page_token,maxResults=500).execute()
#         messages.extend(results['messages'])

    
    
#     #its the variale used to fetch all detail about threads (for future use)
#     threads = service.users().threads().list(userId='me').execute().get('threads', [])
    
#     #final varialbe which is a dataframe store the data
#     email_data = pd.DataFrame(columns=['FROM','TO','SUBJECT','BODY','THREAD_ID'])

#     # these are all the list to store each colomn data 
#     From = []
#     To = []
#     Sub = []
#     Body = []
#     Thread_id = []
#     Date = []
    
#     count = 0
#     #thes varialbe is used as a flag to integate whether we reach the given number of input days
#     terminator = 0
#     for mes in messages:
#         print(count)
#         count = count+1
#         #check for termination
#         if(terminator>0):
#             break
#         #get complete data of each message
#         message = service.users().messages().get(userId='me', id=mes['id'],format='full').execute()
        
#         #these are variables are used as flags which helps us in time of missing or unprovide null values
#         To_flag=0
#         Sub_flag=0
#          #iterate through the message content to get the each colomn value
#         for part in message['payload']['headers']:
#             #to fetch date
#             if(part['name']=='Date'):
#                 #to check the limited days
#                 if(  (    (datetime.datetime.now()  -    (date_parser.parse(part['value'],fuzzy=True).replace(tzinfo=None)) ).days ) > mails_Under_given_days):
#                     print('finished')
#                     #change the flag state if the limits exceeded
#                     terminator = 1
#                 Date.append(date_parser.parse(part['value'],fuzzy=True).replace(tzinfo=None))
#             if part['name']=='From':
#                 From.append(','.join(re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",part['value'])))
#             if part['name']=='To':
#                 To.append(','.join(re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",part['value'])))
#                 To_flag=1

#             if(part['name']=='Subject'):
#                 Sub.append(part['value'])
#                 Sub_flag=1
        
#         #if there is no any part value is as 'To' then the flag doesnt change so we encode 'None' value as Anonymous 
#         if(To_flag==0):
#             To.append('Anonymous Email')
#         if(Sub_flag==0):
#             Sub.append("Anonymous Email")
#         Thread_id.append(message['threadId'])
#         Body.append(message['snippet'])


#     # dump all the list value in the dataframe
#     data_frame_excel = pd.DataFrame({'TimeDate':Date,'From':From,'To':To,'Subject':Sub,'Body':Body,'Thread_Id':Thread_id})

#     # sorting the time to fetch first stimuli and first response and converting timedate formate str to datetime

#     data_frame_excel = (data_frame_excel.sort_values(by='TimeDate',ascending=True)).reset_index(drop=True)

#     # data_frame_excel.to_csv('GmailData.csv') 
#     return (data_frame_excel)



# # mails_Under_given_days = 15 #1 months
# # main(mails_Under_given_days)

