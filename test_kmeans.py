
import ast
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
import os
'''
Importing components from the other folder to implement the main login file.

'''
from Component.GmailIntegration.gmail_integration import gmailIntegration
# from Component.OutlookIntegration.outlook import outlook
from Component.ResponseTime.response_time import responseTimeCalculating,avgResponseTime
from Component.DetectSameEmails.detect_similar_emails import detectingSimilarEmails










def callAPIKmeans(full_data_frame_for_replied_emails,percentage_of_predictingElbowMethod,all_replied_mailData):
    headers = {'content-type': 'application/json'}
    successFlag = True
    count_trying = 0
    retryConnection = 10
    period = 10 #seconds
    all_data_conv_dict_from = {'full_data_frame_for_replied_emails':(full_data_frame_for_replied_emails).to_json(),'percentage_of_predictingElbowMethod':percentage_of_predictingElbowMethod,'all_replied_emails':(all_replied_mailData).to_json()}
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
    all_replied_mailData = pd.DataFrame.from_dict(json.loads(message_value['all_replied_gmailData']), orient='columns')
    return all_replied_mailData,no_of_cluster