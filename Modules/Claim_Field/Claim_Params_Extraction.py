# -*- coding: utf-8 -*-
"""
    Module: Project QB
    Claim_Params_Extraction 
    Extract all 'Claims params' from input text w.r.to excel sheet and 
    remove extracted params from text
"""


import pandas as pd
from Modules.For_All.Text_Preprocessing import text_clean


#------------------------------
# create 'TriggerWord List'
#------------------------------
df2 = pd.read_excel('other/Adhoc_QB_CH_Claims_Entities_31_10_2023.xlsx',sheet_name='Trigger_Words')
df2 = df2['TriggerWords']
trigger_words_list=[]
for word in df2:
    word= text_clean(word)
    trigger_words_list.append(word)


#-----------------------------------------------------
# Create 'Appointment_Params_Dict' with Preprocessing'
#-----------------------------------------------------
df_overall = pd.read_excel('other/Adhoc_QB_CH_Claims_Entities_31_10_2023.xlsx',sheet_name='Params_Sheet')
column_names= df_overall.columns                                    # Get all columns names

all_claim_params_dict={}                                      
for column in column_names:
    df_column=df_overall[column]                                    # get all data from specifice column
    df_column= df_column.dropna()                                   # remove N/A field

    column_entity_list=[]
    for entity in df_column:
        clean_entity= text_clean(entity)                            # clean code using module
        column_entity_list.append(clean_entity)                     # append in list
    all_claim_params_dict[column]= column_entity_list               # insert complete column list in dict 




#==========================================================
# Main Function:
#==========================================================
def claims_extraction(f_text):
    f_text= ' '+ f_text +' '
    field_status=False
        
    #-----------------------------------------
    # set 'field_status' True if 'Appointment' trigger word mentioned in query
    for trigger_word in trigger_words_list:                         
        trigger_word= ' '+trigger_word+' '
        if trigger_word in f_text:
            field_status=True 
      
    #-------------------------
    # Extract params from text
    claim_params_dict={}
    for field_name_key,param_field_list_value in all_claim_params_dict.items(): 
        if field_name_key in ['Risk Score','Radiology Visit','Readmission Count','ER Visit','Inpatient Spend','Hospital outpatient Spend',
                            'Pharmacy Spend','Professional outpatient Spend','SNF Spend','Home Health Spend','Hospice Spend','DME Spend','Total Spend']:
            if field_status == False:
                continue                                                      # skip current loop cycle
        
        extracted_param_list=[]
        param_field_list_value= sorted(param_field_list_value, key=len, reverse=True)
        for param in param_field_list_value:
            start_index = f_text.find(' '+str(param)+' ')
            if start_index != -1: 
                end_index = start_index + len(param)                          # index of the last occurrence of the string in the text
                param_name = f_text[start_index:end_index+1]                  # pick words using start & end index
                param_name=" ".join(param_name.split())                       # remove extra spaces in selected data
                extracted_param_list.append(param_name)                       # append extracted param in list using current key,value of length_dict
                f_text= f_text.replace(' '+param_name+' ',' ')                # remove extracted param from text
        if extracted_param_list:                                              # check: if list is not empty
            try:
                claim_params_dict[field_name_key].extend(extracted_param_list)
            except:
                claim_params_dict[field_name_key]= extracted_param_list
                
    return [claim_params_dict,f_text]


#==========================================================

'''
from Modules.For_All.Text_Preprocessing import text_clean

text='Show all patient with Total cost is 25000 and readmission count is 5'

clean_text= text_clean(text)
result= claims_extraction(clean_text)
print(result)
'''



