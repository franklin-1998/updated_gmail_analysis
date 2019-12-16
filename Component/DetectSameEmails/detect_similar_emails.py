'''
Component : Detecting Similar Emails

detectingSimilarEmails : This function shows the top similar emails for input emails data

Conditions : Python 3.7.4

Libraries : requirements.txt

Instructions :
                1.required columns are 'From','To','Subject','Body'.
                2.Api call for doc2vec process and pca process it is in  server (microservice).
                3.this will be used for all email concepts such as outlook,gmail,yahoo etc...

INPUT:This input has taken from the gmail API using messages()
        data_frame_excel :  Dataframe

        TimeDate            From                    To                               Subject                    Body                         Thread_Id
2019-07-05 16:54:41     illakiyan@gmail.com       ajith@gmail.com                   Document...                 This document has....      16e9ebf3d0810850    
2019-07-23 15:59:44     lingesh@gmail.com         frank@gmail.com,ajith@gmail.com   Getting Some ....           Info of our Project...     16e9ebf3d0810834 
2019-07-06 06:45:06     ajith@gmail.com           illakiyan@gmail.com               Status of our project...    Things related....         16e9ebf3d0810851 
2019-07-17 03:20:00     frank@gmail.com           lingesh@gmail.com                 Re : Getting Some ....      Beyond your questions...   16e9ebf3d0810834 
------------------------------------------------------------------------------------------------------------------------------------------------------ 

        model_path : './microservice/enwiki_dow/doc2vec.bin'

------------------------------------------------------------------------------------------------------------------------------------------------------------------

        index_of_gmailData_inputData : 3

------------------------------------------------------------------------------------------------------------------------------------------------------------------

OUTPUT:

    Future Process : This will be shown in UI for the user's analysis for better understanding that these are the top similar emails relevant to selected emails.
        
    output_for_similar_emails :  Dataframe

        TimeDate            From                    To                               Subject                    Body                         Thread_Id              Distance        SimilarEmails
2019-07-05 16:54:41     illakiyan@gmail.com       ajith@gmail.com                   Document...                 This document has....      16e9ebf3d0810850             0.03         Very Closest
2019-07-23 15:59:44     lingesh@gmail.com         frank@gmail.com,ajith@gmail.com   Getting Some ....           Info of our Project...     16e9ebf3d0810834             0.12            Closest

------------------------------------------------------------------------------------------------------------------------------------------------

'''

import math
import requests
import json
import numpy as np
import pandas as pd
import ast
from collections import OrderedDict 

def detectingSimilarEmails(all_gmail_data,index_of_gmailData_inputData,model_path):

    # api call for doc2vec and pca has to be processed
    def callAPIDoc2Vec(model_path,message_input):
        headers = {'content-type': 'application/json'}
        # print(message_input)
        all_data_conv_dict_from = {'model_path':model_path,'message_value':message_input}
        resp = requests.post("http://127.0.0.1:8200/doc2vec",data = json.dumps(all_data_conv_dict_from),headers=headers)
        #response from the server
        message_value = ast.literal_eval(resp.json())
        # print(message_value)
        return message_value['message_convert']

    # converting the emails to doc2vec vector spaces
    from_value_check = pd.DataFrame(callAPIDoc2Vec(model_path,list(all_gmail_data['From'])))
    to_value_check = pd.DataFrame(callAPIDoc2Vec(model_path,list(all_gmail_data['To'])))
    subject_value_check = pd.DataFrame(callAPIDoc2Vec(model_path,list(all_gmail_data['Subject'])))
    body_value_check = pd.DataFrame(callAPIDoc2Vec(model_path,list(all_gmail_data['Body'])))

    output_data_frame = (pd.concat([from_value_check,to_value_check,subject_value_check,body_value_check],axis=1)).reset_index(drop=True)

    output_data_frame.columns = range(output_data_frame.shape[1])

    # calling api call for applying pca
    def callAPIPCA(message_input):
        headers = {'content-type': 'application/json'}
        # print(message_input)
        all_data_conv_dict_from = {'message_value':(message_input).to_json()}
        resp = requests.post("http://127.0.0.1:8200/doc2vec",data = json.dumps(all_data_conv_dict_from),headers=headers)
        #response from the server
        message_value = ast.literal_eval(resp.json())
        return (pd.DataFrame.from_dict(json.loads(message_value['pca_output']), orient='columns'))

    pca_output = callAPIPCA(output_data_frame)

    # indexing for separating the test data and gmail data
    gmailData_frame_pca = pca_output.iloc[0:index_of_gmailData_inputData]
    
    data_frame_excel = all_gmail_data.iloc[0:index_of_gmailData_inputData].reset_index(drop=True)
    
    inputData_frame_pca = pca_output.iloc[index_of_gmailData_inputData:].reset_index(drop=True)

    distance_value = []

    # calculating the sum of distance for gmail data with all input data
    for gmail_data in range(len(gmailData_frame_pca)):
        sum_list = []
        sum_value = []
        for input_data in range(len(inputData_frame_pca)):
            sum_value.append((gmailData_frame_pca.iloc[gmail_data] - inputData_frame_pca.iloc[input_data])**2)
            square_root_list = []
            for sqrt in range(len(sum_value[0])):
                square_root_list.append(math.sqrt(sum_value[0][sqrt]))
            sum_list.append(sum(square_root_list))
            sum_value = []
        distance_value.append(sum(sum_list))



    data_frame_excel['Distance'] = distance_value
    data_frame_excel.sort_values("Distance",axis = 0,ascending = True,inplace = True,na_position = 'last')
    data_frame_excel = data_frame_excel.reset_index(drop=True)

    distance_list = list(data_frame_excel['Distance'])

    # taking percentage of the list for top emails list
    five_percent = round(len(distance_list) * 0.05)
    first_ten_percent = round(len(distance_list[five_percent:]) * 0.10)
    second_ten_percent = round(len(distance_list[first_ten_percent:]) * 0.10)

    dict_for_percent_and_names = OrderedDict() 
    dict_for_percent_and_names['Very Closest'] = five_percent
    dict_for_percent_and_names['Closest'] = first_ten_percent
    dict_for_percent_and_names['Far'] = second_ten_percent
    
    similar_names = []

    for keys,values in dict_for_percent_and_names.items():
        for val in range(values):
            similar_names.append(keys)

    # appending relevant top emails for the gmail data
    output_for_similar_emails = data_frame_excel.iloc[:len(similar_names)]

    output_for_similar_emails['Similar Emails'] = similar_names

    return (output_for_similar_emails)