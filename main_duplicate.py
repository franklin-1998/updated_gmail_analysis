import ast
import random
import pandas as pd
import numpy as np
import json
import flask
from time import sleep
from collections import OrderedDict
import warnings
from dateutil import parser as date_parser
import dateparser
import requests
from flask import request, jsonify
from flask_cors import CORS
import base64
from datetime import date
import datetime
import pandas as pd
import webbrowser
<<<<<<< HEAD
import shutil
import re
from dateutil import parser as date_parser
from apiclient.http import BatchHttpRequest


=======
import os
>>>>>>> c6d382fd523d649327c4b4a060edcccebeead96f
'''
Importing components from the other folder to implement the main login file.

'''
from Component.GmailIntegration.gmail_integration import gmailIntegration
# from Component.OutlookIntegration.outlook import outlook
from Component.ResponseTime.response_time import responseTimeCalculating,avgResponseTime
from Component.DetectSameEmails.detect_similar_emails import detectingSimilarEmails

# ignoring warning
warnings.filterwarnings('ignore')

# app config for the flask
app = flask.Flask(__name__)
app.config["DEBUG"] = True

global mails_Under_given_days

<<<<<<< HEAD
# Function implements to filter the replied emails and adding response time for the individual thread_id
def dataFiltering_AddingResponseTime(all_data_FromGmail):
        
    # Filter the replied emails
    count_list = list(all_data_FromGmail["Thread_Id"])
=======
mails_Under_given_days = 60 # 1 month

# Function implements to filter the replied emails and adding response time for the individual thread_id
def dataFiltering_AddingResponseTime(all_data_FromMail):
        
    # Filter the replied emails
    count_list = list(all_data_FromMail["Thread_Id"])
>>>>>>> c6d382fd523d649327c4b4a060edcccebeead96f
    count_by_filter = []

    for count_value in range(len(count_list)):
        count_by_filter.append(count_list.count(count_list[count_value]))
<<<<<<< HEAD
    all_data_FromGmail['Count_THREAD_ID'] = count_by_filter
    data_frame_excel_emails = (all_data_FromGmail.loc[all_data_FromGmail['Count_THREAD_ID'] >= 2]).reset_index(drop = True)
=======
    all_data_FromMail['Count_THREAD_ID'] = count_by_filter
    data_frame_excel_emails = (all_data_FromMail.loc[all_data_FromMail['Count_THREAD_ID'] >= 2]).reset_index(drop = True)
>>>>>>> c6d382fd523d649327c4b4a060edcccebeead96f

    # Calling function for individual thread_id response time

    response_time_for_individual_thread_id = responseTimeCalculating(data_frame_excel_emails)

    # Data for storing all replied emails and adding a column response time for each thread_id

    data_frame_excel_replied = pd.DataFrame()
    thread_id_list = []
    for k,v in response_time_for_individual_thread_id.items():
        thread_id_list.append(k)

    for replied in range(len(thread_id_list)):
        replied_dataframe = data_frame_excel_emails.loc[data_frame_excel_emails['Thread_Id'] == thread_id_list[replied]]
        data_frame_excel_replied = data_frame_excel_replied.append(replied_dataframe)
    data_frame_excel_replied = data_frame_excel_replied.reset_index(drop=True) #index reset

    data_frame_excel_replied['ResponseTime'] = ''
    for add_column in range(len(data_frame_excel_replied)):
        for keys,values in response_time_for_individual_thread_id.items():
            if data_frame_excel_replied['Thread_Id'][add_column] == keys:
                data_frame_excel_replied['ResponseTime'][add_column] = str(values)
<<<<<<< HEAD
    return (data_frame_excel_replied,all_data_FromGmail,response_time_for_individual_thread_id)
=======
    return (data_frame_excel_replied,all_data_FromMail,response_time_for_individual_thread_id)
>>>>>>> c6d382fd523d649327c4b4a060edcccebeead96f



# Applying doc2vec process for converting text or document of texts to vector spaces
# Api call for doc2vec
def callAPIDoc2Vec(model_path,message_input):
    headers = {'content-type': 'application/json'}
    # print(message_input)
    all_data_conv_dict_from = {'model_path':model_path,'message_value':message_input}
    successFlag = True
    count_trying = 0
    retryConnection = 10
    period = 10 #seconds
    while successFlag:
        try:
            #sending the data to the server
            resp = requests.post("http://127.0.0.1:8200/doc2vec",data = json.dumps(all_data_conv_dict_from),headers=headers)
            successFlag = False
        except requests.exceptions.ConnectionError:
            print('----------Request Connection Error-----------')
            sleep(period)
            count_trying = count_trying + 1
            if(count_trying > retryConnection):
                print("-------------Some Problem In Server Communication -------------")
                break

    #response from the server
    message_value = ast.literal_eval(resp.json())
    # print(message_value)
    return message_value['message_convert']


