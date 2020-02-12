import warnings
import pandas as pd
warnings.simplefilter(action='ignore', category=FutureWarning)
pd.reset_option('all')
from sklearn import model_selection, preprocessing, linear_model, naive_bayes, metrics, svm
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn import decomposition, ensemble
from scipy.sparse import hstack
from scipy import sparse
from scipy.sparse import csr_matrix
import pandas, xgboost, numpy, textblob, string
from keras.preprocessing import text, sequence
from keras import layers, models, optimizers
import warnings
import dill as pickle
warnings.simplefilter(action='ignore', category=FutureWarning)
frank_copy = pandas.DataFrame()
# load the dataset


excel_data_df = pandas.read_csv('old_trade_email.csv',header=0,encoding = 'unicode_escape')
excel_data_df['Label']=excel_data_df['Label'].astype(int)
excel_data_df['Subject'] = excel_data_df['Subject'].astype('U')
excel_data_df['Clear_Body'] = excel_data_df['Clear_Body'].astype('U')
print(excel_data_df)










# data = open('Dataset/corpus',encoding="utf8").read()
# labels, texts = [], []
# for i, line in enumerate(data.split("\n")):
#     content = line.split()
#     labels.append(content[0])
#     texts.append(" ".join(content[1:]))

# create a dataframe using texts and lables
trainDF = pandas.DataFrame()
trainDF['text'] = excel_data_df['Clear_Body'].astype('U') + excel_data_df['Subject'].astype('U')
trainDF['label'] = excel_data_df['Label'].astype(int)
trainDF['text'] = list(trainDF['text'])
# split the dataset into training and validation datasets 
train_x , train_y = trainDF['text'], list(trainDF['label'])
# label encode the target variable 

# encoder = preprocessing.LabelEncoder()
# train_y = encoder.fit_transform(train_y)
# print("test label for for line in test data : ",valid_y[0:1])
# valid_y = encoder.fit_transform(valid_y)


# # create a count vectorizer object 
# count_vect = CountVectorizer(analyzer='word', token_pattern=r'\w{1,}')
# count_vect.fit(trainDF['text'].astype('U'))

# # transform the training and validation data using count vectorizer object
# xtrain_count =  count_vect.transform(train_x.astype('U'))

# xvalid_count =  count_vect.transform(valid_x.astype('U'))
# print("************\n\n first line from train text {0}\n\n**********************".format(xvalid_count[0,:]))
# # word level tf-idf
# tfidf_vect = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}', max_features=5000)
# tfidf_vect.fit(trainDF['text'].astype('U'))
# xtrain_tfidf =  tfidf_vect.transform(train_x.astype('U'))
# # xvalid_tfidf =  tfidf_vect.transform(valid_x.astype('U'))
# # print("************\n\n shape of tfidf {0}\n\n**********************".format(xtrain_tfidf.shape))
# params_len = (xtrain_tfidf.shape)[1]
# params_hi = (xtrain_tfidf.shape)[0]
# print("############ params :  ",params_len)
# # ngram level tf-idf 
# tfidf_vect_ngram = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}', ngram_range=(2,3), max_features=params_len)
# tfidf_vect_ngram.fit(trainDF['text'].astype('U'))
# xtrain_tfidf_ngram =  tfidf_vect_ngram.transform(train_x.astype('U'))
# xvalid_tfidf_ngram =  tfidf_vect_ngram.transform(valid_x.astype('U'))


# # characters level tf-idf
# tfidf_vect_ngram_chars = TfidfVectorizer(analyzer='char', token_pattern=r'\w{1,}', ngram_range=(2,3), max_features=params_len)
# tfidf_vect_ngram_chars.fit(trainDF['text'].astype('U'))
# xtrain_tfidf_ngram_chars =  tfidf_vect_ngram_chars.transform(train_x.astype('U')) 
# xvalid_tfidf_ngram_chars =  tfidf_vect_ngram_chars.transform(valid_x.astype('U')) 

# new_train = xtrain_tfidf 
# new_valid = xvalid_tfidf 


# # print("\n\n ********** NEW {0}\n *************\n\n".format(new[0,:]))
# # print("\n\n ********** nrml_tfidf {0}\n *************\n\n".format(xtrain_tfidf[0,:]))
# # print("\n\n ********** ngram {0}\n *************\n\n".format(xtrain_tfidf_ngram[0,:]))
# # print(xtrain_count)
# # # print(xvalid_count)

# # # load the pre-trained word-embedding vectors 
# # embeddings_index = {}
# # for i, line in enumerate(open('Dataset/wiki-news-300d-1M.vec',encoding="utf8")):
# #     values = line.split()
# #     embeddings_index[values[0]] = numpy.asarray(values[1:], dtype='float32')

