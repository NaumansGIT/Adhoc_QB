# -*- coding: utf-8 -*-
"""
    QB project: LLM Date Module
    Extract and replace all 'values' from text with token 
"""

import re


#==============================================================================
# all 'Regex' cases/pattern to extract values
all_pattern_dict={
  'patterns_1':[ r"\b\s+from+\s+?(-?\d+(?:\.\d+)?)\s+(?:(?:to|and)\s+)?(-?\d+(?:\.\d+)?)\b",
                 r"\b\s+not between+\s+?(-?\d+(?:\.\d+)?)\s+(?:(?:to|and)\s+)?(-?\d+(?:\.\d+)?)\b",
                 r"\b\s+between+\s+?(-?\d+(?:\.\d+)?)\s+(?:(?:to|and)\s+)?(-?\d+(?:\.\d+)?)\b",
                 r"\b\s+?(-?\d+(?:\.\d+)?)\s+(?:(?:to|and)\s+)?(-?\d+(?:\.\d+)?)\b"],
  'patterns_2':[ r"\b\s+?(-?\d+(?:\.\d+)?)\s" ]}
    
                   
               
#====================================================
# function: to extract all 'values' against given 'regex pattern' and return list
def extract_values(f_pattern,f_text):
    date_list = []
    start_pos = 0
    while True:
        match = re.search(f_pattern, f_text[start_pos:])                       # Use re.search() to find the next occurrence of a year
        if match:
            date = match.group()                                               # Get the matched date
            date_list.append(date)                                             # append result in list
            start_pos += match.end()                                           # Update the start position for the next search
        else:   break
    return date_list


#====================================================
# function: to find all indexs of given date from text 
def find_date_indices(f_list,f_text):
    date_dict_indexs_list={}
    f_list= sorted(set(f_list),reverse=True)
    
    list1,list2=[],[]
    for entity in f_list:
        if ('from' in entity) or ('not betwe en' in entity) or ('between' in entity):
            list1.append(entity)
        else:
            list2.append(entity)

    #------------------------------------    
    for entity in list1:
        indices = []
        start_index = 0
        while start_index < len(f_text):
            index = f_text.find(' '+entity+' ', start_index)
            if index == -1:
                break
            indices.append(index)
            start_index = index + len(entity)
        date_dict_indexs_list[entity]=indices
        replace_word= 'X'*len(entity)
        f_text= f_text.replace(' '+entity+' ',' '+replace_word+' ')
        
    #------------------------------------
    for entity in list2:
        indices = []
        start_index = 0
        while start_index < len(f_text):
            index = f_text.find(' '+entity+' ', start_index)
            if index == -1:
                break
            indices.append(index)
            start_index = index + len(entity)
        date_dict_indexs_list[entity]=indices
    return date_dict_indexs_list



#******************************************************************************
# Main Function code:  extract all dates for params (without dicision)
#******************************************************************************
def replace_value_with_token(f_text):
    value_pad_dict={}                                                          # to save final result in dict    
    modify_text= ' '+f_text+' '                                               
    print(modify_text)
                
    #-----------------------------------------------------
    # run Reg-pattren and extract all dates 
    #-----------------------------------------------------    
    tempory_text= modify_text                                                  # text: to extract dates and remove from text  
    initial_values_list=[]
    for pattern_key,pattern_list in all_pattern_dict.items():
        for pattern in pattern_list:
            match_1 = re.findall(pattern, tempory_text)                        # fetch the values from text through pattern one-by-one
            if match_1:
                value_list= extract_values(pattern,tempory_text)               # extract all date from text using above function
                for value in value_list:
                    value= ' '.join(value.split())
                    initial_values_list.append(value)            
                    tempory_text = tempory_text.replace(' '+value+' ',' ')     # remove extractted time from text
        
    #-----------------------------------------------------
    # get 'indexes' of all 'values' from 'text' using above function
    #-----------------------------------------------------
    values_index_dict= find_date_indices(initial_values_list,modify_text)            
    values_index_dict = {value: key for key, indices in values_index_dict.items() for value in indices}
    values_index_dict= dict(sorted(values_index_dict.items()))                 # sort:'values_index_dict' w.r.to index number      
    
    #-----------------------------------------------------
    valuecount= 0
    for value in list(values_index_dict.values()):
        value_index= modify_text.find(' '+value+' ')                                                         
        pad_token= 'VALUE'+str(valuecount)                                     # create 'value-token' for replace 
        valuecount= valuecount+1                                               # increament in token.No
        second_start= (value_index+len(value))+1                               # set second start index for 'text' 
        modify_text= modify_text[:value_index]+' '+pad_token+' '+modify_text[second_start:]                                                     
        value_pad_dict[pad_token]= value                                       # add 'value-with-token' in dict  

    modify_text= ' '.join(modify_text.split())
    return {'text':modify_text,'values':value_pad_dict}
    
    
    
    
#******************************************************************************
#******************************************************************************

'''
from Modules.For_All.Text_Preprocessing import text_clean
text= 'the -30 to -5.5 hba1c levels are low specifically from -2.6 to -3.9 and bmi is between 30 and 40 and age is above 40 and hba1c not between -5.5 and 5.5'
clean= text_clean(text)

result= replace_value_with_token(text)
'''




