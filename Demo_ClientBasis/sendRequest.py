import ast
import json
import pandas as pd
import numpy as np
import requests
import warnings
from datetime import datetime
from time import sleep

import warnings
import pandas as pd
warnings.simplefilter(action='ignore', category=FutureWarning)
pd.reset_option('all')

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn import decomposition, ensemble
from scipy import sparse
from scipy.sparse import csr_matrix
import pandas, xgboost, numpy, textblob, string
from keras.preprocessing import text, sequence
from keras import layers, models, optimizers
import dill as pickle
from traning_Model import training

# ignoring warning
warnings.filterwarnings('ignore')

def outlookIntegration():
    headers = {'content-type': 'application/json'}
    # print(message_input)
    successFlag = True
    count_trying = 0
    retryConnection = 10
    period = 10 #seconds
    while successFlag:
        try:
            #sending the data to the server
            resp = requests.post("http://127.0.0.1:8000/outlook_run",data = json.dumps("Sending Request"),headers=headers)
            successFlag = False
        except requests.exceptions.ConnectionError:
            print('----------Request Connection Error-----------')
            sleep(period)
            count_trying = count_trying + 1
            if(count_trying > retryConnection):
                print("-------------Some Problem In Server Communication -------------")
                break

    # getting response from the flask app
    message_value = ast.literal_eval(resp.json())
    train_data = pd.DataFrame.from_dict(json.loads(message_value['training']), orient='columns')
    test_data = pd.DataFrame.from_dict(json.loads(message_value['testing']), orient='columns')
    print(training(train_data,test_data))
    filename1 = 'Pretrained_classifier_model.pk'

    with open('./'+filename1 ,'rb') as f1:
        loaded_model = pickle.load(f1)
        
    filename2 = 'Tfidf_vect.pk'
    with open('./'+filename2 ,'rb') as f2:
        loaded_Tfidf = pickle.load(f2)

    xtest_tfidf =  loaded_Tfidf.transform(test_data['Body'].astype('U'))
    predictions = loaded_model.predict(xtest_tfidf)
    test_data['Label'] = predictions
    test_data.to_csv("Output.csv")
    print(predictions)
          
    
    
    return "Prediction Process is Completed"

# function call to send request to sign_in and to get all other informations

print(outlookIntegration())