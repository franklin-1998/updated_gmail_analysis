import ast
import json
import pandas as pd
import numpy as np
import requests
import warnings
from datetime import datetime
from time import sleep

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
            resp = requests.post("http://127.0.0.1:8000/outlook_run",data = json.dumps(str(datetime.now())),headers=headers)
            successFlag = False
        except requests.exceptions.ConnectionError:
            print('----------Request Connection Error-----------')
            sleep(period)
            count_trying = count_trying + 1
            if(count_trying > retryConnection):
                print("-------------Some Problem In Server Communication -------------")
                break
    message_value = ast.literal_eval(resp.json())
       
    data_frame = pd.DataFrame.from_dict(json.loads(message_value['data_frame']), orient='columns')

    return "Close this Terminal and Watch demo_outlook.py Terminal"

# function call to send request to sign_in and to get all other informations

print(outlookIntegration())