# # # create a tokenizer 
# # token = text.Tokenizer()
# # token.fit_on_texts(trainDF['text'].astype('U'))
# # word_index = token.word_index

# # # print(word_index)

# # # convert text to sequence of tokens and pad them to ensure equal length vectors 
# # train_seq_x = sequence.pad_sequences(token.texts_to_sequences(train_x), maxlen=70)
# # valid_seq_x = sequence.pad_sequences(token.texts_to_sequences(valid_x), maxlen=70)

# # # create token-embedding mapping
# # embedding_matrix = numpy.zeros((len(word_index) + 1, 300))
# # for word, i in word_index.items():
# #     embedding_vector = embeddings_index.get(word)
# #     if embedding_vector is not None:
# #         embedding_matrix[i] = embedding_vector

# trainDF['word_count'] = trainDF['text'].apply(lambda x: len(x.split())).astype(int)
# trainDF['title_word_count'] = trainDF['text'].apply(lambda x: len([wrd for wrd in x.split() if wrd.istitle()])).astype(int)




# pos_family = {
#     'noun' : ['NN','NNS','NNP','NNPS'],
#     'pron' : ['PRP','PRP$','WP','WP$'],
#     'verb' : ['VB','VBD','VBG','VBN','VBP','VBZ'],
#     'adj' :  ['JJ','JJR','JJS'],
#     'adv' : ['RB','RBR','RBS','WRB']
# }

# # function to check and get the part of speech tag count of a words in a given sentence
# def check_pos_tag(x, flag):
#     cnt = 0
#     try:
#         wiki = textblob.TextBlob(x)
#         for tup in wiki.tags:
#             ppo = list(tup)[1]
#             if ppo in pos_family[flag]:
#                 cnt += 1
#     except:
#         pass
    
#     return cnt

# trainDF['noun_count'] = trainDF['text'].apply(lambda x: check_pos_tag(x, 'noun')).astype(int)
# trainDF['verb_count'] = trainDF['text'].apply(lambda x: check_pos_tag(x, 'verb')).astype(int)
# trainDF['adj_count'] = trainDF['text'].apply(lambda x: check_pos_tag(x, 'adj')).astype(int)
# trainDF['adv_count'] = trainDF['text'].apply(lambda x: check_pos_tag(x, 'adv')).astype(int)
# trainDF['pron_count'] = trainDF['text'].apply(lambda x: check_pos_tag(x, 'pron')).astype(int)

# frank_copy['noun_count'] = trainDF['noun_count']
# frank_copy['verb_count'] = trainDF['verb_count']
# frank_copy['adj_count'] =  trainDF['adj_count']
# frank_copy['adv_count']  =  trainDF['adv_count']
# frank_copy['pron_count']  =  trainDF['pron_count']
# frank_copy['word_count']  =  trainDF['word_count']
# frank_copy['title_word_count']  =  trainDF['title_word_count']

# # # frank_copy = frank_copy.as_matrix().astype(int)
# frank_copy = csr_matrix(frank_copy)
# print(frank_copy.shape)
# filename1 = 'franky.pk'

# with open('./'+filename1 ,'wb') as f1:
#     pickle.dump(frank_copy, f1)
# # print("\n**************** start  frank DF   ****************")
# # print(trainDF)
# # print("\n**************** END  frank DF   ****************")

# # print("\n**************** start  frank array   ****************")
# # print(trainDF.to_xarray)
# # print("\n**************** END  frank array   ****************")

# # # train a LDA Model
# # lda_model = decomposition.LatentDirichletAllocation(n_components=20, learning_method='online', max_iter=20)
# # X_topics = lda_model.fit_transform(xtrain_count)
# # topic_word = lda_model.components_ 
# # vocab = count_vect.get_feature_names()

# # # view the topic models
# # n_top_words = 10
# # topic_summaries = []
# # for i, topic_dist in enumerate(topic_word):
# #     topic_words = numpy.array(vocab)[numpy.argsort(topic_dist)][:-(n_top_words+1):-1]
# #     topic_summaries.append(' '.join(topic_words))


# # # print(topic_summaries)
# epochs = 20
filename2 = 'franky.pk'
with open('./'+filename2 ,'rb') as f1:
    frank_copy = pickle.load(f1)
print(frank_copy.shape)
print(train_y)
model = ensemble.RandomForestClassifier().fit(frank_copy,train_y)
# def train_model(classifier, feature_vector_train, label, feature_vector_valid, is_neural_net=False):
#     # fit the training dataset on the classifier
#     classifier.fit(feature_vector_train, label)
    
