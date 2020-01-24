import extract_msg
import pandas as pd
import os
import re
from dateutil import parser as date_parser
# import talon
# from talon import signature

# #initialize talon methods
# talon.init()


os.chdir("C:/Users/Dev/Documents/GitHub/updated_gmail_analysis/Trade_Email") # directory object to be passed to the function for accessing emails, this is where you will store all .msg files

direct = os.getcwd()# directory object to be passed to the function for accessing emails, this is where you will store all .msg files

ext = '.msg' #type of files in the folder to be read
df = pd.DataFrame({})

def DataImporter(directory, extension):
    global df
    my_list = []
    for i in os.listdir(direct):
        try:
            if i.endswith(ext):
                msg = extract_msg.Message(i)
                sendFrom = ','.join(re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",msg.sender))
                sendTo = ','.join(re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",msg.to))

                sendDate = date_parser.parse(msg.date,fuzzy=True).replace(tzinfo=None)
                print(sendDate)
                # text, signatures = signature.extract(msg.body,sender=each_mes['from']['emailAddress']['address'])
                # text1, signatures1 = signature.extract(text,sender=each_mes['from']['emailAddress']['address'])
                # text2, signatures2 = signature.extract(signatures,sender=each_mes['from']['emailAddress']['address'])
                sendBody = (msg.body).encode("ascii", "ignore").decode("utf-8")
                print(sendBody)
                my_list.append([sendDate,sendFrom,sendTo, msg.subject,sendBody]) #These are in-built features of '**extract_msg.Message**' class
                df = pd.DataFrame(my_list, columns = ['TimeDate','From','To','Subject','Body'])
        except (UnicodeEncodeError,AttributeError,TypeError):
            print("Not Possible")
            pass

DataImporter(direct,ext)
df.to_csv("tradeEmail2.csv")