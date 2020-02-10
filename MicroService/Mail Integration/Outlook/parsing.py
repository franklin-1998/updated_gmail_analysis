# import pandas as pd
# import re
# import numpy as np
# from talon.signature.bruteforce import extract_signature
# from email_reply_parser import EmailReplyParser,EmailMessage


# data_frame = pd.read_pickle("kook2.pkl")
# # print(data_frame)

# for i in range(5):
#     string_body = data_frame['Full_Body'][i].replace('\n','2s3r')
#     list_body = string_body.split('3r')
#     list_body = (list(filter(None, list_body)))
#     replace_new_line = []
#     for j in range(len(list_body)):
#         if 'From:' not in list_body[j] and 'To:' not in list_body[j] and 'Sent:' not in list_body[j] and 'Subject:' not in list_body[j] and 'Date:' not in list_body[j] and '---------- Forwarded message ---------' not in list_body[j] and 'Cc:' not in list_body[j] and 'Bcc' not in list_body[j] :
#             replace_new_line.append(list_body[j])
#     parsed_body = replace_new_line
#     # print(EmailReplyParser.parse_reply('\n'.join(replace_new_line).replace('2s','\n')))
#     string_body = ' '.join(parsed_body).replace('2s','\n')
#     print(string_body)
#     # print(EmailReplyParser.parse_reply('\n'.join(replace_new_line)))
#     # print("\n\n\n\n\n")
#     # a = (EmailMessage.read(string_body))
#     # print(type(a))

       
    
#     print("\n\n\n\n\n WELCOME TO CLOOBOT TECHLABS\n\n\n\n\n")


# import numpy as np
# import pandas as pd


# data = pd.read_csv("tradeEmail_Filtered_new.csv")

# # print(data['Clear_Body'])

# f= open("email_body.txt","w+")
# for i in range(len(data)):
#     string = data['Clear_Body'][i].replace("\n"," ")
#     print(string)
#     f.write(string)

# f.close()






# import pandas as pd
# import numpy as np

# data = pd.read_csv("ner_dataset.csv", encoding="ISO-8859-1")
# data = data.fillna(method="ffill")

# print(data.tail(20))



















import spacy
from spacy import displacy
import nltk
# nltk.download("word_tokenize")
# nltk.download("pos_tag")
# nltk.download('maxent_ne_chunker')
# nltk.download('words')
# nltk.download('averaged_perceptron_tagger')
from nltk.tokenize import word_tokenize
from nltk.chunk import conlltags2tree, tree2conlltags
from pprint import pprint
from nltk.corpus import stopwords
import pandas as pd
from nltk.tag import pos_tag
from collections import Counter
import en_core_web_sm
nlp = spacy.load("en")

stop_words = set(stopwords.words('english')) 

# ex = 'European authorities fined Google a record $5.1 billion on Wednesday for abusing its power in the mobile phone market and ordered the company to alter its practices'

# def preprocess(sent):
#     sent = nltk.word_tokenize(sent)
#     sent = nltk.pos_tag(sent)
#     return sent


# sent = preprocess(ex)
# pattern = 'NP: {<DT>?<JJ>*<NN>}'
# cp = nltk.RegexpParser(pattern)
# cs = cp.parse(sent)
# # print(cs)
# # print(sent)


# iob_tagged = tree2conlltags(cs)
# # print(iob_tagged)

# ne_tree = nltk.ne_chunk(pos_tag(word_tokenize(ex)))
# # print(ne_tree)

# doc = nlp('European authorities fined Google a record $5.1 billion on Wednesday for abusing its power in the mobile phone market and ordered the company to alter its practices')
ner_dataframe = pd.DataFrame()

data = pd.read_csv("tradeEmail_Filtered_new.csv")

# print(data)
for i in range(len(data)-29):
    string = data['Clear_Body'][i].split("\n")
    string = (list(filter(None, string)))
    # word_tokens = word_tokenize(' '.join(string))
    # filtered_sentence = []
    # for w in word_tokens: 
    #     if w not in stop_words: 
    #         filtered_sentence.append(w) 
    # print(' '.join(filtered_sentence))
    data['Clear_Body'][i] = '\n'.join(string)


words_tokenize_list = []
position_list = []
entity_name_list = []

# # finding scores for individual values
# for tokenizing in range(len(data)-29):
#     doc = nlp(data['Clear_Body'][tokenizing])
#     for tagging in doc:
#         beams = nlp.entity.beam_parse([ doc ], beam_width = 16, beam_density = 0.0001)

#         entity_scores = defaultdict(float)
#         for beam in beams:
#             for score, ents in nlp.entity.moves.get_beam_parses(beam):
#                 for start, end, label in ents:
#                     entity_scores[(start, end, label)] += score
#     for key in entity_scores:
#         start, end, label = key
#         score = entity_scores[key]
#         if ( score > threshold):
#             # print ('Label: {}, Text: {}, Score: {}'.format(label, doc[start:end], score))    
#             words_tokenize_list.append(str(doc[start:end]))
#             # position_list.append(doc[start:end].en)
#             entity_name_list.append(label)
#             score_list.append(score)


for tokenizing in range(len(data)-29):
    doc = nlp(data['Clear_Body'][tokenizing])
    for tagging in doc:
        words_tokenize_list.append(str(tagging))
        position_list.append(tagging.ent_iob_)
        entity_name_list.append(tagging.ent_type_)


ner_dataframe['Words_Tokenize'] = words_tokenize_list
ner_dataframe['Position'] = position_list
ner_dataframe['Entity_Name'] = entity_name_list

ner_dataframe.to_csv('Entity_Named_DataSet.csv')

print(ner_dataframe)