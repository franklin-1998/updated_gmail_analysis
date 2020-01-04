'''
MicroService : ML_Classifiers(KMeans Clustering)

kmeansClustering : This function returns the clusters of related to same content emails

Conditions : Python 3.7.4

Libraries : requirements.txt

Server Information : This will be hosted in flask server()

Instructions :
                1.required columns are any numerical columns are accepted.
                2.KMeans used for any numerical columns such as texts and documentText converted to numerical term or vector spaces.

INPUT:This input has taken from the gmail API using messages()

      data_frame_excel :  Dataframe

        TimeDate            From                    To                               Subject                    Body                         Thread_Id 
2019-07-05 16:54:41     illakiyan@gmail.com       ajith@gmail.com                   Document...                 This document has....      16e9ebf3d0810850             
2019-07-23 15:59:44     lingesh@gmail.com         frank@gmail.com,ajith@gmail.com   Getting Some ....           Info of our Project...     16e9ebf3d0810834            
2019-07-06 06:45:06     ajith@gmail.com           illakiyan@gmail.com               Status of our project...    Things related....         16e9ebf3d0810851             
2019-07-17 03:20:00     frank@gmail.com           lingesh@gmail.com                 Re : Getting Some ....      Beyond your questions...   16e9ebf3d0810834         
       ---------------------------------------------------------------------------------------------------------------------- 
    percentage_of_predicting = 0.05
       ---------------------------------------------------------------------------------------------------------------------
      full_data_frame_of_email : Dataframe

    0       1       2       3       4       5       ........        1199       1200 
   0.32    0.023   0.07    0.09    0.087   0.056                    0.003      0.034
   0.34    0.045   0.07    0.43    0.032   0.0534                   0.012      0.65
   0.67    0.076   0.45    0.34    0.087   0.0435                   0.312      0.04
   0.098   0.098   0.67    0.43    0.056   0.034                    0.324      0.34
    .       .       .       .       .       .                        .          .
    .       .       .       .       .       .                        .          .
    .       .       .       .       .       .                        .          .
   0.345   0.012   0.97    0.2445  0.545   0.022                    0.234      0.324
   0.654   0.011   0.347   0.2434  0.086   0.034                    0.234      0.340

       ---------------------------------------------------------------------------------------------------------------------
OUTPUT:This output will be interface with UI integration

       data_frame_excel :Dataframe

       TimeDate            From                    To                               Subject                    Body                        Thread_Id             label
2019-07-05 16:54:41     illakiyan@gmail.com       ajith@gmail.com                   Document...                 This document has....      16e9ebf3d0810850         0    
2019-07-23 15:59:44     lingesh@gmail.com         frank@gmail.com,ajith@gmail.com   Getting Some ....           Info of our Project...     16e9ebf3d0810834         1   
2019-07-06 06:45:06     ajith@gmail.com           illakiyan@gmail.com               Status of our project...    Things related....         16e9ebf3d0810851         2    
2019-07-17 03:20:00     frank@gmail.com           lingesh@gmail.com                 Re : Getting Some ....      Beyond your questions...   16e9ebf3d0810834         0   

       -------------------------------------------------------------------------------------------------------------------------

       no_of_clusters = 3

       -------------------------------------------------------------------------------------------------------------------------       
'''


from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import json
import flask
import warnings
from pandas.io.json import json_normalize
from sklearn.exceptions import ConvergenceWarning
from flask import request, jsonify
from flask_cors import CORS
import ast

#warning filter

warnings.simplefilter("always", ConvergenceWarning)

# server hosting in flask
app = flask.Flask(__name__)
app.config["DEBUG"] = True

#flask process to host
cors = CORS(app, resources={r"/kmeans": {"origins": "*"}})

@app.route('/kmeans', methods=['POST'])

def kmeansClustering():
    # getting information from the api call
    test_json = request.data
    message_info = ast.literal_eval(test_json.decode("utf-8"))
    
    #extracting information from the json format
    full_data_frame_for_replied_emails = pd.DataFrame.from_dict(json.loads(message_info['full_data_frame_for_replied_emails']), orient='columns')

    percentage_of_predictingElbowMethod = message_info['percentage_of_predictingElbowMethod']
    
    all_replied_gmailData = pd.DataFrame.from_dict(json.loads(message_info['all_replied_emails']), orient='columns')

    # finding number of clusters is suitable for the kmeans clustering
    def closestValueIndex(full_data_frame_of_email,percentage_of_predictingElbowMethod):
        elbow_method_list = []
        list_k = list(range(1, full_data_frame_of_email.shape[0]))
        for k in list_k:
            km = KMeans(n_clusters=k)
            km.fit(full_data_frame_of_email)
            elbow_method_list.append(km.inertia_)

        no_of_cluster = max(elbow_method_list) * percentage_of_predictingElbowMethod
        #finding nearest minimum to the sum of square distance and to determine the number of clusters
        predicted_no_of_cluster = elbow_method_list.index(elbow_method_list[min(range(len(elbow_method_list)), key = lambda i: abs(elbow_method_list[i]-no_of_cluster))])
        return predicted_no_of_cluster

    no_of_clusters = closestValueIndex(full_data_frame_for_replied_emails,percentage_of_predictingElbowMethod)

    # K-Means Parameters
    # kmeans

    clf = KMeans(n_clusters=no_of_clusters, n_jobs=-1, random_state=1)
    kmeans = clf.fit(full_data_frame_for_replied_emails)
    ymeans = kmeans.cluster_centers_

    # cluster labelling for the individual messages and add label in orginal message info
    result = clf.labels_
    all_replied_gmailData['label'] = result


    # sorting for clustered lables and resetting index
    all_replied_gmailData.sort_values("label",axis = 0,ascending = True,inplace = True,na_position = 'last')
    all_replied_gmailData = all_replied_gmailData.reset_index(drop = True)

    output_dict = {'all_replied_gmailData':(all_replied_gmailData).to_json(),'no_of_cluster':no_of_clusters}
        
    return json.dumps(str(output_dict))



app.run(port=9200,use_reloader=False)