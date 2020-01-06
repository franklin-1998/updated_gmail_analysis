from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import json
import flask
import matplotlib.pyplot as plt
import warnings
from pandas.io.json import json_normalize
from sklearn.exceptions import ConvergenceWarning
from flask import request, jsonify
from flask_cors import CORS
import ast

#warnings filter
warnings.simplefilter("always", ConvergenceWarning)



def kmeansClustering(all_replied_gmailData,full_data_frame_for_replied_emails,percentage_of_predictingElbowMethod):

    # finding number of clusters is suitable for the kmeans clustering
    def closestValueIndex(full_data_frame_of_email,percentage_of_predictingElbowMethod):
        elbow_method_list = []
        list_k = list(range(1, full_data_frame_of_email.shape[0]))
        for k in list_k:
            with warnings.catch_warnings(record=True):
                warnings.simplefilter("ignore")
                km = KMeans(n_clusters=k,precompute_distances='auto',init='kmeans++')
                km = km.fit(full_data_frame_of_email)
                elbow_method_list.append(km.inertia_)
        plt.plot(list_k,elbow_method_list,'bx-')
        plt.show()  

        no_of_cluster = max(elbow_method_list) * percentage_of_predictingElbowMethod
        #finding nearest minimum to the sum of square distance and to determine the number of clusters
        predicted_no_of_cluster = elbow_method_list.index(elbow_method_list[min(range(len(elbow_method_list)), key = lambda i: abs(elbow_method_list[i]-no_of_cluster))])
        return predicted_no_of_cluster

    print("Finding No Of Clusters")
    # no_of_clusters = closestValueIndex(full_data_frame_for_replied_emails,percentage_of_predictingElbowMethod)

    # print(no_of_clusters)

    
    # K-Means Parameters
    # kmeans

    clf = KMeans(n_clusters=20, n_jobs=-1,max_iter=50000, random_state=1)
    kmeans = clf.fit(full_data_frame_for_replied_emails)
    ymeans = kmeans.cluster_centers_

    # cluster labelling for the individual messages and add label in orginal message info
    result = clf.labels_
    all_replied_gmailData['label'] = result


    # sorting for clustered lables and resetting index
    all_replied_gmailData.sort_values("label",axis = 0,ascending = True,inplace = True,na_position = 'last')
    all_replied_gmailData = all_replied_gmailData.reset_index(drop = True)

    print(all_replied_gmailData)




all_replied_gmailData = pd.read_csv("all_gmailData.csv")
full_data_frame_for_replied_emails = pd.read_csv("doc2vec.csv")
percentage_of_predictingElbowMethod = 0.05

kmeansClustering(all_replied_gmailData,full_data_frame_for_replied_emails,percentage_of_predictingElbowMethod)