import ast
import pandas as pd
import numpy as np
import json
import flask
from time import sleep
from collections import OrderedDict
import warnings
import requests
from flask import request, jsonify
from flask_cors import CORS
from googleapiclient.discovery import build
from sklearn.feature_extraction.text import TfidfVectorizer
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





'''
Importing components from the other folder to implement the main login file.

'''
from Component.GmailIntegration.gmail_integration import main2
from Component.ResponseTime.response_time import responseTimeCalculating,avgResponseTime
from Component.DetectSameEmails.detect_similar_emails import detectingSimilarEmails
# import loading

# ignoring warning
warnings.filterwarnings('ignore')



# app config for the flask
app = flask.Flask(__name__)
app.config["DEBUG"] = True



def dataFiltering_AddingResponseTime(all_gmail_data):
        
    # filter the replied emails
    count_list = list(all_gmail_data["Thread_Id"])
    count_by_filter = []

    for count_value in range(len(count_list)):
        count_by_filter.append(count_list.count(count_list[count_value]))
    all_gmail_data['Count_THREAD_ID'] = count_by_filter
    data_frame_excel_emails = (all_gmail_data.loc[all_gmail_data['Count_THREAD_ID'] >= 2]).reset_index(drop = True)

    # calling function for individual thread_id response time

    response_time_for_individual_thread_id = responseTimeCalculating(data_frame_excel_emails)

    # data for storing all replied emails and adding a column response time for each thread_id

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
    return (data_frame_excel_replied,all_gmail_data,response_time_for_individual_thread_id)









# applying doc2vec process for converting text or document of texts to vector spaces
# api call for doc2vec
def callAPIDoc2Vec(model_path,message_input):
    headers = {'content-type': 'application/json'}
    # print(message_input)
    all_data_conv_dict_from = {'model_path':model_path,'message_value':message_input}
    success_flag = True
    count_tring = 0
    retryConnection = 10
    period = 10 #seconds
    while success_flag:
        try:
            #sending the data to the server
            resp = requests.post("http://127.0.0.1:8200/doc2vec",data = json.dumps(all_data_conv_dict_from),headers=headers)
            success_flag = False
        except requests.exceptions.ConnectionError:
            print('----------Request Connection Error-----------')
            sleep(period)
            count_tring = count_tring + 1
            if(count_tring > retryConnection):
                print("-------------Some Problem Has been Occured----------")
                break

    #response from the server
    message_value = ast.literal_eval(resp.json())
    # print(message_value)
    return message_value['message_convert']




# after finishing applying kmeans clustering for the relevant emails that related with other emails
# api call for kmeans

def callAPIKmeans(full_data_frame_for_replied_emails,percentage_of_predictingElbowMethod,all_replied_gmailData):
    headers = {'content-type': 'application/json'}
    success_flag = True
    count_tring = 0
    retryConnection = 10
    period = 10 #seconds
    all_data_conv_dict_from = {'full_data_frame_for_replied_emails':(full_data_frame_for_replied_emails).to_json(),'percentage_of_predictingElbowMethod':percentage_of_predictingElbowMethod,'all_replied_emails':(all_replied_gmailData).to_json()}
    while success_flag:
        try:
            #sending the data to the server
            resp = requests.post("http://127.0.0.1:9200/kmeans",data = json.dumps(all_data_conv_dict_from),headers=headers)
            success_flag = False
        except requests.exceptions.ConnectionError:
            print('----------Request Connection Error-----------')
            sleep(period)
            count_tring = count_tring + 1
            if(count_tring > retryConnection):
                print("-------------Some Problem Has been Occured----------")
                break
    
    # response of the server
    message_value = ast.literal_eval(resp.json())
    no_of_cluster = message_value['no_of_cluster']
    print('**************************************callkmeans',all_replied_gmailData)
    all_replied_gmailData = pd.DataFrame.from_dict(json.loads(message_value['all_replied_gmailData']), orient='columns')
    print('**************************************callkmeans*2',all_replied_gmailData)
    return all_replied_gmailData,no_of_cluster