# after finishing applying kmeans clustering for the relevant emails that related with other emails
# api call for kmeans

def callAPIKmeans(full_data_frame_for_replied_emails,percentage_of_predictingElbowMethod,all_replied_mailData):
    headers = {'content-type': 'application/json'}
    successFlag = True
    count_trying = 0
    retryConnection = 10
    period = 10 #seconds
<<<<<<< HEAD
    all_data_conv_dict_from = {'full_data_frame_for_replied_emails':(full_data_frame_for_replied_emails).to_json(),'percentage_of_predictingElbowMethod':percentage_of_predictingElbowMethod,'all_replied_emails':(all_replied_gmailData).to_json()}
=======
    all_data_conv_dict_from = {'full_data_frame_for_replied_emails':(full_data_frame_for_replied_emails).to_json(),'percentage_of_predictingElbowMethod':percentage_of_predictingElbowMethod,'all_replied_emails':(all_replied_mailData).to_json()}
>>>>>>> c6d382fd523d649327c4b4a060edcccebeead96f
    while successFlag:
        try:
            #sending the data to the server
            resp = requests.post("http://127.0.0.1:9200/kmeans",data = json.dumps(all_data_conv_dict_from),headers=headers)
            successFlag = False
        except requests.exceptions.ConnectionError:
            print('----------Request Connection Error-----------')
            sleep(period)
            count_trying = count_trying + 1
            if(count_trying > retryConnection):
                print("-------------Some Problem In Server Communication -------------")
                break
    
    # Response from the server
    message_value = ast.literal_eval(resp.json())
    no_of_cluster = message_value['no_of_cluster']
<<<<<<< HEAD
    all_replied_gmailData = pd.DataFrame.from_dict(json.loads(message_value['all_replied_gmailData']), orient='columns')
    return all_replied_gmailData,no_of_cluster
=======
    all_replied_mailData = pd.DataFrame.from_dict(json.loads(message_value['all_replied_gmailData']), orient='columns')
    return all_replied_mailData,no_of_cluster
>>>>>>> c6d382fd523d649327c4b4a060edcccebeead96f


# Finding keywords in the subject and body
def callAPIKeywords(all_replied_mailData,no_of_cluster):
    headers = {'content-type': 'application/json'}
    individual_ClusterWiseKeyword = {}
    for iterate_no_of_cluster in range(no_of_cluster):
        successFlag = True
        count_trying = 0
        retryConnection = 10
        period = 10 #seconds
        cluster_wise_sub_body = all_replied_mailData.loc[all_replied_mailData['label'] == iterate_no_of_cluster]
        conv_list = []
        conv_list.append(' '.join(list(cluster_wise_sub_body['Subject'])))
        conv_list.append(' '.join(list(cluster_wise_sub_body['Body'])))
        all_data_conv_dict_from = {'subject_body_list':' '.join(conv_list)}
        while successFlag:
            try:
                #sending the data to the server
                resp = requests.post("http://127.0.0.1:8200/keywords",data = json.dumps(all_data_conv_dict_from),headers=headers)
                successFlag = False
            except requests.exceptions.ConnectionError:
                print('----------Request Connection Error-----------')
                sleep(period)
                count_trying = count_trying + 1
                if(count_trying > retryConnection):
                    print("-------------Some Problem In Server Communication -------------")
                    break

        # Response from the server
        message_value = ast.literal_eval(resp.json())
        keywords_output = message_value['keywords_output']
        individual_ClusterWiseKeyword[iterate_no_of_cluster] = keywords_output
    
    return individual_ClusterWiseKeyword


# Converting all objects to dictionary format
def converted_ToUserFormat(data_frame_excel,no_of_clusters):
    dict_subject = dict()
    no_of_emails = dict()
    for filter_value in range(no_of_clusters):
        individual_clusterwise = data_frame_excel.loc[data_frame_excel['label'] == filter_value].reset_index(drop=True)
        no_of_emails[filter_value] = len(individual_clusterwise)
        dict_subject[filter_value] = random.choice(individual_clusterwise['Subject'])
    return dict_subject,no_of_emails


