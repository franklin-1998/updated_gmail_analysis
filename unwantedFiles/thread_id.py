import pandas as pd
import datetime
# Function to get First sender

def call_ConversationFirstSender(all_mailData):
    #unique thread_id
    unique_thread_id = all_mailData['Thread_Id'].unique()
    
    data_frame_FirstSender = pd.DataFrame({})

    # loop to sort time date and fetch first conversation

    for loop_1 in range(len(unique_thread_id)):
        individual_thread_id_mailData = all_mailData.loc[all_mailData['Thread_Id'] == unique_thread_id[loop_1]]
        
        # sorting the time to fetch first stimuli 

        individual_thread_id_mailData = (individual_thread_id_mailData.sort_values(by='TimeDate',ascending=True)).reset_index(drop=True)
        data_frame_FirstSender = data_frame_FirstSender.append(individual_thread_id_mailData.iloc[0])
    
    data_frame_FirstSender = data_frame_FirstSender.reset_index(drop=True)

    #list of keywords that marked as issue

    related_keywordsIssue = ['updation pending','error','issue','issues','problem','check','pending','not update','not','not done','not posting','mismatch','reminder','wrongly','wrong','missing','discrepancy','discrepancies','unable']
    
    # print(data_frame_FirstSender['Subject'].str.lower())
    # print(type(related_keywordsIssue[0]))
    body_Issue = list(data_frame_FirstSender['Body'].str.lower().apply(lambda x: any([k in str(x) for k in related_keywordsIssue])))
    subject_Issue = list(data_frame_FirstSender['Subject'].str.lower().apply(lambda x: any([k in str(x) for k in related_keywordsIssue])))
    concat_SubjectBody = [subject_Issue,body_Issue]

    # initially storing -1 in the label column
    data_frame_FirstSender['Label'] = -999	


    # looping for label the data which is issue or not
    for issue_key in range(len(concat_SubjectBody)):
        for labelling in range(len(concat_SubjectBody[issue_key])):
            if concat_SubjectBody[issue_key][labelling]:
                if data_frame_FirstSender['Label'][labelling] not in [0,1]:
                    data_frame_FirstSender['Label'][labelling] = 1
            else:
                if data_frame_FirstSender['Label'][labelling] not in [0,1]:
                    data_frame_FirstSender['Label'][labelling] = 0
        print('===================')

    data_frame_FirstSender.to_csv("1.csv")
    return True




data_frame = call_ConversationFirstSender(pd.read_csv(r"C:\Users\Dev\Documents\GitHub\updated_gmail_analysis\MicroService\Mail Integration\Outlook\fahad.csv"))
print(data_frame)

# data_frame['TimeDate'] = [datetime.datetime.strptime(x,"%Y-%m-%d %H:%M:%S") for x in data_frame['TimeDate']]

# #unique thread_id
# unique_thread_id = data_frame['Thread_Id'].unique()

# data_frame_FirstSender = pd.DataFrame({})

# # loop to sort time date and fetch first conversation

# for loop_1 in range(len(unique_thread_id)):
#     individual_thread_id_mailData = data_frame.loc[data_frame['Thread_Id'] == unique_thread_id[loop_1]]
    
#     # print(individual_thread_id_mailData)
#     # sorting the time to fetch first stimuli 

#     individual_thread_id_mailData = (individual_thread_id_mailData.sort_values(by='TimeDate',ascending=True)).reset_index(drop=True)
#     data_frame_FirstSender = data_frame_FirstSender.append(individual_thread_id_mailData.iloc[0])

# data_frame_FirstSender = data_frame_FirstSender.reset_index(drop=True)
# data_frame_FirstSender.to_csv("filter_unique.csv")

# print(data_frame_FirstSender)