# converting to data type format of string
import ast
# the following four lines is to ignore the future warnings that arises by tensor flow
import warnings
import pandas as pd
warnings.simplefilter(action='ignore', category=FutureWarning)
pd.reset_option('all')

# this pakage is to make pipe line 
from sklearn.pipeline import Pipeline

# these pakages used to extract features from text
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer

# this is to store the created model for future use
import dill as pickle
import requests
#this imports thr random forrest classifer
from sklearn.ensemble import RandomForestClassifier

#this is used to find the best parameters of the each features
from sklearn.model_selection import GridSearchCV

#and this is for accuracy detection
from sklearn import  metrics

import requests

#load the data to train initially from data set
excel_data_df = pd.read_csv('new_created.csv',header=0,encoding = 'unicode_escape')

#remove NA values which are not use for the learning
excel_data_df.dropna()

#this is to randomize the order of rows in readed data inorder to avoid biased learning
excel_data_df = excel_data_df.sample(frac=1).reset_index(drop=True)

# the following steps are used to typecast the each colomn to datatype as per our considerings
excel_data_df['Label']=excel_data_df['Label'].astype(int)
excel_data_df['Clear_Body'] = excel_data_df['Clear_Body'].astype('U')
excel_data_df['Subject'] = excel_data_df['Subject'].astype('U')






# create a dataframe using texts and lables
trainDF = pd.DataFrame()
trainDF['text'] = excel_data_df['Subject'] + excel_data_df['Clear_Body']
trainDF['label'] = excel_data_df['Label']

#this steps are for our understanding snd list typecast for proper insertion of data into pipeline without type cast error will arises
train_data = list(trainDF['text'])
train_label = list(trainDF['label'])


# these steps are used to send data to microservice and get the preducted values and accuracy
predicted = requests.post("http://127.0.0.1:8000/ml_test",json = {'mail': train_data,'label':train_label,'operation':"test_only"})
output = ast.literal_eval(predicted.json())
print(output['predicted'],"\n ACCURACY  :  ",output['accuracy'])
excel_data_df['tested_lab']=output['predicted']
excel_data_df.to_csv("new.csv")



# #it is used to make the model updation
# update = requests.post("http://127.0.0.1:8000/ml_test",json = {'mail': train_data,'label':train_label,'operation':"update"})
# print(update.json())