# -*- coding: utf-8 -*-
"""
    Module: Project QB
    Appointment_Params_Extraction 
    Extract all 'Appointment params' from input text w.r.to excel sheet
"""


import pandas as pd
from Modules.For_All.Text_Preprocessing import text_clean

#--------------------------------------------------------------
# create 'TriggerWord List'
df2 = pd.read_excel('other/Adhoc_QB_CH_Appointment_Entities_31_10_2023.xlsx',sheet_name='Trigger_Words')
df2 = df2['TriggerWords']
trigger_words_list=[]
for word in df2:
    word= text_clean(word)
    trigger_words_list.append(word)


#--------------------------------------------------------------
# Create 'Appointment_Params_Dict' with Preprocessing'
df_overall = pd.read_excel('other/Adhoc_QB_CH_Appointment_Entities_31_10_2023.xlsx',sheet_name='Params_Sheet')
column_names= df_overall.columns                                    # Get all columns names

all_appointment_params_dict={}                                      # Result: {'Problem:[code...])
for column in column_names:
    df_column=df_overall[column]                                    # get all data from specifice column
    df_column= df_column.dropna()                                   # remove N/A field

    column_code_list=[]
    for code in df_column:
        clean_code= text_clean(code)                                # clean code using module
        column_code_list.append(clean_code)                         # append in list
    column_code_list= sorted(column_code_list,reverse=True)
    all_appointment_params_dict[column]= column_code_list           # insert complete column list in dict like {'Vist Type':[...]}



#==========================================================
# Main Function:
#==========================================================
def appointment_extraction(f_text):
    f_text= ' '+ f_text +' '
    field_status=False
    
    #-----------------------------------------
    # set 'field_status' True if 'Appointment' trigger word mentioned in query
    for trigger_word in trigger_words_list:                         
        trigger_word= ' '+trigger_word+' '
        if trigger_word in f_text:
            field_status=True 
            
    #-------------------------
    # Extract params
    appointment_params_dict={}
    for field_name_key,param_field_list_value in all_appointment_params_dict.items():
        if field_name_key in ['Admitting Provider NPI','Admitting Provider Name','Attending Provider NPI','Attending Provider Name',
                                'Created By','Duration','Start Date','Visit Type']:
            if field_status == False:
                continue                                            # skip current loop cycle
        
        extracted_param_list=[]
        param_field_list_value= sorted(param_field_list_value, key=len, reverse=True)
        for param in param_field_list_value:
            start_index = f_text.find(' '+str(param)+' ')
            if start_index != -1: 
                end_index = start_index + len(param)                # index of the last occurrence of the string in the text
                param_name = f_text[start_index:end_index+1]        # pick words using start & end index
                param_name=" ".join(param_name.split())             # remove extra spaces in selected data
                extracted_param_list.append(param_name)             # append extracted param in list using current key,value of length_dict
                f_text= f_text.replace(' '+param_name+' ',' ')      # remove extracted param from text
        if extracted_param_list:
            try:
                appointment_params_dict[field_name_key].extend(extracted_param_list)
            except:
                appointment_params_dict[field_name_key]= extracted_param_list
    
    #-----------------------------------
    # Remove 'extracted params' from text
    modify_text= f_text
    for param_list in appointment_params_dict.values():
        for param in param_list:
            modify_text = modify_text.replace(' '+param+' ',' ')
    modify_text= ' '.join(modify_text.split())                      # remove extra spaces from text
    
                
    return [appointment_params_dict,modify_text]


#==========================================================

'''
from Modules.For_All.Text_Preprocessing import text_clean

text='Show all appointment record of  type whose  start in 2023 with  duration of 5h follow up pap and end at'
clean_text= text_clean(text)
result= appointment_extraction(clean_text)
print(result)
'''