# Get the clusters keyword,subject,avg_response,no_of_emails to view easily for UserInterface and User
def converted_ToUserInterface(data_frame_excel ,dict_individual_keyword_cluster,cluster_dict_subject,avg_response_time_for_clusters,no_emails_per_cluster,no_of_clusters):
    all_cluster_values = []

    for cluster_value in range(no_of_clusters):
        all_cluster_values.append({'cluster_value':cluster_value,'Keywords':dict_individual_keyword_cluster[cluster_value],'Subject':cluster_dict_subject[cluster_value],'Average_ResponseTime':str(avg_response_time_for_clusters[cluster_value])+' mins','No_Of_Emails':no_emails_per_cluster[cluster_value],'Messages':"Some Important Messages"})
    return (all_cluster_values)


# Function for displaying the selected cluster information and easily to understand viewers

weekDays = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

def charts_selected_cluster(label_data):
    global selected_clusterWeek
    global selected_clusterDay
    global selected_ClusterInformation

    label = int(label_data)
    labelled_emailData = all_replied_mailData.loc[all_replied_mailData['label'] == label].reset_index(drop=True)
    labelled_list = []
    for iterate in range(len(labelled_emailData)):
        dict_conv = OrderedDict()
        dict_conv = {'TimeDate':labelled_emailData['TimeDate'][iterate],'From':labelled_emailData['From'][iterate],'To':labelled_emailData['To'][iterate],'Subject':labelled_emailData['Subject'][iterate],'Body':labelled_emailData['Body'][iterate],'Thread_Id':labelled_emailData['Thread_Id'][iterate],'ResponseTime':labelled_emailData['ResponseTime'][iterate]}
        labelled_list.append(dict_conv)
  
    # DataStored for selected cluster
    clustered_Data,selected_ClusterInformation =  labelled_emailData,labelled_list

    # Converting String format of DateTime format
    clustered_Data['TimeDate'] = pd.to_datetime(clustered_Data['TimeDate'])

    # Initializing lists to store the data's for the graph representation and Information about the emails
    weekWise_Mails = []
    no_of_mails_occured=[]
    for i in range(len(clustered_Data)):
        weekWise_Mails.append(weekDays[clustered_Data['TimeDate'][i].weekday()])
    for i in weekDays:
        no_of_mails_occured.append(weekWise_Mails.count(i))
    selected_clusterWeek = dict()
    selected_clusterWeek = { "chart": {
                "caption": "Messages in week of selected cluster",
                "subCaption": "Your messages",
                "xAxisName": "Week",
                "yAxisName": "No_Of_Mails",
                "numberSuffix": " Emails",
                "theme": "fusion",
                }}
    list_appendWeekWiseValues=[]
    for i in range(7):
        list_appendWeekWiseValues.append({"label" : weekDays[i],"value":str(no_of_mails_occured[i]) })

    selected_clusterWeek.update({"data":list_appendWeekWiseValues})

    selected_clusterDay={ "chart": {
                "caption": "Messages In a Day of selected cluster",
                "subCaption": "Your messages",
                "xAxisName": "Hours",
                "yAxisName": "No_Of_Mails",
                "numberSuffix": " Emails",
                "theme": "fusion",
                }}
    list_appendHourWiseValues=[]

    hour_bins=["0:00 AM - 3:00 AM","3:00 AM - 6:00 AM","6:00 AM - 9:00 AM ","9:00 AM - 12:00 PM ","12:00 PM - 15:00 PM ","15:00 PM - 18:00 PM ","18:00 PM - 21:00 PM ","21:00 PM - 0:00 AM"]
    hour_WiseCounts=[0,0,0,0,0,0,0,0]
    for i in range(len(clustered_Data)):
        if(clustered_Data['TimeDate'][i].hour>=0 and clustered_Data['TimeDate'][i].hour<3):
            hour_WiseCounts[0]=hour_WiseCounts[0]+1
        if(clustered_Data['TimeDate'][i].hour>=3 and clustered_Data['TimeDate'][i].hour<6):
            hour_WiseCounts[1]=hour_WiseCounts[1]+1
        if(clustered_Data['TimeDate'][i].hour>=6 and clustered_Data['TimeDate'][i].hour<9):
            hour_WiseCounts[2]=hour_WiseCounts[2]+1
        if(clustered_Data['TimeDate'][i].hour>=9 and clustered_Data['TimeDate'][i].hour<12):
            hour_WiseCounts[3]=hour_WiseCounts[3]+1
        if(clustered_Data['TimeDate'][i].hour>=12 and clustered_Data['TimeDate'][i].hour<15):
            hour_WiseCounts[4]=hour_WiseCounts[4]+1
        if(clustered_Data['TimeDate'][i].hour>=15 and clustered_Data['TimeDate'][i].hour<18):
            hour_WiseCounts[5]=hour_WiseCounts[5]+1
        if(clustered_Data['TimeDate'][i].hour>=18 and clustered_Data['TimeDate'][i].hour<21):
            hour_WiseCounts[6]=hour_WiseCounts[6]+1
        if(clustered_Data['TimeDate'][i].hour>=21 and clustered_Data['TimeDate'][i].hour<=24):
            hour_WiseCounts[7]=hour_WiseCounts[7]+1

    for i in range(8):
        list_appendHourWiseValues.append({"label":hour_bins[i],"value":str(hour_WiseCounts[i])})
    selected_clusterDay.update({"data":list_appendHourWiseValues})
    
    print("------------------------Process For Selected Cluster Had Been Analysed------------------------")
    return {"status":"successfull"}