# finding keywords in the subject and body
def callAPIKeywords(all_replied_gmailData,no_of_cluster):
    headers = {'content-type': 'application/json'}
    dict_individual_keyword_cluster = {}
    for iterate_no_of_cluster in range(no_of_cluster):
        success_flag = True
        count_tring = 0
        retryConnection = 10
        period = 10 #seconds
        cluster_wise_sub_body = all_replied_gmailData.loc[all_replied_gmailData['label'] == iterate_no_of_cluster]
        conv_list = []
        conv_list.append(' '.join(list(cluster_wise_sub_body['Subject'])))
        conv_list.append(' '.join(list(cluster_wise_sub_body['Body'])))
        all_data_conv_dict_from = {'subject_body_list':' '.join(conv_list)}
        while success_flag:
            try:
                #sending the data to the server
                resp = requests.post("http://127.0.0.1:8200/keywords",data = json.dumps(all_data_conv_dict_from),headers=headers)
                success_flag = False
            except requests.exceptions.ConnectionError:
                print('----------Request Connection Error-----------')
                sleep(period)
                count_tring = count_tring + 1
                if(count_tring > retryConnection):
                    print("-------------Some Problem Has been Occured----------")
                    break

        # response of the server
        message_value = ast.literal_eval(resp.json())
        keywords_output = message_value['keywords_output']
        dict_individual_keyword_cluster[iterate_no_of_cluster] = keywords_output
    
    return dict_individual_keyword_cluster


# converting all objects to dict
def convert_dict(data_frame_excel,no_of_clusters):
    dict_subject = dict()
    no_of_emails = dict()
    for filter_value in range(no_of_clusters):
        individual_clusterwise = data_frame_excel.loc[data_frame_excel['label'] == filter_value].reset_index(drop=True)
        no_of_emails[filter_value] = len(individual_clusterwise)
        dict_subject[filter_value] = individual_clusterwise['Subject'][0]
    return dict_subject,no_of_emails



# get cluster has keyword,subject,avg_response,no_of_emails to view easily for UI and user
def get_clusterwise(data_frame_excel ,dict_individual_keyword_cluster,cluster_dict_subject,avg_response_time_for_clusters,no_emails_per_cluster,no_of_clusters):
    all_cluster_values = []

    # print(data_frame_excel)
    for cluster_value in range(no_of_clusters):
        all_cluster_values.append({'cluster_value':cluster_value,'Keywords':dict_individual_keyword_cluster[cluster_value],'Subject':cluster_dict_subject[cluster_value],'Average_ResponseTime':str(avg_response_time_for_clusters[cluster_value])+' mins','No_Of_Emails':no_emails_per_cluster[cluster_value],'Messages':"Some Important Messages"})
    return (all_cluster_values)



# function for displaying the selected cluster and easily to understand viewers

weekDays = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

