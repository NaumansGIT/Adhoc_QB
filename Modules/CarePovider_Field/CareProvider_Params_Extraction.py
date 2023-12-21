# -*- coding: utf-8 -*-
"""
    Module: Project QB
    Claim_Params_Extraction 
    Extract all 'Claims params' from input text w.r.to excel sheet and 
    remove extracted params from text
"""

import re
import pandas as pd
from Modules.For_All.Text_Preprocessing import text_clean


#------------------------------
# create 'TriggerWord List'
#------------------------------
df2 = pd.read_excel('other/Adhoc_QB_CH_Care_Provider_Entities_31_10_2023.xlsx',sheet_name='Trigger_Words')
df2 = df2['TriggerWords']
trigger_words_list=[]
for word in df2:
    word= text_clean(word)
    if word not in trigger_words_list:
        trigger_words_list.append(word)



#-----------------------------------------------------
# Create 'CareAppointment_Params_Dict' with Preprocessing'
#-----------------------------------------------------
df_overall = pd.read_excel('other/Adhoc_QB_CH_Care_Provider_Entities_31_10_2023.xlsx',sheet_name='Params_Sheet')
column_names= df_overall.columns                                            # Get all columns names

all_cp_params_dict={}                                      
for column in column_names:
    df_column=df_overall[column]                                            # get all data from specifice column
    df_column= df_column.dropna()                                           # remove N/A field

    column_entity_list=[]
    for entity in df_column:
        clean_entity= text_clean(entity)                                     # clean code using module
        column_entity_list.append(clean_entity)                              # append in list
    column_entity_list= sorted(column_entity_list, key=len, reverse=True)
    all_cp_params_dict[column]= column_entity_list                           # insert complete column list in dict 




#==========================================================
# Main Function: 'Params Extraction'
#==========================================================
def careprovider_extraction(f_text):
    f_text= ' '+ f_text +' '
    field_status=False
        
    #--------------------------------------------------
    # set 'field_status' True if 'Appointment' trigger word mentioned in query
    #--------------------------------------------------
    for trigger_word in trigger_words_list:                         
        trigger_word= ' '+trigger_word+' '
        if trigger_word in f_text:
            field_status=True 
     
    #--------------------------------------------------
    # Extract params from text using excel_sheet_dict
    #--------------------------------------------------
    careprovider_params_dict={}                                                # 'final dict' to save result
    for field_name_key,param_field_list_value in all_cp_params_dict.items():
        if field_name_key in ['Startdate','Enddate','First Name','Last Name','NPI','Role','Specialty',
                              'Status','Zipcode','State','City']:
            if field_status == False:
                continue                                                   # skip current loop cycle

        extracted_param_list=[]
        for param in param_field_list_value:
            start_index = f_text.find(' '+str(param)+' ')                  # find the index of param in text
            if start_index != -1: 
                end_index = start_index + len(param)                       # index of the last occurrence of the string in the text
                param_name = f_text[start_index:end_index+1]               # pick words using start & end index
                param_name=" ".join(param_name.split())                    # remove extra spaces in selected data
                extracted_param_list.append(param_name)                    # append extracted param in list using current key,value of length_dict
                f_text= f_text.replace(' '+param+' ',' ')
        if extracted_param_list:                                           # check: if list is not empty
            try:
                careprovider_params_dict[field_name_key].extend(extracted_param_list)
            except:
                careprovider_params_dict[field_name_key]= extracted_param_list


    #--------------------------------------------------
    # Extract 'Email' from text using 're_pattern'
    #--------------------------------------------------
    email_pattern= r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email_matches = re.findall(email_pattern, f_text)
    if email_matches:
        try:
            careprovider_params_dict['Email'].extend(email_matches)
        except:
            careprovider_params_dict['Email']= email_matches
                
 
    '''
    #--------------------------------------------------
    # Extract 'Phone#' from text using 're_pattern' (cases cover=['(123) 456-7890',
    # '123-456-7890','123.456.7890','1234567890','+1 (123) 456-7890']
    #--------------------------------------------------
    
    # Define the regex pattern for USA phone numbers
    pattern = re.compile(r'''
       # (?:(?:\+1\s?)?   # Optional +1 country code
       # (?:\(\d{3}\)|\d{3})  # Area code in parentheses or without
       # [\s\.-]?)  # Separator (whitespace, dot, or hyphen)
       # \d{3}        # First three digits
       # [\s\.-]?     # Separator
       # \d{4}        # Last four digits
    ''', re.VERBOSE)
    phone_matches = pattern.findall(f_text)
    if phone_matches:
        try:
            careprovider_params_dict['Phone'].extend(phone_matches)
        except:
            careprovider_params_dict['Phone']= phone_matches
    '''        
                   
    return [careprovider_params_dict,f_text]


#==========================================================
#==========================================================
'''
#text="Arkansas Alexandria and abjl care provider start at 2020"
text= "Show me all the data where the care manager's last name is JOhn, "
clean_text= text_clean(text)
result= careprovider_extraction(clean_text)
print('\n',result[0])
print('\n',result[1])
'''


