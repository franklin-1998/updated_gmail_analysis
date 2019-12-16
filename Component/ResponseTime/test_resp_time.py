from response_time import responseTimeCalculating,avgResponseTime
import pandas as pd

data_frame_check = pd.DataFrame({'TimeDate':['05-08-2019  21:08:08','05-08-2019  21:10:08','05-08-2019  21:12:08','05-08-2019  21:14:00'],
                                 'From':['mail.ajithsubash@gmail.com,mail@gmail.com','frankjos1998@gmail.com','tejas@gmail.com','vinod@gmail.com'],
                                 'To':['frankjos1998@gmail.com','mail.ajithsubash@gmail.com','ajithsubash1999@gmail.com,vinod@gmail.com','tejas@gmail.com'],
                                 'Subject':['Final Ouput for Stimulus and Response','Re : Final Ouput for Stimulus and Response','Status Update','Re : Status Update'],
                                 'Body':['1.Final Ouput for Stimulus and Response completed 2.All the rows stored in db Mailtrack Sender notified by Mailtrack','1.Final Ouput for Stimulus and Response completed','Send me the details of our project and current update','Here is the update see it in the document'],
                                 'Thread_Id':['16e9ebf3d0810850','16e9ebf3d0810850','16e9ebf3d0810851','16e9ebf3d0810851'],
                                 'label':[0,0,1,1]})

data_frame_check['TimeDate']= pd.to_datetime(data_frame_check['TimeDate']) 
output_dict = {'16e9ebf3d0810850': 2.0, '16e9ebf3d0810851': 1.87}

def test_responseTime():
    # print(responseTimeCalculating(data_frame_check))
    assert responseTimeCalculating(data_frame_check) == output_dict

# check_responseTime()