def charts_selected_cluster(label_data):
    print(all_replied_gmailData)

    global UI_function_csv1
    global UI_function_csv2
    global data1

    label = int(label_data)
    labelled_emailData = all_replied_gmailData.loc[all_replied_gmailData['label'] == label].reset_index(drop=True)
    labelled_list = []
    for iterate in range(len(labelled_emailData)):
        dict_conv = OrderedDict()
        dict_conv = {'TimeDate':labelled_emailData['TimeDate'][iterate],'From':labelled_emailData['From'][iterate],'To':labelled_emailData['To'][iterate],'Subject':labelled_emailData['Subject'][iterate],'Body':labelled_emailData['Body'][iterate],'Thread_Id':labelled_emailData['Thread_Id'][iterate],'ResponseTime':labelled_emailData['ResponseTime'][iterate]}
        labelled_list.append(dict_conv)
    
    # print(labelled_emailData)

    data_csv,data1 =  labelled_emailData,labelled_list
    # print(data)
    # Preview the first 5 lines of the loaded data
    data_csv['TimeDate'] = pd.to_datetime(data_csv['TimeDate'])
    day_wise_list_csv = []
    height_csv=[]
    for i in range(len(data_csv)):
        day_wise_list_csv.append(weekDays[data_csv['TimeDate'][i].weekday()])
    for i in weekDays:
        height_csv.append(day_wise_list_csv.count(i))
    UI_function_csv1 = dict()
    UI_function_csv1 = { "chart": {
                "caption": "Messages in week of selected cluster",
                "subCaption": "Your messages",
                "xAxisName": "Week",
                "yAxisName": "No_Of_Mails",
                "numberSuffix": " Emails",
                "theme": "fusion",
                }}
    li_csv=[]
    for i in range(7):
        li_csv.append({"label" : weekDays[i],"value":str(height_csv[i]) })

    UI_function_csv1.update({"data":li_csv})

    UI_function_csv2={ "chart": {
                "caption": "Messages In a Day of selected cluster",
                "subCaption": "Your messages",
                "xAxisName": "Hours",
                "yAxisName": "No_Of_Mails",
                "numberSuffix": " Emails",
                "theme": "fusion",
                }}
    li2_csv=[]

    hour_bin_csv=["0:00 AM - 3:00 AM","3:00 AM - 6:00 AM","6:00 AM - 9:00 AM ","9:00 AM - 12:00 PM ","12:00 PM - 15:00 PM ","15:00 PM - 18:00 PM ","18:00 PM - 21:00 PM ","21:00 PM - 0:00 AM"]
    hist_hour_count_csv=[0,0,0,0,0,0,0,0]
    for i in range(len(data_csv)):
        if(data_csv['TimeDate'][i].hour>=0 and data_csv['TimeDate'][i].hour<3):
            hist_hour_count_csv[0]=hist_hour_count_csv[0]+1
        if(data_csv['TimeDate'][i].hour>=3 and data_csv['TimeDate'][i].hour<6):
            hist_hour_count_csv[1]=hist_hour_count_csv[1]+1
        if(data_csv['TimeDate'][i].hour>=6 and data_csv['TimeDate'][i].hour<9):
            hist_hour_count_csv[2]=hist_hour_count_csv[2]+1
        if(data_csv['TimeDate'][i].hour>=9 and data_csv['TimeDate'][i].hour<12):
            hist_hour_count_csv[3]=hist_hour_count_csv[3]+1
        if(data_csv['TimeDate'][i].hour>=12 and data_csv['TimeDate'][i].hour<15):
            hist_hour_count_csv[4]=hist_hour_count_csv[4]+1
        if(data_csv['TimeDate'][i].hour>=15 and data_csv['TimeDate'][i].hour<18):
            hist_hour_count_csv[5]=hist_hour_count_csv[5]+1
        if(data_csv['TimeDate'][i].hour>=18 and data_csv['TimeDate'][i].hour<21):
            hist_hour_count_csv[6]=hist_hour_count_csv[6]+1
        if(data_csv['TimeDate'][i].hour>=21 and data_csv['TimeDate'][i].hour<=24):
            hist_hour_count_csv[7]=hist_hour_count_csv[7]+1

    for i in range(8):
        li2_csv.append({"label":hour_bin_csv[i],"value":str(hist_hour_count_csv[i])})
    UI_function_csv2.update({"data":li2_csv})
    
    return {"status":"successfull"}
  


