'''
Component : responseTime

responseTimeCalculating : This Function will establish the ResponseTime for the Individual Thread_id that  means which has calculated for only replied emails
avgResponseTime : This function will find the averageResponseTime for the each clustered labels.

Conditions : Python 3.7.4

Libraries : requirements.txt

Instructions :
                1.required columns are 'TimeDate','From','To','Thread_Id','labels'
                2.this will be used for all thread_id concepts

INPUT: This input has taken from the gmail API using messages()
        Dataframe

        TimeDate            From                    To                                      Thread_Id            labels
2019-07-05 16:54:40     illakiyan@gmail.com       ajith@gmail.com                      16e9ebf3d0810850            0
2019-07-05 16:54:40     lingesh@gmail.com         frank@gmail.com,ajith@gmail.com     16e9ebf3d0810834             1
2019-07-05 16:54:40     ajith@gmail.com           illakiyan@gmail.com                 16e9ebf3d0810850             0
2019-07-05 16:54:40     frank@gmail.com           lingesh@gmail.com                   16e9ebf3d0810834             1
       ---------------------------------------------------------------------------------------------------------------------- 
        no_of_clusters = 2
       ---------------------------------------------------------------------------------------------------------------------
OUTPUT:
        This output has obtain from the email replied messages and output will be interface with the UI

        responseTimeCalculating :
                        OUTPUT:dict
                        {'16e9ebf3d0810850':56.98
                        '16e9ebf3d0810834':34.00}
       -------------------------------------------------------------------------------------------------------------------------
       This will return the averageResponseTime for the cluster wise labels

       avgResponseTime : 
                        OUTPUT:dict
                        {'0':56.98
                         '1':34.00}
       --------------------------------------------------------------------------------------------------------------------------
''' 


import pandas as pd
import numpy as np
from dateparser import parse

# Function for calculating response time for the individual thread_id

'''
INPUT: This input has taken from the gmail API using messages()
        Dataframe

        TimeDate            From                    To                                      Thread_Id            labels
2019-07-05 16:54:40     illakiyan@gmail.com       ajith@gmail.com                      16e9ebf3d0810850            0
2019-07-05 16:54:40     lingesh@gmail.com         frank@gmail.com,ajith@gmail.com     16e9ebf3d0810834             1
2019-07-05 16:54:40     ajith@gmail.com           illakiyan@gmail.com                 16e9ebf3d0810850             0
2019-07-05 16:54:40     frank@gmail.com           lingesh@gmail.com                   16e9ebf3d0810834             1

'''

def responseTimeCalculating(data_frame_excel):
    #initialize variables
    response_time_dict = {}
    unique_thread_id_list = []
    index_marking = data_frame_excel.index #shape of the dataframe    

    # unique thread id taken from the replied email
    for all_thread_id_index in range(index_marking[0],index_marking[-1]+1):
        if data_frame_excel['Thread_Id'][all_thread_id_index] not in unique_thread_id_list:
            unique_thread_id_list.append(data_frame_excel['Thread_Id'][all_thread_id_index])

    # calculating response time for the replied emails
    for cal_resp in range(len(unique_thread_id_list)):
        individual_messages = (data_frame_excel.loc[data_frame_excel['Thread_Id'] == unique_thread_id_list[cal_resp]]).reset_index(drop = True)
        response_time_minute = -1
        for value_check in range(len(individual_messages)):
            from_value = (individual_messages['From'][value_check]).split(',')
            to_value = (individual_messages['To'][value_check]).split(',')
            timestamp_value = individual_messages['TimeDate'][value_check]
            for resp_time in range(value_check+1,len(individual_messages)):
                for from_value_check in (individual_messages['From'][resp_time]).split(','):
                    if str(from_value_check) in to_value:
                        for to_value_check in (individual_messages['To'][resp_time]).split(','):
                            if str(to_value_check) in from_value:
                                response_time_minute = round(((abs(individual_messages['TimeDate'][resp_time] - timestamp_value).total_seconds())/60),2)
                        break
        response_time_dict[unique_thread_id_list[cal_resp]] = response_time_minute
        
    # deleting unreplied emails
    delete_list = []
    for keys,values in response_time_dict.items():
        if values == -1:
            delete_list.append(keys)
    for delete in delete_list:
        del response_time_dict[delete]

    return (response_time_dict)

# calculating average response time for individual clusters

'''
INPUT: This input has taken from the gmail API using messages()
        data_frame_excel : Dataframe

        TimeDate            From                    To                                      Thread_Id            labels
2019-07-05 16:54:40     illakiyan@gmail.com       ajith@gmail.com                      16e9ebf3d0810850            0
2019-07-05 16:54:40     lingesh@gmail.com         frank@gmail.com,ajith@gmail.com     16e9ebf3d0810834             1
2019-07-05 16:54:40     ajith@gmail.com           illakiyan@gmail.com                 16e9ebf3d0810850             0
2019-07-05 16:54:40     frank@gmail.com           lingesh@gmail.com                   16e9ebf3d0810834             1

----------------------------------------------------------------------------------------------------------------------------------

    response_time_for_individual_thread_id = dict
    
    {'16e9ebf3d0810850':56.98,'16e9ebf3d0810834':34.00}

------------------------------------------------------------------------------------------------------------------------------------

no_of_cluster = 2 (format : integer)
-------------------------------------------------------------------------------------------------------------------------------------
'''

def avgResponseTime(data_frame_excel,response_time_for_individual_thread_id,no_of_clusters):
    clustered_avg_response_time = {}
    for cluster_value in range(no_of_clusters):
        individual_cluster = data_frame_excel.loc[data_frame_excel["label"] == cluster_value]
        unique_thread_id_list = individual_cluster['Thread_Id'].unique()
        sum_value = 0
        for unique_value in range(len(unique_thread_id_list)):
            sum_value = sum_value + response_time_for_individual_thread_id[unique_thread_id_list[unique_value]]
        clustered_avg_response_time[cluster_value] = round((sum_value)/len(unique_thread_id_list),2)
    return clustered_avg_response_time





