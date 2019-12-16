from detect_similar_emails import detectingSimilarEmails
import pandas as pd

model_path = 'enwiki_dbow/doc2vec.bin'

data_frame_check = pd.DataFrame({'TimeDate':['05-08-2019  21:08:08','05-08-2019  21:10:08','05-08-2019  21:12:08','05-08-2019  21:14:00','05-08-2019  21:04:00','06-09-2019  13:14:00','07-09-2019  21:14:56','08-09-2019  01:54:00','05-10-2019  21:14:00','06-10-2019  15:14:00','15-10-2019  02:14:00','25-10-2019  11:25:59','07-09-2019  21:14:56','08-09-2019  01:54:00','05-10-2019  21:14:00','06-10-2019  15:14:00','15-10-2019  02:14:00','25-10-2019  11:25:59'],
                                 'From':['mail.ajithsubash@gmail.com,mail@gmail.com','frankjos1998@gmail.com','tejas@gmail.com','vinod@gmail.com','mail.ajithsubash@gmail.com','tejas@gmail.com','mail.ajithsubash@gmail.com','tejas@gmail.com','mail.ajithsubash@gmail.com','tejas@gmail.com','vinod@gmail.com','vinod@gmail.com','mail.ajithsubash@gmail.com','tejas@gmail.com','mail.ajithsubash@gmail.com','tejas@gmail.com','vinod@gmail.com','vinod@gmail.com'],
                                 'To':['frankjos1998@gmail.com','mail.ajithsubash@gmail.com','ajithsubash1999@gmail.com,vinod@gmail.com','tejas@gmail.com','frankjos1998@gmail.com','ajithsubash1999@gmail.com,vinod@gmail.com','vinod@gmail.com','vinod@gmail.com','ajithsubash1999@gmail.com','ajithsubash1999@gmail.com','ajithsubash1999@gmail.com','ajithsubash1999@gmail.com','vinod@gmail.com','vinod@gmail.com','ajithsubash1999@gmail.com','ajithsubash1999@gmail.com','ajithsubash1999@gmail.com','ajithsubash1999@gmail.com'],
                                 'Subject':['Final Ouput for Stimulus and Response','Re : Final Ouput for Stimulus and Response','Status Update','Re : Status Update','Final Ouput for Stimulus and Response','Re : Final Ouput for Stimulus and Response','Status Update','Re : Status Update','Final Ouput for Stimulus and Response','Re : Final Ouput for Stimulus and Response','Status Update','Re : Status Update','Status Update','Re : Status Update','Final Ouput for Stimulus and Response','Re : Final Ouput for Stimulus and Response','Status Update','Re : Status Update'],
                                 'Body':['1.Final Ouput for Stimulus and Response completed 2.All the rows stored in db Mailtrack Sender notified by Mailtrack','1.Final Ouput for Stimulus and Response completed','Send me the details of our project and current update','Here is the update see it in the document','1.Final Ouput for Stimulus and Response completed 2.All the rows stored in db Mailtrack Sender notified by Mailtrack','1.Final Ouput for Stimulus and Response completed','Send me the details of our project and current update','Here is the update see it in the document','1.Final Ouput for Stimulus and Response completed 2.All the rows stored in db Mailtrack Sender notified by Mailtrack','1.Final Ouput for Stimulus and Response completed','Send me the details of our project and current update','Here is the update see it in the document','Send me the details of our project and current update','Here is the update see it in the document','1.Final Ouput for Stimulus and Response completed 2.All the rows stored in db Mailtrack Sender notified by Mailtrack','1.Final Ouput for Stimulus and Response completed','Send me the details of our project and current update','Here is the update see it in the document'],
                                 'Thread_Id':['16e9ebf3d0810850','16e9ebf3d0810850','16e9ebf3d0810851','16e9ebf3d0810851','16e9ebf3d0810850','16e9ebf3d0810850','16e9ebf3d0810851','16e9ebf3d0810851','16e9ebf3d0810850','16e9ebf3d0810850','16e9ebf3d0810851','16e9ebf3d0810851','16e9ebf3d0810851','16e9ebf3d0810851','16e9ebf3d0810850','16e9ebf3d0810850','16e9ebf3d0810851','16e9ebf3d0810851']})
                                

data_frame_check['TimeDate']= pd.to_datetime(data_frame_check['TimeDate'])

index_for_gmailData_inputData = 16

output_data_frame = detectingSimilarEmails(data_frame_check,index_for_gmailData_inputData,model_path)

output_list = list(output_data_frame['Similar Emails'])

predicted_list = ['Very Closest','Closest','Far']

flag = True

for check in output_list:
    if check not in predicted_list:
        flag = False

def test_detect_similar_emails():
    assert flag == True




