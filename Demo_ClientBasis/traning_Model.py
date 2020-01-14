import warnings
import pandas as pd
warnings.simplefilter(action='ignore', category=FutureWarning)
pd.reset_option('all')
import numpy as np
from sklearn import model_selection, preprocessing, linear_model, naive_bayes, metrics, svm
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn import decomposition, ensemble
from scipy import sparse
from scipy.sparse import csr_matrix
import pandas, xgboost, numpy, textblob, string
from keras.preprocessing import text, sequence
from keras import layers, models, optimizers
from flask import Flask, jsonify, request
import dill as pickle
# frank_copy = pandas.DataFrame()
# load the dataset

def training(train_df,test_df):
    # split the dataset into training and validation datasets 


    train_x = train_df['Body'].astype('U')
    train_y = train_df['Label']

    valid_x = test_df['Body'].astype('U')
    
    
    whole_data_tfidf = pd.DataFrame() 
    whole_data_tfidf['Body'] = train_x + valid_x
    # word level tf-idf
    tfidf_vect = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}', max_features=5000)
    tfidf_vect.fit(whole_data_tfidf['Body'].astype('U'))
    xtrain_tfidf =  tfidf_vect.transform(train_x.astype('U'))
    
    print("************\n\n shape of tfidf {0}\n\n**********************".format(xtrain_tfidf.shape))
    

    def train_model(classifier, feature_vector_train, label, is_neural_net=False):
        # fit the training dataset on the classifier
        classifier.fit(feature_vector_train, label)
        return classifier


    # RF on Word Level TF IDF Vectors
    model = train_model(ensemble.RandomForestClassifier(bootstrap=True, 
                class_weight=None, criterion='gini',
                max_depth=None, max_features='sqrt', max_leaf_nodes=None,
                min_impurity_decrease=0.0, min_impurity_split=None,
                min_samples_leaf=1, min_samples_split=2,
                min_weight_fraction_leaf=0.0, n_estimators=200, n_jobs=1,
                oob_score=False, random_state=None, verbose=0,
                warm_start=False)
                , xtrain_tfidf, train_y )

    # print("RF, WordLevel TF-IDF: ", accuracy)
    filename1 = 'Pretrained_classifier_model.pk'
    filename2 = 'Tfidf_vect.pk'
    data_frame = 'alldata_df'

    with open('./'+filename1, 'wb') as file1:
            pickle.dump(model, file1)

    with open('./'+filename2, 'wb') as file2:
            pickle.dump(tfidf_vect, file2)

   
    return "Model trained and ready to test"
