# import spacy
# # Word tokenization
# from spacy.lang.en import English

# # importing the model en_core_web_sm of English for vocabluary, syntax & entities
# import en_core_web_sm
# import en_core_web_lg

# # for detecting punctuation
# import string  

# # # Load English tokenizer, tagger, parser, NER and word vectors
# # nlp = English()

# #importing stop words from English language.
# spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS



# text = """When Chennai data science, you shouldn't get discouraged!
# Challenges and setbacks aren't failures, they're just part of the 31/32/1999. You've got this!"""


# # load en_core_web_sm of English for vocabluary, syntax & entities
# # nlp = en_core_web_sm.load()
# nlp = spacy.load("en_core_web_lg")

# #  "nlp" Object is used to create documents with linguistic annotations.
# my_doc = nlp("India 21/03/2010")

# # Create list of word tokens
# token_list = []
# for ent in my_doc.ents:
#     print(ent.text, ent.start_char, ent.end_char, ent.label_)
# # for token in my_doc:
# #     if token.is_stop==False:
# #         print(token.pos_)
# #         if token.pos_ not in 'PUNCT' and '\n' not in token.text:
# #             token_list.append(token.text)
# # print(' '.join(token_list))















# import spacy
# import nltk
# # nltk.download("gutenberg")

# from nltk.corpus import gutenberg
# # from spacy import en
# nlp = spacy.load('en_core_web_sm')
# import random
# import pandas as pd
# import matplotlib.pyplot as plt
# # emma = gutenberg.raw('austen-emma.txt')
# data = pd.read_csv("tradeEmail_Filtered_new.csv")
# type_entity=[]
# sentences=[]
# entities=[]


# for sent in data['Clear_Body']:
#     parsed_sentence=nlp(sent)
#     for ent in parsed_sentence.ents:
#         if ent.text not in entities:
#             entities.append(ent.text)
#             sentences.append(sent)
#             type_entity.append(ent.label_)
# Entities=pd.DataFrame({'Sentence':sentences,'Entity':entities,'Entity_type':type_entity})
# print('The total number of entities detected were:{}'.format(len(Entities)))
# print(Entities)

# # print(data)
# # parsed_emma = nlp(emma)












# import spacy
# from spacy import displacy
# import en_core_web_lg
# from IPython.display import display, HTML



# # nlp = spacy.load('en_core_web_lg')
# # sample_text = "Mark Zuckerberg took two days to testify before members of Congress last week, and he apologised for privacy breaches on Facebook. He said that the social media website did not take a broad enough view of its responsibility, which was a big mistake. He continued to take responsibility for Facebook, saying that he started it, runs it, and he is responsible for what happens at the company. Illinois Senator Dick Durbin asked Zuckerberg whether he would be comfortable sharing the name of the hotel where he stayed the previous night, or the names of the people who he messaged that week. The CEO was startled by the question, and he took about 7 seconds to respond with no."
# # doc = nlp(sample_text)

# # a = displacy.render(doc, style='ent', jupyter=True)

# # display(HTML(displacy.render(doc, style='ent', jupyter=True)))

# # sp = spacy.load('en_core_web_sm')

# # sen = sp('Good afternoon, In the context of DSM tender 01/02/2020,31/01/2021 we would like to extend the existing   allocation to Durban, for a regular volume of approx. 1 tank/month.The successful operator rate we offered on  previous version of the tender is 700 usd with 7 days free at POD > 35 $ Can you pls check if you can match or give me your best price with a  commitment for the whole tender validity and volume? MSDS of the cargo in attachment.Pls let me have your feed-back by the 13/01.')
# nlp = spacy.load("en_core_web_sm")

# sen = nlp('''Good afternoon,

 

# In the context of DSM tender 01/02/2020 
# 31/01/2021 we would like to extend the existing   allocation to Durban, for a regular volume of approx. 1 tank/month.

 

# The successful operator rate we offered on  previous version of the tender is 700 usd with 7 days free at POD > 35 $

 

# Can you pls check if you can match or give me your best price with a  commitment for the whole tender validity and volume?

 

# MSDS of the cargo in attachment.

 

# Pls let me have your feed-back by the 13/01.

 

# Thanks
# ''')
# # print(list(sen.sents))
# # sentence = sen

# # for sentence in sentence.ents:
# #     print (sentence.text)
# # print(list(sen.sents))

# for entity in sen.ents:
#     print(entity.text + ' - ' + entity.label_ + ' - ' + str(spacy.explain(entity.label_)))


# python -m spacy download en only administrator cmd will work

# import spacy 

# text = "But Google is starting from behind. The company made a late push\ninto hardware, and Apple’s Siri, available on iPhones, and Amazon’s Alexa\nsoftware, which runs on its Echo and Dot devices, have clear leads in\nconsumer adoption."

# nlp = spacy.load("en") 

# doc = nlp(text) 

# for ent in doc.ents:
#     print(ent.text, ent.start_char, ent.end_char, ent.label_)

























import spacy
import sys
from collections import defaultdict

nlp = spacy.load('en')
text =''' Dear Suresh,

Good day,

 

Please advise your best rate for Iso Tank from BND or BIK to NSA

Product description: Linear Alkyl Benzene

Quantity: 2200 MT

MSDS as per attached. 

 

Looking forward your kind reply,
'''


# with nlp.disable_pipes('ner'):
doc = nlp(text)

threshold = 0.2
beams = nlp.entity.beam_parse([ doc ], beam_width = 16, beam_density = 0.0001)

entity_scores = defaultdict(float)
for beam in beams:
    for score, ents in nlp.entity.moves.get_beam_parses(beam):
        for start, end, label in ents:
            entity_scores[(start, end, label)] += score

print(entity_scores)
print ('Entities and scores (detected with beam search)')
for key in entity_scores:
    start, end, label = key
    score = entity_scores[key]
    if ( score > threshold):
        print ('Label: {}, Text: {}, Score: {}'.format(label, doc[start:end], score))