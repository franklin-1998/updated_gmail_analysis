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
from sklearn import metrics


import flask
from flask import request, jsonify
from flask_cors import CORS
# server hosting in flask
app = flask.Flask(__name__)
app.config["DEBUG"] = True



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

#the following 8 lines is for additional features but we didnt used.it may be used in future
# import nltk
# from nltk.stem.snowball import SnowballStemmer
# stemmer = SnowballStemmer("english", ignore_stopwords=True)
# class StemmedCountVectorizer(CountVectorizer):
#     def build_analyzer(self):
#         analyzer = super(StemmedCountVectorizer, self).build_analyzer()
#         return lambda doc: ([stemmer.stem(w) for w in analyzer(doc)])
# stemmed_count_vect = StemmedCountVectorizer(analyzer='word', token_pattern=r'\w{1,}',stop_words='english',ngram_range = (1,2))

#construct a pipeline for our feature extraction and ml model fitting flow
text_clf2 = Pipeline([('vect', CountVectorizer(analyzer='char', token_pattern=r'\w{1,}',stop_words='english',ngram_range = (1,2))),
# text_clf2 = Pipeline([ ('vect_stemming', stemmed_count_vect),
                     ('tfidf',  TfidfTransformer(use_idf= False)),
                     ('clf-rm', RandomForestClassifier(bootstrap=True, 
                                class_weight=None, criterion='gini',
                                max_depth=None, max_features='auto', max_leaf_nodes=None,
                                min_impurity_decrease=0.0, min_impurity_split=None,
                                min_samples_leaf=1, min_samples_split=2,
                                min_weight_fraction_leaf=0.0, n_estimators=150, n_jobs=1,
                                oob_score=False, random_state=None, verbose=0,
                                warm_start=False))])

#this fit the datas initally (very initial trainning)
text_clf2 = text_clf2.fit(train_data,train_label)

#the following lines are used to find best parametric values for high accuracy
# parameters_rm = {'vect__ngram_range': [(1, 1), (1, 2)],
#  'tfidf__use_idf': (True, False),
# 'clf-rm__bootstrap': [True, False],
#  'clf-rm__max_depth': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, None],
#  'clf-rm__max_features': ['auto', 'sqrt'],
#  'clf-rm__min_samples_leaf': [1, 2, 4],
#  'clf-rm__min_samples_split': [2, 5, 10],
#  'clf-rm__n_estimators': [200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000]}
# gs_clf_svm = GridSearchCV(text_clf2, parameters_rm, n_jobs=-1)
# gs_clf_svm = gs_clf_svm.fit(train_data, train_label)
# print(gs_clf_svm.best_score_)
# print(gs_clf_svm.best_params_)



# following store the created pipeline as pickle file
filename1 = 'Pretrained_classifier_model.pk'
with open('./'+filename1, 'wb') as file1:
	pickle.dump(text_clf2, file1)

#flask process to host
cors = CORS(app, resources={r"/ml_test": {"origins": "*"}})

@app.route('/ml_test', methods=['GET','POST'])

def test():
    #this condition applies when the request is to test the sended data and return the respose
    if(request.method == 'POST' and request.get_json(force=True)['operation']=="test_only"):
        filename1 = 'Pretrained_classifier_model.pk'
        with open('./'+filename1 ,'rb') as f1:
            loaded_model = pickle.load(f1)
        data = request.get_json(force=True)
        prediction = list(loaded_model.predict(data['mail']))
        acc = metrics.accuracy_score(prediction,data['label'])
        output = {'predicted':prediction,'accuracy' : acc}
        return jsonify(str(output))
    #this condition allied if the request is to fit the model for updation
    elif(request.method == 'POST' and request.get_json(force=True)['operation']=="update"):
        filename1 = 'Pretrained_classifier_model.pk'
        with open('./'+filename1 ,'rb') as f1:
            loaded_model = pickle.load(f1)
        data = request.get_json(force=True)
        loaded_model = loaded_model.fit(data['mail'],data['label'])
        with open('./'+filename1, 'wb') as file1:
            pickle.dump(loaded_model, file1)
        return jsonify("Ml_Model updated successfully")
        
        
     
app.run(port=8000,use_reloader=False)
