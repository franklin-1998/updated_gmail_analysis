import warnings
import pandas as pd
warnings.simplefilter(action='ignore', category=FutureWarning)
pd.reset_option('all')

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


excel_data_df = pandas.read_csv('tradeEmail.csv',header=0,encoding = 'unicode_escape')
excel_data_df['Label']=excel_data_df['Label'].astype(int)
excel_data_df['Body'] = excel_data_df['Body'].astype('U')
print(excel_data_df)






# create a dataframe using texts and lables
trainDF = pandas.DataFrame()
trainDF['text'] = excel_data_df['Body']
trainDF['label'] = excel_data_df['Label']

# split the dataset into training and validation datasets 
train_x, valid_x, train_y, valid_y = model_selection.train_test_split(trainDF['text'], trainDF['label'],test_size=0.01)

# label encode the target variable 


# create a count vectorizer object 
count_vect = CountVectorizer(analyzer='word', token_pattern=r'\w{1,}')
count_vect.fit(trainDF['text'].astype('U'))

# transform the training and validation data using count vectorizer object
xtrain_count =  count_vect.transform(train_x.astype('U'))

xvalid_count =  count_vect.transform(valid_x.astype('U'))
print("************\n\n first line from train text {0}\n\n**********************".format(xvalid_count[0,:]))
# word level tf-idf
tfidf_vect = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}', max_features=5000)
tfidf_vect.fit(trainDF['text'].astype('U'))
xtrain_tfidf =  tfidf_vect.transform(train_x.astype('U'))
xvalid_tfidf =  tfidf_vect.transform(valid_x.astype('U'))
print("************\n\n shape of tfidf {0}\n\n**********************".format(xtrain_tfidf.shape))
params_len = (xtrain_tfidf.shape)[1]
params_hi = (xtrain_tfidf.shape)[0]

# ngram level tf-idf 
tfidf_vect_ngram = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}', ngram_range=(2,3), max_features=5000)
tfidf_vect_ngram.fit(trainDF['text'].astype('U'))
xtrain_tfidf_ngram =  tfidf_vect_ngram.transform(train_x.astype('U'))
xvalid_tfidf_ngram =  tfidf_vect_ngram.transform(valid_x.astype('U'))


# characters level tf-idf
tfidf_vect_ngram_chars = TfidfVectorizer(analyzer='char', token_pattern=r'\w{1,}', ngram_range=(2,3), max_features=5000)
tfidf_vect_ngram_chars.fit(trainDF['text'].astype('U'))
xtrain_tfidf_ngram_chars =  tfidf_vect_ngram_chars.transform(train_x.astype('U')) 
xvalid_tfidf_ngram_chars =  tfidf_vect_ngram_chars.transform(valid_x.astype('U')) 

new_train = xtrain_tfidf 
new_valid = xvalid_tfidf 


epochs = 20

def train_model(classifier, feature_vector_train, label, feature_vector_valid, is_neural_net=False):
    # fit the training dataset on the classifier
    classifier.fit(feature_vector_train, label)
    
    # predict the labels on validation dataset
    predictions = classifier.predict(feature_vector_valid)
    if is_neural_net:
        predictions = predictions.argmax(axis=-1)
    print("********* testing single input from testing Data  and its label**** \n {0} \t\t {1}\n**************************************".format(valid_x[0:1,],valid_y[0:1,]))
    
    print("\n**************** new labeled output   ****************")
    print(classifier.predict(feature_vector_valid))
    print("\n****************    ****************")
    
    print("Accuracy : ",metrics.accuracy_score(predictions, valid_y))
    return classifier

# # RF on Count Vectors
# accuracy = train_model(ensemble.RandomForestClassifier(), xtrain_count, train_y, xvalid_count)
# print("RF, Count Vectors: ", accuracy)

# # RF on Word Level TF IDF Vectors
# model = train_model(ensemble.RandomForestClassifier(bootstrap=True, 
#             class_weight=None, criterion='gini',
#             max_depth=None, max_features='sqrt', max_leaf_nodes=None,
#             min_impurity_decrease=0.0, min_impurity_split=None,
#             min_samples_leaf=1, min_samples_split=2,
#             min_weight_fraction_leaf=0.0, n_estimators=100, n_jobs=1,
#             oob_score=False, random_state=None, verbose=0,
#             warm_start=False)
#             , xtrain_tfidf, train_y, xvalid_tfidf )

# model training using svm
model = train_model(svm.SVC(C=1.0, kernel='rbf', degree=3, gamma='scale',
                 coef0=0.0, shrinking=True, probability=False,
                 tol=1e-3, cache_size=200, class_weight=None,
                 verbose=False, max_iter=-1, decision_function_shape='ovr',
                 random_state=None)
            , xtrain_tfidf, train_y, xvalid_tfidf )

# print("RF, WordLevel TF-IDF: ", accuracy)
filename1 = 'Pretrained_classifier_model.pk'
filename2 = 'Tfidf_vect.pk'
with open('./'+filename1, 'wb') as file1:
        pickle.dump(model, file1)
with open('./'+filename2, 'wb') as file2:
        pickle.dump(tfidf_vect, file2)

with open('./'+filename1 ,'rb') as f1:
    loaded_model = pickle.load(f1)
with open('./'+filename2 ,'rb') as f2:
    loaded_tfidf = pickle.load(f2)

print("### picled prediction ####",loaded_model.predict(xvalid_tfidf))
print("labeled goint to test",valid_y)