# displaying graph for all clusters
def all_clusterInformation(all_replied_gmailData):
    print("all_cluster_info----------------------------------")
    print(all_replied_gmailData)
    global UI_function1
    global UI_function2

    all_replied_gmailData['TimeDate'] = pd.to_datetime(all_replied_gmailData['TimeDate'])

    day_wise_list = []
    height=[]
    for i in range(len(all_replied_gmailData)):
        day_wise_list.append(weekDays[all_replied_gmailData['TimeDate'][i].weekday()])
    for i in weekDays:
        height.append(day_wise_list.count(i))
    UI_function1 = dict()
    UI_function1 = { "chart": {
                "caption": "Messages in week",
                "subCaption": "Your messages",
                "xAxisName": "Week",
                "yAxisName": "No_Of_Mails",
                "numberSuffix": " Emails",
                "theme": "fusion",
                }}
    li=[]
    for i in range(7):
        li.append({"label" : weekDays[i],"value":str(height[i]) })

    UI_function1.update({"data":li})

    UI_function2={ "chart": {
                "caption": "Messages In a Day",
                "subCaption": "Your messages",
                "xAxisName": "Hours",
                "yAxisName": "No_Of_Mails",
                "numberSuffix": " Emails",
                "theme": "fusion",
                }}
    li2=[]

    hour_bin=["0:00 AM - 3:00 AM","3:00 AM - 6:00 AM","6:00 AM - 9:00 AM ","9:00 AM - 12:00 PM ","12:00 PM - 15:00 PM ","15:00 PM - 18:00 PM ","18:00 PM - 21:00 PM ","21:00 PM - 0:00 AM"]
    hist_hour_count=[0,0,0,0,0,0,0,0]
    for i in range(len(all_replied_gmailData)):
        if(all_replied_gmailData['TimeDate'][i].hour>=0 and all_replied_gmailData['TimeDate'][i].hour<3):
            hist_hour_count[0]=hist_hour_count[0]+1
        if(all_replied_gmailData['TimeDate'][i].hour>=3 and all_replied_gmailData['TimeDate'][i].hour<6):
            hist_hour_count[1]=hist_hour_count[1]+1
        if(all_replied_gmailData['TimeDate'][i].hour>=6 and all_replied_gmailData['TimeDate'][i].hour<9):
            hist_hour_count[2]=hist_hour_count[2]+1
        if(all_replied_gmailData['TimeDate'][i].hour>=9 and all_replied_gmailData['TimeDate'][i].hour<12):
            hist_hour_count[3]=hist_hour_count[3]+1
        if(all_replied_gmailData['TimeDate'][i].hour>=12 and all_replied_gmailData['TimeDate'][i].hour<15):
            hist_hour_count[4]=hist_hour_count[4]+1
        if(all_replied_gmailData['TimeDate'][i].hour>=15 and all_replied_gmailData['TimeDate'][i].hour<18):
            hist_hour_count[5]=hist_hour_count[5]+1
        if(all_replied_gmailData['TimeDate'][i].hour>=18 and all_replied_gmailData['TimeDate'][i].hour<21):
            hist_hour_count[6]=hist_hour_count[6]+1
        if(all_replied_gmailData['TimeDate'][i].hour>=21 and all_replied_gmailData['TimeDate'][i].hour<=24):
            hist_hour_count[7]=hist_hour_count[7]+1

    for i in range(8):
        li2.append({"label":hour_bin[i],"value":str(hist_hour_count[i])})
    UI_function2.update({"data":li2})
    return True








