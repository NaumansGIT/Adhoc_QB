# -*- coding: utf-8 -*-
"""
    Module: Project QB
    Payer_Params_Extraction 
    Extract all 'Payer params' from input text w.r.to excel sheet and 
    remove extracted params from text
"""

import pandas as pd
from Modules.For_All.Text_Preprocessing import text_clean


#------------------------------
# create 'TriggerWord List'
#------------------------------
df2 = pd.read_excel('other/Adhoc_QB_CH_Attribution_Entities_31_10_2023.xlsx',sheet_name='Trigger_Words')
df2 = df2['TriggerWords']
trigger_words_list=[]
for word in df2:
    word= text_clean(word)
    if word not in trigger_words_list:
        trigger_words_list.append(word)



#-----------------------------------------------------
# Create 'Attribute_Params_Dict' with Preprocessing'
#-----------------------------------------------------
df_overall = pd.read_excel('other/Adhoc_QB_CH_Attribution_Entities_31_10_2023.xlsx',sheet_name='Params_Sheet')
column_names= df_overall.columns                                               # Get all columns names

all_attribute_params_dict={}                                      
for column in column_names:
    df_column=df_overall[column]                                               # get all data from specifice column
    df_column= df_column.dropna()                                              # remove N/A field

    column_entity_list=[]
    for entity in df_column:
        clean_entity= text_clean(entity)                                       # clean code using module
        if clean_entity:
            column_entity_list.append(clean_entity)                            # append in list
    column_entity_list= sorted(column_entity_list, key=len, reverse=True)
    all_attribute_params_dict[column]= column_entity_list                      # insert complete column list in dict 




#==========================================================
# Main Function: 'Params Extraction'
#==========================================================
def attribute_extraction(f_text):
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
    attribute_params_dict={}                                                   # 'final dict' to save result
    for field_name_key,param_field_list_value in all_attribute_params_dict.items():
        if field_name_key in ['Attributed Group','Attributed Practice','Attributed Practice Name','Attributed Program','Attributed Program Type',
                              'Attributed Provider Emp Status','Attributed Provider Id','Attributed Provider Name']:
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
                attribute_params_dict[field_name_key].extend(extracted_param_list)
            except:
                attribute_params_dict[field_name_key]= extracted_param_list

                   
    return [attribute_params_dict,f_text]


#==========================================================
#==========================================================
'''
text= "from Attribute data, Practice Name is arja md pc "
clean_text= text_clean(text)
result= attribute_extraction(clean_text)
print('\n',result[0])
print('\n',result[1])
'''