# Displaying graph for all clusters and return to the angular for displaying graphs

<<<<<<< HEAD
def all_clusterInformation(all_replied_gmailData):
    global all_clusterWeek
    global all_clusterDay

     # Converting String format of DateTime format
    all_replied_gmailData['TimeDate'] = pd.to_datetime(all_replied_gmailData['TimeDate'])

    # Initializing lists to store the data's for the graph representation and Information about the emails

    clustered_dayWise = []
    no_of_mails_in_week=[]
    for i in range(len(all_replied_gmailData)):
        clustered_dayWise.append(weekDays[all_replied_gmailData['TimeDate'][i].weekday()])
=======
def all_clusterInformation(all_replied_mailData):
    global all_clusterWeek
    global all_clusterDay

     # Converting String format of DateTime format
    all_replied_mailData['TimeDate'] = pd.to_datetime(all_replied_mailData['TimeDate'])

    # Initializing lists to store the data's for the graph representation and Information about the emails

    clustered_dayWise = []
    no_of_mails_in_week=[]
    for i in range(len(all_replied_mailData)):
        clustered_dayWise.append(weekDays[all_replied_mailData['TimeDate'][i].weekday()])
>>>>>>> c6d382fd523d649327c4b4a060edcccebeead96f
    for i in weekDays:
        no_of_mails_in_week.append(clustered_dayWise.count(i))
    all_clusterWeek = dict()
    all_clusterWeek = { "chart": {
                "caption": "Messages in week",
                "subCaption": "Your messages",
                "xAxisName": "Week",
                "yAxisName": "No_Of_Mails",
                "numberSuffix": " Emails",
                "theme": "fusion",
                }}
    append_allClusterWeekWise=[]
    for i in range(7):
        append_allClusterWeekWise.append({"label" : weekDays[i],"value":str(no_of_mails_in_week[i]) })

    all_clusterWeek.update({"data":append_allClusterWeekWise})

    all_clusterDay={ "chart": {
                "caption": "Messages In a Day",
                "subCaption": "Your messages",
                "xAxisName": "Hours",
                "yAxisName": "No_Of_Mails",
                "numberSuffix": " Emails",
                "theme": "fusion",
                }}
    append_allClusterDayWise=[]

    hour_bins = ["0:00 AM - 3:00 AM","3:00 AM - 6:00 AM","6:00 AM - 9:00 AM ","9:00 AM - 12:00 PM ","12:00 PM - 15:00 PM ","15:00 PM - 18:00 PM ","18:00 PM - 21:00 PM ","21:00 PM - 0:00 AM"]
    hour_WiseCounts=[0,0,0,0,0,0,0,0]