def main():
    global UI_function
    global all_replied_gmailData


    print("called")
    # collecting gmail data
    mails_Under_given_days = 2 # 1 month
    









    # request for service from gmail
    service = build('gmail', 'v1', credentials=main2())
    # webbrowser.open('http://localhost:4200/all',new=0)
    #for route to gmail integration
      

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
        #get complete data of each message
        
        
        #these are variables are used as flags which helps us in time of missing or unprovide null values
        To_flag=0
        Sub_flag=0
         #iterate through the message content to get the each colomn value
        for part in message['payload']['headers']:
            #to fetch date
            if(part['name']=='Date'):
                #print(    (    (datetime.datetime.now()  -    (date_parser.parse(part['value'],fuzzy=True).replace(tzinfo=None)) ).days )    )
                #to check the limited days
                if(  (    (datetime.datetime.now()  -    (date_parser.parse(part['value'],fuzzy=True).replace(tzinfo=None)) ).days ) > mails_Under_given_days):
                    print('finished')
                    #change the flag state if the limits exceeded
                    terminator = 1
                #if((datetime.datetime.now()  -    (date_parser.parse(part['value'],fuzzy=True).replace(tzinfo=None)) )  )
                Date.append(date_parser.parse(part['value'],fuzzy=True).replace(tzinfo=None))
            if part['name']=='From':
                # print(part['value'])
                From.append(','.join(re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",part['value'])))
            if part['name']=='To':
                # print(part['value'])
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
        print(count)
        count = count+1

        #print(count)
        #print("\n************\n")
    
    #     print(message)
    # print(len(Date))
    # print(len(From))
    # print(len(To))
    # print(len(Sub))
    # print(len(Body))
    # print(len(Thread_id))

    # dump all the list value in the dataframe
    data_frame_excel = pd.DataFrame({'TimeDate':Date,'From':From,'To':To,'Subject':Sub,'Body':Body,'Thread_Id':Thread_id})

    # sorting the time to fetch first stimuli and first response and converting timedate formate str to datetime

    all_gmail_data = (data_frame_excel.sort_values(by='TimeDate',ascending=True)).reset_index(drop=True)
    

    







































    # all_gmail_data = pd.read_csv("all_gmail_data.csv")

    # function for data_filtering and finding response time for the all replied emails
   

    # calling function for the filtering replied emails and adding response time for the replied emails
    all_replied_gmailData,all_gmail_data,response_time_for_individual_thread_id = dataFiltering_AddingResponseTime(all_gmail_data)

    # converting datetime column to string to avoid overlapping in the data
    all_replied_gmailData['TimeDate'] = all_replied_gmailData['TimeDate'].dt.strftime('%Y-%m-%d %H:%M:%S')
    
    # all_gmail_data = pd.read_csv('all_gmailData.csv')
    # all_replied_gmailData = pd.read_csv('all_replied_gmailData.csv')
    print("Responsetime+++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(all_replied_gmailData)

    # calling API function for doc2vec

    model_path = 'enwiki_dbow/doc2vec.bin'

    from_value = pd.DataFrame(callAPIDoc2Vec(model_path,list(all_replied_gmailData['From'])))
    to_value = pd.DataFrame(callAPIDoc2Vec(model_path,list(all_replied_gmailData['To'])))
    subject_value = pd.DataFrame(callAPIDoc2Vec(model_path,list(all_replied_gmailData['Subject'])))
    body_value = pd.DataFrame(callAPIDoc2Vec(model_path,list(all_replied_gmailData['Body'])))

    # concating all message values to single data frame
    full_data_frame_for_replied_emails = pd.concat([from_value,to_value,subject_value,body_value],axis=1)
    full_data_frame_for_replied_emails.columns = range(full_data_frame_for_replied_emails.shape[1])

    # full_data_frame_for_replied_emails = pd.read_csv("full_data_frame_for_replied_emails.csv")
    print("Doc2Vec+++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(all_replied_gmailData)

    # function call for the API Kmeans
    percentage_of_predictingElbowMethod = 0.05
    all_replied_gmailData,no_of_cluster = callAPIKmeans(full_data_frame_for_replied_emails,percentage_of_predictingElbowMethod,all_replied_gmailData)

    print("+++++++++++++++++++++++++++++++++Kmeans++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print(all_replied_gmailData)
    
    # all_replied_gmailData['TimeDate'] = pd.to_datetime(all_replied_gmailData['TimeDate'])

    
    # # converting sec to correct datetime object    
    # all_replied_gmailData['TimeDate'] = pd.to_datetime(all_replied_gmailData['TimeDate'])

    # # then detecting similar emails in all gmail data with some input data

    # def get_index_from_UserSelection():
    #     # get the data from the server UI
    #     requests_data = requests.get(url)#refer

    #     input_from_UI = 9  #input lenght gmailData
        
    #     return input_from_UI

    # calling function to find similar emails to the input data
    # detecting_similar_emails = detectingSimilarEmails(all_gmail_data,get_index_from_UserSelection(),model_path)

    # UI interface functions are done here

    avg_response_time = avgResponseTime(all_replied_gmailData,response_time_for_individual_thread_id,no_of_cluster)

    # calling function to convert all objects to dict

    dict_individual_keyword_cluster  = callAPIKeywords(all_replied_gmailData,no_of_cluster)

    # calling function to convert all objects to dict

    cluster_dict_subject,no_emails_per_cluster = convert_dict(all_replied_gmailData,no_of_cluster)

    # storing the information to easily to view in the UI and to understand user
    UI_function = get_clusterwise(all_replied_gmailData,dict_individual_keyword_cluster,cluster_dict_subject,avg_response_time,no_emails_per_cluster,no_of_cluster)
    UI_function = sorted(UI_function, key = lambda i: i['No_Of_Emails'])
    
    # function calling for all cluster graph

    all_clusterInformation(all_replied_gmailData)

    print("*********************    ALL function finised   ***********************************")
    return "success"


 
   
#function calling for all cluster graph
# for hosting initialize the cors and address to server
cors = CORS(app, resources={r"/week/cluster": {"origins": "*"}})
@app.route('/week/cluster', methods=['GET','POST'])
def api_all10():
    try:
        return jsonify(UI_function_csv1)
    except NameError:
        print("Its Takes Sometimes to Loading.....................")
        return ("Its Takes Sometimes to Loading.....................")

cors = CORS(app, resources={r"/days/cluster": {"origins": "*"}})
@app.route('/days/cluster', methods=['GET','POST'])
def api_all11():
    try:
        return jsonify(UI_function_csv2)
    except NameError:
        print("Its Takes Sometimes to Loading.....................")
        return ("Its Takes Sometimes to Loading.....................")

cors = CORS(app, resources={r"/clusterlabel": {"origins": "*"}})
@app.route('/clusterlabel', methods=['GET','POST'])
def api_all12():
    try:
        return jsonify(data1)
    except NameError:
        print("Its Takes Sometimes to Loading.....................")
        return ("Its Takes Sometimes to Loading.....................")



# # for hosting initialize the cors and address to server and getting data from angular
cors = CORS(app, resources={r"/angtoflask": {"origins": "*"}})
@app.route('/angtoflask', methods=['POST'])
def detdata():
    try:
        raw_data = request.data
        req_value = raw_data.decode('utf-8')
        label_value = ast.literal_eval(req_value)['label']
        return jsonify(charts_selected_cluster(label_value))
    except NameError:
        print("Its Takes Sometimes to Loading.....................")
        return ("Its Takes Sometimes to Loading.....................")



# for hosting initialize the cors and address to server
cors = CORS(app, resources={r"/week": {"origins": "*"}})
@app.route('/week', methods=['GET','POST'])
def api_all1():
    try:
        return jsonify(UI_function1)
    except NameError:
        print("Its Takes Sometimes to Loading.....................")
        return ("Its Takes Sometimes to Loading.....................")

cors = CORS(app, resources={r"/days": {"origins": "*"}})
@app.route('/days', methods=['GET','POST'])
def api_all2():
    try:
        return jsonify(UI_function2)
    except NameError:
        print("Its Takes Sometimes to Loading.....................")
        return ("Its Takes Sometimes to Loading.....................")

cors = CORS(app, resources={r"/": {"origins": "*"}})
@app.route('/', methods=['GET','POST'])
def api_all():
    try:
        return jsonify(UI_function)
    except NameError:
        print("Its Takes Sometimes to Loading.....................")
        return ("Its Takes Sometimes to Loading.....................")


    












# running the app in flask default address
cors = CORS(app, resources={r"/gmail": {"origins": "*"}})
@app.route('/gmail', methods=['GET','POST'])
def api_all_gmail():
    if(request):
        print("************** reguest getted ***************")
        if(main() == "success"):
            print("*******************   main returned    ***********************")
            return jsonify({"hi":"frank"})

        

        




app.run(use_reloader=False)


