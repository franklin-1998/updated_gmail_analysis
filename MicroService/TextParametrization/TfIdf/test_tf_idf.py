from tfIdf import convertWordToNumerical
import pandas as pd

model_path = 'enwiki_dbow/doc2vec.bin'


data_frame_check = pd.DataFrame({'TimeDate':['05-08-2019  21:08:08','05-08-2019  21:10:08','05-08-2019  21:12:08','05-08-2019  21:14:00'],
                                 'From':['mail.ajithsubash@gmail.com,mail@gmail.com','frankjos1998@gmail.com','tejas@gmail.com','vinod@gmail.com'],
                                 'To':['frankjos1998@gmail.com','mail.ajithsubash@gmail.com','ajithsubash1999@gmail.com,vinod@gmail.com','tejas@gmail.com'],
                                 'Subject':['Final Ouput for Stimulus and Response','Re : Final Ouput for Stimulus and Response','Status Update','Re : Status Update'],
                                 'Body':['1.Final Ouput for Stimulus and Response completed 2.All the rows stored in db Mailtrack Sender notified by Mailtrack','1.Final Ouput for Stimulus and Response completed','Send me the details of our project and current update','Here is the update see it in the document'],
                                 'Thread_Id':['16e9ebf3d0810850','16e9ebf3d0810850','16e9ebf3d0810851','16e9ebf3d0810851'],
                                 'label':[0,0,1,1]})
                                

data_frame_check['TimeDate']= pd.to_datetime(data_frame_check['TimeDate'])

from_value_check = pd.DataFrame(convertWordToNumerical(data_frame_check['From']))
to_value_check = pd.DataFrame(convertWordToNumerical(data_frame_check['To']))
subject_value_check = pd.DataFrame(convertWordToNumerical(data_frame_check['Subject']))
body_value_check = pd.DataFrame(convertWordToNumerical(data_frame_check['Body']))

output_data_frame = (pd.concat([from_value_check,to_value_check,subject_value_check,body_value_check],axis=1)).reset_index(drop=True)

column_length = output_data_frame.shape[1]
output_data_frame.columns = range(output_data_frame.shape[1])
column_list = []

for check_between in range(column_length):
    column_list.append(''.join([str(i) for i in list(set(output_data_frame[check_between].between(-1,1)))]))

output_value = list(set(column_list))

# print(output_value)


# # print(''.join(output_value))

def test_doc2vec():
    assert ''.join(output_value) == str(True)