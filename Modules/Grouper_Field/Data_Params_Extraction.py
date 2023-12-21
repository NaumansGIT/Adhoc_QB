# -*- coding: utf-8 -*-
"""
    Module: Project QB
    Data_Params_Extraction
    Extract all param from input text w.r.to excel sheet
"""

import pandas as pd
from Modules.For_All.Text_Preprocessing import text_clean

# load sheet, apply preprocessing through function and create new df_table
df_overall = pd.read_excel('other/Adhoc_QB_CH_Param_Entities_31_10_2023.xlsx',sheet_name='Param_Final')
column_names= df_overall.columns                                   # Get all columns names


#==========================================================
# pick the max_length of param 
#==========================================================
column_max_len=[]
for column in column_names:
    df=df_overall[column]                                       # get all data from specifice column
    df= df.dropna()                                             # remove N/A field
    entity_length = [len(data.split()) for data in df]          # calculate each entity length and save in list
    column_max_len.append(max(entity_length))                   # find the max number/length within same column
final_max_len= max(column_max_len)                              # find the max number from all columns


#==========================================================
# create param dictionary (from 'sheet' to 'dict') 
#==========================================================
sheet_to_dict={}
for c_name in column_names:
    df=df_overall[c_name]
    df= df.dropna() 
    
    column_data= []
    for entity in df:
        data= text_clean(entity)                               # apply preprocessing using module
        if data not in column_data:
            column_data.append(data)            
    sheet_to_dict[c_name]= column_data


#==========================================================
# Split the params sheet into different dict w.r.to length
# like "length=1" will come in one dict and so on 
#==========================================================
final_all_params_dict_list=[]                                  # to save all length-wise dict in list
for num in range(final_max_len, 0, -1):                        # run loop from max_length to 1 (like 8 to 1)  
    len_param_dict={}                                          # to save result w.r.to current (loop) condition      
    all_field_len_param_dict={}                                # fill missing field in above dict and save in new dict
    
    for par_key,par_value in sheet_to_dict.items():
        entity_list=[]        
        for entity_1 in par_value:     
            entity_length= len(entity_1.split())
            if entity_length == num:
                entity_list.append(entity_1)    
                len_param_dict[par_key]=entity_list
    
    for c_name_2 in column_names:                              # fill missing param fields
        try:
            all_field_len_param_dict[c_name_2]= len_param_dict[c_name_2]
        except:
            all_field_len_param_dict[c_name_2]= []
    final_all_params_dict_list.append(all_field_len_param_dict)
      
        
#======================================================================
# function to extract params w.r.to above created dicts (dicts in list)
#======================================================================
def param_extraction(f_text):
    extracted_params_wth_list_of_words={}
    for dict_list in final_all_params_dict_list:                               # loop for access all length-wise-dicts (one by one)
        f_text= ' '+ f_text +' '                                               # add space in input_text at start & end 
        all_field_params=[]
        
        for dict_keys,dict_value in dict_list.items():                         # loop for access keys and values of current dict (above dict)
            extract_param_list=[]
            
            #--------------------------------------------------------
            # Find, extract and append param
            #--------------------------------------------------------
            for param in dict_value:
                start_index = f_text.find(' '+str(param)+' ')                  # index of the first occurrence of the string in the text
                if start_index != -1: 
                    end_index = start_index + len(param)                       # index of the last occurrence of the string in the text
                    word = f_text[start_index:end_index+1]                     # pick words using start & end index
                    word=" ".join(word.split())                                # remove extra spaces in selected data
                    extract_param_list.append(word)                            # append extracted param in list using current key,value of length_dict 
                    all_field_params.append(word)                              # list, that will use to remove all extracted params from input-text before start next length-dict  
                    
                    #--------------------------------------------------------
                    # Get already saved data from dict, update and append it. 
                    # if previous data is 'None' insert new data 
                    #--------------------------------------------------------
                    previous_data= extracted_params_wth_list_of_words.get(dict_keys)    
                    if previous_data:
                        previous_data.append(word)
                        extracted_params_wth_list_of_words[dict_keys]= previous_data
                    else:                    
                        extracted_params_wth_list_of_words[dict_keys]= extract_param_list
                        
        #--------------------------------------------------------------------
        # pick all unique params and remove these before start next iteration 
        # (like current length=8, then next is length=7)
        #--------------------------------------------------------------------
        remove_data= set(all_field_params)
        if remove_data:        
            for entity in remove_data:
                f_text= f_text.replace(entity,' ')
                f_text=" ".join(f_text.split())
                
    
    
    #-------------------------------------------------------------------------------------
    # remove all dublicate values in 'extracted_params_wth_list_of_words' (Unique values) 
    #-------------------------------------------------------------------------------------
    final_extracted_params_wth_list_of_words={}
    for key,value in extracted_params_wth_list_of_words.items():
         final_value= list(set(value))
         final_extracted_params_wth_list_of_words[key]= final_value
    return final_extracted_params_wth_list_of_words
                



#======================================================================
# test 'param_extract' function
#======================================================================  

'''
input_text='Digoxin Level,Ejection Fraction,Eye Exam,Functional Status Assessment,GFR'
clean_text= text_clean(input_text)
output= param_extraction(clean_text)
print(output)
'''

       
    