<<<<<<< HEAD
    for i in range(len(all_replied_gmailData)):
        if(all_replied_gmailData['TimeDate'][i].hour>=0 and all_replied_gmailData['TimeDate'][i].hour<3):
            hour_WiseCounts[0]=hour_WiseCounts[0]+1
        if(all_replied_gmailData['TimeDate'][i].hour>=3 and all_replied_gmailData['TimeDate'][i].hour<6):
            hour_WiseCounts[1]=hour_WiseCounts[1]+1
        if(all_replied_gmailData['TimeDate'][i].hour>=6 and all_replied_gmailData['TimeDate'][i].hour<9):
            hour_WiseCounts[2]=hour_WiseCounts[2]+1
        if(all_replied_gmailData['TimeDate'][i].hour>=9 and all_replied_gmailData['TimeDate'][i].hour<12):
            hour_WiseCounts[3]=hour_WiseCounts[3]+1
        if(all_replied_gmailData['TimeDate'][i].hour>=12 and all_replied_gmailData['TimeDate'][i].hour<15):
            hour_WiseCounts[4]=hour_WiseCounts[4]+1
        if(all_replied_gmailData['TimeDate'][i].hour>=15 and all_replied_gmailData['TimeDate'][i].hour<18):
            hour_WiseCounts[5]=hour_WiseCounts[5]+1
        if(all_replied_gmailData['TimeDate'][i].hour>=18 and all_replied_gmailData['TimeDate'][i].hour<21):
            hour_WiseCounts[6]=hour_WiseCounts[6]+1
        if(all_replied_gmailData['TimeDate'][i].hour>=21 and all_replied_gmailData['TimeDate'][i].hour<=24):
=======
    for i in range(len(all_replied_mailData)):
        if(all_replied_mailData['TimeDate'][i].hour>=0 and all_replied_mailData['TimeDate'][i].hour<3):
            hour_WiseCounts[0]=hour_WiseCounts[0]+1
        if(all_replied_mailData['TimeDate'][i].hour>=3 and all_replied_mailData['TimeDate'][i].hour<6):
            hour_WiseCounts[1]=hour_WiseCounts[1]+1
        if(all_replied_mailData['TimeDate'][i].hour>=6 and all_replied_mailData['TimeDate'][i].hour<9):
            hour_WiseCounts[2]=hour_WiseCounts[2]+1
        if(all_replied_mailData['TimeDate'][i].hour>=9 and all_replied_mailData['TimeDate'][i].hour<12):
            hour_WiseCounts[3]=hour_WiseCounts[3]+1
        if(all_replied_mailData['TimeDate'][i].hour>=12 and all_replied_mailData['TimeDate'][i].hour<15):
            hour_WiseCounts[4]=hour_WiseCounts[4]+1
        if(all_replied_mailData['TimeDate'][i].hour>=15 and all_replied_mailData['TimeDate'][i].hour<18):
            hour_WiseCounts[5]=hour_WiseCounts[5]+1
        if(all_replied_mailData['TimeDate'][i].hour>=18 and all_replied_mailData['TimeDate'][i].hour<21):
            hour_WiseCounts[6]=hour_WiseCounts[6]+1
        if(all_replied_mailData['TimeDate'][i].hour>=21 and all_replied_mailData['TimeDate'][i].hour<=24):
>>>>>>> c6d382fd523d649327c4b4a060edcccebeead96f
            hour_WiseCounts[7]=hour_WiseCounts[7]+1

    for i in range(8):
        append_allClusterDayWise.append({"label":hour_bins[i],"value":str(hour_WiseCounts[i])})
    all_clusterDay.update({"data":append_allClusterDayWise})
    return True


