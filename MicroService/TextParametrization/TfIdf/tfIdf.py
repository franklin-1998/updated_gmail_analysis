'''
MicroService : Tf-Idf converter

convertWordToNumerical : This function implements that the words or any texts to numerical formats.

Conditions : Python 3.7.4

Libraries : requirements.txt

Server Information : This will be hosted in flask server()

Instructions :
                1.required columns are any text columns are accepted to convert texts to numbers.
                2.this will be used for all email concepts such as outlook,gmail,yahoo etc... and text related concepts.

INPUT:
        Dataframe Columns of 'From','To','Subject','Body' are the input of doc2vec converter

   1.      From             |   2.  To                               |    3.   Subject               | 4.    Body                     
     illakiyan@gmail.com    |       ajith@gmail.com                  |      Document...              |   This document has....              
     lingesh@gmail.com      |       frank@gmail.com,ajith@gmail.com  |      Getting Some ....        |   Info of our Project...             
     ajith@gmail.com        |       illakiyan@gmail.com              |      Status of our project... |   Things related....                   
     frank@gmail.com        |       lingesh@gmail.com                |      Re : Getting Some ....   |   Beyond your questions...         
       ---------------------------------------------------------------------------------------------------------------------- 
OUTPUT : 

      conv_data_frame : DataFrame

                  0         1         2         3
          0    0.773158 -0.426660  0.766498 -0.231932
          1   -0.067376  0.004136 -0.002534 -0.001246
          2   -0.067376  0.004136 -0.002534 -0.001246
          3   -0.067376  0.004136 -0.002534 -0.001246
          4   -0.067376  0.004136 -0.002534 -0.001246
      -----------------------------------------------------------------------------------------------------------------------------

      pca_output : DataFrame

                  0         1         2 
          0   0.773158  -0.42660   0.73649
          1   0.07376   0.004136  -0.00253
          2   0.06776   0.004136  -0.0025
          3   0.0376    0.002346  -0.534 
          4   0.34376   0.007136  -0.2534 

    -----------------------------------------------------------------------------------------------------------------------------


'''

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import numpy as np
import flask
import urllib.request
import json
import requests
import ast
from flask import request, jsonify
from flask_cors import CORS

# server hosting in flask
app = flask.Flask(__name__)
app.config["DEBUG"] = True

#flask process to host and allow cors
cors = CORS(app, resources={r"/tf_idf": {"origins": "*"}})


'''
INPUT:
        Dataframe Columns of 'From','To','Subject','Body' are the input of doc2vec converter

   1.      From             |   2.  To                               |    3.   Subject               | 4.    Body                     
     illakiyan@gmail.com    |       ajith@gmail.com                  |      Document...              |   This document has....              
     lingesh@gmail.com      |       frank@gmail.com,ajith@gmail.com  |      Getting Some ....        |   Info of our Project...             
     ajith@gmail.com        |       illakiyan@gmail.com              |      Status of our project... |   Things related....                   
     frank@gmail.com        |       lingesh@gmail.com                |      Re : Getting Some ....   |   Beyond your questions...         
       ---------------------------------------------------------------------------------------------------------------------- 
'''
@app.route('/tf_idf', methods=['POST'])
def convertWordToNumerical(message_info):

    #getting information from the api call
    test_json = request.data
    # print(test_json.decode("utf-8"))
    message_info = ast.literal_eval(test_json.decode("utf-8"))
    
    #extracting information from the url
    message_value = message_info['message_value']

    #removing stopwords in the given list
    remove_stopwords = TfidfVectorizer(stop_words='english',lowercase=True)

    # input data is fitting to tf-idf method 
    fitting_to_words = remove_stopwords.fit_transform(message_value)

    #converting to dataframe
    conv_data_frame = pd.DataFrame(fitting_to_words.todense())

    output_dict = {'message_convert' : (conv_data_frame).to_json()}
    return json.dumps(str(output_dict))

'''
INPUT : this input has derive from the tf-idf method output
      conv_data_frame : DataFrame

                  0         1         2         3
          0    0.773158 -0.426660  0.766498 -0.231932
          1   -0.067376  0.004136 -0.002534 -0.001246
          2   -0.067376  0.004136 -0.002534 -0.001246
          3   -0.067376  0.004136 -0.002534 -0.001246
          4   -0.067376  0.004136 -0.002534 -0.001246
      -----------------------------------------------------------------------------------------------------------------------------
'''

#flask process to host and allow cors
cors = CORS(app, resources={r"/doc2vec": {"origins": "*"}})

@app.route('/tf_idf_pca', methods=['POST'])
def compressing_After_TfIdf_UsingPCA(message_value):
   #getting information from the api call
    test_json = request.data
    message_info = ast.literal_eval(test_json.decode("utf-8"))
    
    #extracting information from the url
    message_value = pd.DataFrame.from_dict(json.loads(message_info['message_value']), orient='columns')

    scaler = MinMaxScaler(feature_range=[0, 1])
    data_rescaled = scaler.fit_transform(message_value)

    # predicting components with 95% variance
    pca = PCA(0.95).fit(data_rescaled)
    components = pca.n_components_ 
    pca_value = PCA(n_components=components).fit_transform(message_value)
    
    output_dict = {'pca_output' : (pd.concat([pd.DataFrame(pca_value)],axis=1)).to_json()}

    return json.dumps(str(output_dict))
