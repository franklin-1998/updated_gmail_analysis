'''
MicroService : Doc2Vec converter

convertDoc2vec : This function implements that the documentation of words converted to vector formats and trained using wikipedia pages words.

Conditions : Python 3.7.4

Libraries : requirements.txt

Server Information : This will be hosted in flask server()

Instructions :
                1.required columns are any text columns are accepted to convert texts to vectors.
                2.this will be used for all email concepts such as outlook,gmail,yahoo etc... and text related concepts.

INPUT:This input has taken from the gmail API using messages()
        Dataframe Columns of 'From','To','Subject','Body' are the input of doc2vec converter

   1.      From             |   2.  To                               |    3.   Subject               | 4.    Body                     
     illakiyan@gmail.com    |       ajith@gmail.com                  |      Document...              |   This document has....              
     lingesh@gmail.com      |       frank@gmail.com,ajith@gmail.com  |      Getting Some ....        |   Info of our Project...             
     ajith@gmail.com        |       illakiyan@gmail.com              |      Status of our project... |   Things related....                   
     frank@gmail.com        |       lingesh@gmail.com                |      Re : Getting Some ....   |   Beyond your questions...         
       ---------------------------------------------------------------------------------------------------------------------- 

        model_path : './microservice/enwiki_dow/doc2vec.bin'

       ----------------------------------------------------------------------------------------------------------------------

    pca_value :   This input has taken from the doc2vec output(format : dataframe)
    
      0       1       2       3       4       5       ........        299        300 
    0.32    0.023   0.07    0.09    0.087   0.056                    0.003      0.034
    0.34    0.045   0.07    0.43    0.032   0.0534                   0.012      0.65
    0.67    0.076   0.45    0.34    0.087   0.0435                   0.312      0.04
    0.098   0.098   0.67    0.43    0.056   0.034                    0.324      0.34
      .       .       .       .       .       .                        .          .
      .       .       .       .       .       .                        .          .
      .       .       .       .       .       .                        .          .
    0.345   0.012   0.97    0.2445  0.545   0.022                    0.234      0.324
    0.654   0.011   0.347   0.2434  0.086   0.034                    0.234      0.340
    ------------------------------------------------------------------------------------------------------------------------------------------

OUTPUT:

    Future Process : Output will be fitted for KMeans Clustering
        
    message_data_frame : DataFrame 

            0       1       2       3       4       5       ........        299        300 
        0.32    0.023   0.07    0.09    0.087   0.056                    0.003      0.034
        0.34    0.045   0.07    0.43    0.032   0.0534                   0.012      0.65
        0.67    0.076   0.45    0.34    0.087   0.0435                   0.312      0.04
        0.098   0.098   0.67    0.43    0.056   0.034                    0.324      0.34
            .       .       .       .       .       .                        .          .
            .       .       .       .       .       .                        .          .
            .       .       .       .       .       .                        .          .
        0.345   0.012   0.97    0.2445  0.545   0.022                    0.234      0.324
        0.654   0.011   0.347   0.2434  0.086   0.034                    0.234      0.340
            -------------------------------------------------------------------------------------------------------------------------

    pca_value : DataFrame 

            0       1       2       3       4       5    
        0.32    0.023   0.07    0.09    0.087   0.056  
        0.34    0.045   0.07    0.43    0.032   0.0534         
        0.67    0.076   0.45    0.34    0.087   0.0435    
        0.098   0.098   0.67    0.43    0.056   0.034                
            .       .       .       .       .       .                       
            .       .       .       .       .       .                        
            .       .       .       .       .       .                       
        0.345   0.012   0.97    0.2445  0.545   0.022                    
        0.654   0.011   0.347   0.2434  0.086   0.034 
            -------------------------------------------------------------------------------------------------------------------------

'''

from gensim.models.doc2vec import Doc2Vec
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
import flask
import urllib.request
from rake_nltk import Rake
import json
import requests
import ast
from flask import request, jsonify
from flask_cors import CORS

