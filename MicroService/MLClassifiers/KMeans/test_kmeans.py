from kmeans import kmeansClustering
import pandas as pd
from pandas.testing import assert_frame_equal


data_frame_check = pd.DataFrame({'TimeDate':['05-08-2019  21:08:08','05-08-2019  21:10:08','05-08-2019  21:12:08','05-08-2019  21:14:00'],
                                 'From':['mail.ajithsubash@gmail.com,mail@gmail.com','frankjos1998@gmail.com','mail@gmail.com','frankjos1998@gmail.com'],
                                 'To':['frankjos1998@gmail.com','mail.ajithsubash@gmail.com','frankjos1998@gmail.com','mail@gmail.com'],
                                 'Subject':['Final Ouput for Stimulus and Response','Re : Final Ouput for Stimulus and Response','Status Update','Re : Status Update'],
                                 'Body':['1.Final Ouput for Stimulus and Response completed 2.All the rows stored in db Mailtrack Sender notified by Mailtrack','1.Final Ouput for Stimulus and Response completed','Send me the details of our project and current update','Here is the update see it in the document'],
                                 'Thread_Id':['16e9ebf3d0810850','16e9ebf3d0810850','16e9ebf3d0810851','16e9ebf3d0810851']})
                                

data_frame_check['TimeDate']= pd.to_datetime(data_frame_check['TimeDate'])

percentage_of_predictingElbowMethod = 0.05

full_data_frame_of_email = pd.DataFrame({'0':[-0.0014,-0.00235,0.0147,0.0235],
                                         '1':[-0.00124,-0.00235,0.0140,0.0235],
                                         '2':[0.0321,0.0355,0.1410,0.323],
                                         '3':[0.2441,0.235,-0.141,0.362],
                                         '4':[-0.0244,-0.0235,-0.014,0.012],
                                         '5':[0.234,0.235,-0.014,-0.0121],
                                         '6':[0.00224,0.00235,0.014,-0.021],
                                         '7':[0.5456,0.5465,-0.00654,-0.0125]})

output_data_frame_predicted = pd.DataFrame({'TimeDate':['05-08-2019  21:08:08','05-08-2019  21:10:08','05-08-2019  21:12:08','05-08-2019  21:14:00'],
                                 'From':['mail.ajithsubash@gmail.com,mail@gmail.com','frankjos1998@gmail.com','mail@gmail.com','frankjos1998@gmail.com'],
                                 'To':['frankjos1998@gmail.com','mail.ajithsubash@gmail.com','frankjos1998@gmail.com','mail@gmail.com'],
                                 'Subject':['Final Ouput for Stimulus and Response','Re : Final Ouput for Stimulus and Response','Status Update','Re : Status Update'],
                                 'Body':['1.Final Ouput for Stimulus and Response completed 2.All the rows stored in db Mailtrack Sender notified by Mailtrack','1.Final Ouput for Stimulus and Response completed','Send me the details of our project and current update','Here is the update see it in the document'],
                                 'Thread_Id':['16e9ebf3d0810850','16e9ebf3d0810850','16e9ebf3d0810851','16e9ebf3d0810851'],
                                 'label':[0,0,1,1]})
output_data_frame_predicted['TimeDate']= pd.to_datetime(output_data_frame_predicted['TimeDate'])
                                
output_from_clustering,no_of_clusters = kmeansClustering(full_data_frame_of_email,percentage_of_predictingElbowMethod,data_frame_check)

def test_kmeansclustering():
    assert_frame_equal(output_data_frame_predicted, output_from_clustering, check_dtype=False)