#     # predict the labels on validation dataset
#     predictions = classifier.predict(feature_vector_valid)
#     if is_neural_net:
#         predictions = predictions.argmax(axis=-1)
#     print("********* testing single input from testing Data  and its label**** \n {0} \t\t {1}\n**************************************".format(valid_x[0:1,],valid_y[0:1,]))
#     # print(classifier.summary())
#     print("\n**************** new labeled output   ****************")
#     print(classifier.predict(feature_vector_valid[-1:,]))
#     print("\n****************    ****************")
    
    
#     return metrics.accuracy_score(predictions, valid_y)

# # # RF on Count Vectors
# # accuracy = train_model(ensemble.RandomForestClassifier(), xtrain_count, train_y, xvalid_count)
# # print("RF, Count Vectors: ", accuracy)

# # RF on Word Level TF IDF Vectors
# accuracy = train_model(ensemble.RandomForestClassifier(bootstrap=True, 
#             class_weight=None, criterion='gini',
#             max_depth=None, max_features='auto', max_leaf_nodes=None,
#             min_impurity_decrease=0.0, min_impurity_split=None,
#             min_samples_leaf=1, min_samples_split=2,
#             min_weight_fraction_leaf=0.0, n_estimators=150, n_jobs=1,
#             oob_score=True, random_state=None, verbose=0,
#             warm_start=False)
#             , merged_data_train, train_y, merged_data_valid )
# print("RF, WordLevel TF-IDF: ", accuracy)

# # # RF on Word Level TF IDF Vectors
# # accuracy = train_model(ensemble.RandomForestClassifier(), xtrain_tfidf_ngram, train_y, xvalid_tfidf_ngram)
# # print("RF, WordLevel NGRAMS TF-IDF: ", accuracy)

# # # RF on Word Level TF IDF Vectors
# # accuracy = train_model(ensemble.RandomForestClassifier(), xtrain_tfidf_ngram_chars, train_y, xvalid_tfidf_ngram_chars)
# # print("RF, WordLevel CHAR LVL TF-IDF: ", accuracy)


# # # RF on Word Level TF IDF Vectors
# # accuracy = train_model(ensemble.RandomForestClassifier(), new_train, train_y, new_valid)
# # print("RF, OUR OWN LVL TF-IDF: ", accuracy)

# # def create_model_architecture(input_size):
# #     # create input layer 
# #     input_layer = layers.Input((input_size, ), sparse=True)
    
# #     # create hidden layer
# #     hidden_layer = layers.Dense(100, activation="relu")(input_layer)
    
# #     # create output layer
# #     output_layer = layers.Dense(1, activation="sigmoid")(hidden_layer)

# #     classifier = models.Model(inputs = input_layer, outputs = output_layer)
# #     classifier.compile(optimizer=optimizers.Adam(), loss='binary_crossentropy')
# #     return classifier 

# # classifier = create_model_architecture(xtrain_tfidf_ngram.shape[1])
# # accuracy = train_model(classifier, xtrain_tfidf_ngram, train_y, xvalid_tfidf_ngram, is_neural_net=True)
# # print("NN, Ngram Level TF IDF Vectors",  accuracy)

# # def create_cnn():
# #     # Add an Input Layer
# #     input_layer = layers.Input((70, ))

# #     # Add the word embedding Layer
# #     embedding_layer = layers.Embedding(len(word_index) + 1, 300, weights=[embedding_matrix], trainable=True)(input_layer)
# #     embedding_layer = layers.SpatialDropout1D(0.3)(embedding_layer)

# #     # Add the convolutional Layer
# #     conv_layer = layers.Convolution1D(100, 3, activation="relu")(embedding_layer)

# #     # Add the pooling Layer
# #     pooling_layer = layers.GlobalMaxPool1D()(conv_layer)

# #     # Add the output Layers
# #     output_layer1 = layers.Dense(50, activation="relu")(pooling_layer)
# #     output_layer1 = layers.Dropout(0.25)(output_layer1)
# #     output_layer2 = layers.Dense(1, activation="sigmoid")(output_layer1)

# #     # Compile the model
# #     model = models.Model(inputs=input_layer, outputs=output_layer2)
# #     model.compile(optimizer=optimizers.Adam(), loss='binary_crossentropy')
    
# #     return model

# # classifier = create_cnn()
# # accuracy = train_model(classifier, train_seq_x, train_y, valid_seq_x, is_neural_net=True)
# # print("CNN, Word Embeddings",  accuracy)



filename3 = 'Pretrained_classifier_model2.pk'

with open('./'+filename3 ,'wb') as f2:
    pickle.dump(model, f2)





# print("### picled prediction ####",loaded_model.predict(xtrain_tfidf))