# server hosting in flask
app = flask.Flask(__name__)
app.config["DEBUG"] = True

#flask process to host and allow cors
cors = CORS(app, resources={r"/doc2vec": {"origins": "*"}})

@app.route('/doc2vec', methods=['POST'])

# funcion to convert the document of texts to vectors
def convertDoc2Vec():
    
    #getting information from the api call
    test_json = request.data
    # print(test_json.decode("utf-8"))
    message_info = ast.literal_eval(test_json.decode("utf-8"))
    
    #extracting information from the url
    model_path = message_info['model_path']
    message_value = message_info['message_value']
    # print(message_value)
    
    #load model from saved file
    model = Doc2Vec.load(model_path)
    
    # function for converting the document of texts to vector format

    def apply_trained_doc2vec(message_value):
        message_list = []
        for vec in message_value:
            message_list.append(list(model.infer_vector([vec])))
        return message_list
    
    output = apply_trained_doc2vec(message_value)
    output_dict = {'message_convert' : output}
    return json.dumps(str(output_dict))


'''
INPUT:This input has taken from the doc2vec output
    
    0       1       2       3       4       5       ........        299        300 
   0.32    0.023   0.07    0.09    0.087   0.056                    0.003      0.034
   0.34    0.045   0.07    0.43    0.032   0.0534                   0.012      0.65
   0.67    0.076   0.45    0.34    0.087   0.0435                   0.312      0.04
   0.098   0.098   0.67    0.43    0.056   0.034                    0.324      0.34
    .       .       .       .       .       .                        .          .
    .       .       .       .       .       .                        .          .
    .       .       .       .       .       .                        .          .
   0.345   0.012   0.97    0.2445  0.545   0.022                    0.234      0.324
   0.654   0.011   0.347   0.2434  0.086   0.034                    0.234      0.340
------------------------------------------------------------------------------------------------------------------------------------------
'''
#flask process to host and allow cors
cors = CORS(app, resources={r"/PCA": {"origins": "*"}})

@app.route('/PCA', methods=['POST'])

def compressingUsingPCA():

    #getting information from the api call
    test_json = request.data
    # print(test_json)
    message_info = ast.literal_eval(test_json.decode("utf-8"))
    # print(message_info)
    
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



'''
INPUT:This input has taken from the gmail API using messages()
        Dataframe Columns of 'Subject','Body' are the input of keywords extracter

        1.   Subject             | 2.    Body                     
        Document...              |   This document has....              
        Getting Some ....        |   Info of our Project...             
        Status of our project... |   Things related....                   
        Re : Getting Some ....   |   Beyond your questions...         
       ---------------------------------------------------------------------------------------------------------------------- 

'''

#flask process to host and allow cors
cors = CORS(app, resources={r"/keywords": {"origins": "*"}})

@app.route('/keywords', methods=['POST'])

def keywordsExtracter():
    #getting information from the api call
    test_json = request.data

    message_info = ast.literal_eval(test_json.decode("utf-8"))
    
    #extracting information from the url
    message_value = message_info['subject_body_list']

    #initializing rake for object
    r = Rake()
    extract=r.extract_keywords_from_text(message_value)
    rank=r.get_ranked_phrases()
    rank_with_scores=r.get_ranked_phrases_with_scores()
    
    #initialize dict for converting list of couple to dict format
    dict_rank_keywords = {}

    for iterate in range(len(rank_with_scores)):
        dict_rank_keywords[rank_with_scores[iterate][1]] = rank_with_scores[iterate][0]

    keywords_list = sorted(dict_rank_keywords, key=dict_rank_keywords.get, reverse=True)[:3]

    output_dict = {'keywords_output' : keywords_list}
    return json.dumps(str(output_dict))

# running app to host for request and resposne

app.run(port=8200,use_reloader=False)