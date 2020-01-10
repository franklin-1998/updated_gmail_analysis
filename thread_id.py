import pandas as pd
import datetime

data_frame = pd.read_csv("second.csv",encoding='unicode escape')

data_frame['TimeDate'] = [datetime.datetime.strptime(x,"%Y-%m-%d %H:%M:%S") for x in data_frame['TimeDate']]

#unique thread_id
unique_thread_id = data_frame['Thread_Id'].unique()

data_frame_FirstSender = pd.DataFrame({})

# loop to sort time date and fetch first conversation

for loop_1 in range(len(unique_thread_id)):
    individual_thread_id_mailData = data_frame.loc[data_frame['Thread_Id'] == unique_thread_id[loop_1]]
    
    # print(individual_thread_id_mailData)
    # sorting the time to fetch first stimuli 

    individual_thread_id_mailData = (individual_thread_id_mailData.sort_values(by='TimeDate',ascending=True)).reset_index(drop=True)
    data_frame_FirstSender = data_frame_FirstSender.append(individual_thread_id_mailData.iloc[0])

data_frame_FirstSender = data_frame_FirstSender.reset_index(drop=True)
data_frame_FirstSender.to_csv("filter_unique.csv")

print(data_frame_FirstSender)