# Calling function for all subProcessFunction such as data filtering and api calls for Doc2Vec,Kmeans
<<<<<<< HEAD
def main():
    global stored_forUserInterface
    global all_replied_gmailData
    global all_data_FromGmail

    print("called")
    # collecting gmail data
    mails_Under_given_days = 2 # 1 month

    # request for service from gmail
    service = build('gmail', 'v1', credentials=main2())
      
    #list to extend(store) messages in corresponding pages
    messages = []

    # Call the Gmail API to fetch INBOX
    # get initialy upto 500 messages

    results = service.users().messages().list(userId='me',maxResults=500).execute()
    
    #extract messages to messages varialbe from result becaue we use "result" varialbe for n times
    messages.extend(results['messages'])
    page_token = results['nextPageToken']
    results = service.users().messages().list(userId='me',pageToken=page_token,maxResults=500).execute()
    messages.extend(results['messages'])
    #collect all messages based on pagetoken wise
    # while('nextPageToken' in results):
    #     page_token = results['nextPageToken']
    #     results = service.users().messages().list(userId='me',pageToken=page_token,maxResults=500).execute()
    #     messages.extend(results['messages'])

    #its the variale used to fetch all detail about threads (for future use)
    threads = service.users().threads().list(userId='me').execute().get('threads', [])

    # these are all the list to store each colomn data 
    From = []
    To = []
    Sub = []
    Body = []
    Thread_id = []
    Date = []
    batch = BatchHttpRequest()
    count = 0
    message_batch=[]
    #thes varialbe is used as a flag to integate whether we reach the given number of input days
    terminator = 0
    
    # function for batch request  
    def callback(request_id, response, exception):
        
        if exception is not None:
            print(response)
        else:
            message_batch.append(response)
            
    for mes in messages:
        # print("batching")
        batch.add(service.users().messages().get(userId='me', id=mes['id']),callback = callback)
    batch.execute()
    
    for message in message_batch:
        
        if(terminator>0):
            break
       
        #these are variables are used as flags which helps us in time of missing or unprovide null values
        To_flag=0
        Sub_flag=0
         #iterate through the message content to get the each colomn value
        for part in message['payload']['headers']:
            #to fetch date
            if(part['name']=='Date'):
                #to check the limited days
                if(((datetime.datetime.now() - (date_parser.parse(part['value'],fuzzy=True).replace(tzinfo=None)) ).days ) > mails_Under_given_days):
                    print('finished')
                    #change the flag state if the limits exceeded
                    terminator = 1
                Date.append(date_parser.parse(part['value'],fuzzy=True).replace(tzinfo=None))
            if part['name']=='From':
                From.append(','.join(re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",part['value'])))
            if part['name']=='To':
                To.append(','.join(re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",part['value'])))
                To_flag=1

            if(part['name']=='Subject'):
                Sub.append(part['value'])
                Sub_flag=1
        #if there is no any part value is as 'To' then the flag doesnt change so we encode 'None' value as Anonymous 
        if(To_flag==0):
            To.append('<unknown@gmail.com>')
        if(Sub_flag==0):
            Sub.append("No Content")
        Thread_id.append(message['threadId'])
        Body.append(message['snippet'])

    # dump all the list value in the dataframe
    data_frame_from_gmail = pd.DataFrame({'TimeDate':Date,'From':From,'To':To,'Subject':Sub,'Body':Body,'Thread_Id':Thread_id})

    # sorting the time to fetch first stimuli and first response and converting timedate formate str to datetime

    all_data_FromGmail = (data_frame_from_gmail.sort_values(by='TimeDate',ascending=True)).reset_index(drop=True)

    # calling function for the filtering replied emails and adding response time for the replied emails

    all_replied_gmailData,all_data_FromGmail,response_time_for_individual_thread_id = dataFiltering_AddingResponseTime(all_data_FromGmail)

    # converting datetime column to string to avoid overlapping in the data

    all_replied_gmailData['TimeDate'] = all_replied_gmailData['TimeDate'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
=======
def main(inputData):
    global stored_forUserInterface
    global all_replied_mailData
    global all_data_FromMail
    
    print("called")
    
    all_data_FromMail = inputData
    # # collecting gmail data
    # mails_Under_given_days = 30 # 1 month
    # all_data_FromMail = gmailIntegration(mails_Under_given_days)

    # calling function for the filtering replied emails and adding response time for the replied emails

    all_replied_mailData,all_data_FromMail,response_time_for_individual_thread_id = dataFiltering_AddingResponseTime(all_data_FromMail)

    # converting datetime column to string to avoid overlapping in the data

    all_replied_mailData['TimeDate'] = all_replied_mailData['TimeDate'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    print("Begining of text classification")
>>>>>>> c6d382fd523d649327c4b4a060edcccebeead96f
    # calling API function for doc2vec

    model_path = 'enwiki_dbow/doc2vec.bin'

    from_value = pd.DataFrame(callAPIDoc2Vec(model_path,list(all_replied_mailData['From'])))
    to_value = pd.DataFrame(callAPIDoc2Vec(model_path,list(all_replied_mailData['To'])))
    subject_value = pd.DataFrame(callAPIDoc2Vec(model_path,list(all_replied_mailData['Subject'])))
    body_value = pd.DataFrame(callAPIDoc2Vec(model_path,list(all_replied_mailData['Body'])))

    # concating all message values to single data frame
    full_data_frame_for_replied_emails = pd.concat([from_value,to_value,subject_value,body_value],axis=1)
    full_data_frame_for_replied_emails.columns = range(full_data_frame_for_replied_emails.shape[1])

<<<<<<< HEAD
    # function call for the API Kmeans
    percentage_of_predictingElbowMethod = 0.05
    all_replied_gmailData,no_of_cluster = callAPIKmeans(full_data_frame_for_replied_emails,percentage_of_predictingElbowMethod,all_replied_gmailData)
=======
    full_data_frame_for_replied_emails.to_csv("doc2vec.csv")
    all_replied_mailData.to_csv("all_gmailData.csv")
    
    print("Begining of Kmeans")
    # function call for the API Kmeans
    percentage_of_predictingElbowMethod = 0.05
    all_replied_mailData,no_of_cluster = callAPIKmeans(full_data_frame_for_replied_emails,percentage_of_predictingElbowMethod,all_replied_mailData)
>>>>>>> c6d382fd523d649327c4b4a060edcccebeead96f

    # # then detecting similar emails in all gmail data with some input data

    # def get_index_from_UserSelection():
    #     # get the data from the server UI
    #     requests_data = requests.get(url)#refer

    #     input_from_UI = 9  #input lenght gmailData
        
    #     return input_from_UI

    # calling function to find similar emails to the input data
<<<<<<< HEAD
    # detecting_similar_emails = detectingSimilarEmails(all_data_FromGmail,get_index_from_UserSelection(),model_path)

    # UI interface functions are done here

    clusterwise_avg_responsetime = avgResponseTime(all_replied_gmailData,response_time_for_individual_thread_id,no_of_cluster)
=======
    # detecting_similar_emails = detectingSimilarEmails(all_data_FromMail,get_index_from_UserSelection(),model_path)

    # UI interface functions are done here

    clusterwise_avg_responsetime = avgResponseTime(all_replied_mailData,response_time_for_individual_thread_id,no_of_cluster)
>>>>>>> c6d382fd523d649327c4b4a060edcccebeead96f

    print("Begining of Keywords fetching")
    # calling function to convert all objects to dict

    dict_individual_keyword_cluster  = callAPIKeywords(all_replied_mailData,no_of_cluster)

    # calling function to convert all objects to dict

<<<<<<< HEAD
    clusterwise_subject,no_emails_per_cluster = converted_ToUserFormat(all_replied_gmailData,no_of_cluster)

    # storing the information to easily to view in the UI and to understand user
    stored_forUserInterface = converted_ToUserInterface(all_replied_gmailData,dict_individual_keyword_cluster,clusterwise_subject,clusterwise_avg_responsetime,no_emails_per_cluster,no_of_cluster)
=======
    clusterwise_subject,no_emails_per_cluster = converted_ToUserFormat(all_replied_mailData,no_of_cluster)

    # storing the information to easily to view in the UI and to understand user
    stored_forUserInterface = converted_ToUserInterface(all_replied_mailData,dict_individual_keyword_cluster,clusterwise_subject,clusterwise_avg_responsetime,no_emails_per_cluster,no_of_cluster)
>>>>>>> c6d382fd523d649327c4b4a060edcccebeead96f
    stored_forUserInterface = sorted(stored_forUserInterface, key = lambda i: i['No_Of_Emails'])
    
    # function calling for all cluster graph

    all_clusterInformation(all_replied_mailData)

    print("*******************************    ALL function finised   ***********************************")
    return "Success"
   

# Function calling for ClusterWise Graph
# For hosting initialize the CORS and PORT number

# Below function for selected cluster from the all clusters visualize the individual week wise the number of mails
cors = CORS(app, resources={r"/week/cluster": {"origins": "*"}})
@app.route('/week/cluster', methods=['GET','POST'])
def api_CallSelectedWeekWiseCluster():
    try:
        return jsonify(selected_clusterWeek)
    except NameError:
        print("...........................Takes Sometimes for Loading............................")
        return (".........................Takes Sometimes for Loading.....................")

# Below function for selected cluster from the all clusters visualize the individual day wise the number of mails
cors = CORS(app, resources={r"/days/cluster": {"origins": "*"}})
@app.route('/days/cluster', methods=['GET','POST'])
def api_CallSelectedDayWiseCluster():
    try:
        return jsonify(selected_clusterDay)
    except NameError:
        print("...........................Takes Sometimes for Loading............................")
        return (".........................Takes Sometimes for Loading.....................")

# Below function for selected cluster from the all clusters visualize the information in the tabel format such "TimeDate,From,To,Subject,Body,Thread_Id,ResponseTime"

cors = CORS(app, resources={r"/clusterlabel": {"origins": "*"}})
@app.route('/clusterlabel', methods=['GET','POST'])
def api_CallSelectedClusterInformation():
    try:
        return jsonify(selected_ClusterInformation)
    except NameError:
        print("...........................Takes Sometimes for Loading............................")
        return (".........................Takes Sometimes for Loading.....................")
<<<<<<< HEAD


=======


>>>>>>> c6d382fd523d649327c4b4a060edcccebeead96f
# For hosting initialize the cors and address to server and getting data from the angular to route the selected cluster details page
cors = CORS(app, resources={r"/angtoflask": {"origins": "*"}})
@app.route('/angtoflask', methods=['POST'])
def detdata():
    try:
        raw_data = request.data
        req_value = raw_data.decode('utf-8')
        label_value = ast.literal_eval(req_value)['label']
        return jsonify(charts_selected_cluster(label_value))
    except NameError:
        print("...........................Takes Sometimes for Loading............................")
        return (".........................Takes Sometimes for Loading.....................")
<<<<<<< HEAD

=======
>>>>>>> c6d382fd523d649327c4b4a060edcccebeead96f


# Function calling for ClusterWise Graph
# For hosting initialize the CORS and PORT number

<<<<<<< HEAD
=======
# Function calling for ClusterWise Graph
# For hosting initialize the CORS and PORT number

>>>>>>> c6d382fd523d649327c4b4a060edcccebeead96f
# Below function for visualizing all clusters week wise the number of mails
cors = CORS(app, resources={r"/week": {"origins": "*"}})
@app.route('/week', methods=['GET','POST'])
def api_CallWeekWiseCluster():
    try:
        return jsonify(all_clusterWeek)
    except NameError:
        print("...........................Takes Sometimes for Loading............................")
        return (".........................Takes Sometimes for Loading.....................")

# Below function for visualizing all clusters day wise the number of mails

cors = CORS(app, resources={r"/days": {"origins": "*"}})
@app.route('/days', methods=['GET','POST'])
def api_CallDayWiseCluster():
    try:
        return jsonify(all_clusterDay)
    except NameError:
        print("...........................Takes Sometimes for Loading............................")
        return (".........................Takes Sometimes for Loading.....................")

# Below function for all clusters visualize the information in the tabel format such "ClusterLabel,Keywords,Subject,AverageResponseTime,No_of_Mails"

cors = CORS(app, resources={r"/": {"origins": "*"}})
@app.route('/', methods=['GET','POST'])
def api_CallClustersInformation():
    try:
        return jsonify(stored_forUserInterface)
    except NameError:
        print("...........................Takes Sometimes for Loading............................")
        return (".........................Takes Sometimes for Loading.....................")
<<<<<<< HEAD



# This below function gets the input from the angular to begin the gmailIntegration all other process
cors = CORS(app, resources={r"/gmail": {"origins": "*"}})
@app.route('/gmail', methods=['GET','POST'])
def api_InputFromAngular():
    if(request):
        print("************** Request Getted To Begin The Gmail Integration And All Other Process***************")
        if(main() == "Success"):
            print("*******************   Function Returned By Finishing The Analysis Process    ***********************")
            return jsonify({"Process":"Analysing Of Gmail Data had been Completed"})
=======



# This below function gets the input from the angular to begin the gmailIntegration all other process
cors = CORS(app, resources={r"/gmail": {"origins": "*"}})
@app.route('/gmail', methods=['GET','POST'])
def api_InputFromAngular_Gmail():
    if(request):
        print("************** Request Getted To Begin The Gmail Integration And All Other Process***************")
        if(main(gmailIntegration(mails_Under_given_days)) == "Success"):
            print("*******************   Function Returned By Finishing The Analysis Process    ***********************")
            return jsonify({"Process":"Analysing Of Gmail Data had been Completed"})


cors = CORS(app, resources={r"/outlook": {"origins": "*"}})
@app.route('/outlook', methods=['GET','POST'])
def api_InputFromAngular_Outlook():
    if(request):
        print("************** Request Getted To Begin The Outlook Integration And All Other Process***************")
        headers = {'content-type': 'application/json'}
        #sending the data to the server
        resp = requests.post("http://127.0.0.1:8000/outlook_run",data = json.dumps("Sending Request to Collect the Data"),headers=headers)
        message_value = ast.literal_eval(resp.json())
       
        data_frame = pd.DataFrame.from_dict(json.loads(message_value['data_frame']), orient='columns')
        data_frame['TimeDate'] = [datetime.datetime.strptime(x,"%Y-%m-%d %H:%M:%S") for x in data_frame['TimeDate']]

        print(data_frame)
        if(main(data_frame) == "Success"):
            print("*******************   Function Returned By Finishing The Analysis Process    ***********************")
            try:
                return jsonify({"Process":"Analysing Of Gmail Data had been Completed"})
            except AssertionError:
                print("assertion error throw")
>>>>>>> c6d382fd523d649327c4b4a060edcccebeead96f


# Running the flask server in the default address
app.run(use_reloader=False)
