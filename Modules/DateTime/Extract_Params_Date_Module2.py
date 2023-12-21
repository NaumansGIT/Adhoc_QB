# -*- coding: utf-8 -*-
"""
    Module: QB project
    Extract all params Low_date & high_date and save result in dict
    like >> {'depression': [{'text': 'from 2020 to 2021', 'type': 'low'}]...}
    
"""

import re
import pandas as pd
from Modules.For_All.Text_Preprocessing import text_clean
from Modules.For_All.All_Module_Dictionaries import ld_month_pad_dict


#----------------------------------------------------------------
# load excel sheet , save in list and sorted
df = pd.read_excel('other/Adhoc_QB_Other_Entities_31_10_2023.xlsx',sheet_name='For_Date')
df_to_dict_initial= df.set_index("Date_Decision_Word").to_dict().get('Date_Decision_Oprt')

# create 'Date_Decision_Word' dict
date_decision_word_dict={}
for word,symbol in df_to_dict_initial.items():
    word= text_clean(word)
    if word !='nan':
        date_decision_word_dict[word]= symbol

# sort dict w.r.to 
sorted_date_decision_word_dict = dict(sorted(date_decision_word_dict.items(), key=lambda item: len(item[0]), reverse=True))


#==============================================================================
# all 'Low_date' cases/pattern
all_pattern_dict={
  'year_patterns':[r'\blast\s+(\d+)\s+(?:year|years)\b',                       # for case: "last 6 year"
                   r'\bprevious\s+(\d+)\s+(?:year|years)\b',                   # for case: "previous 3 year"
                   r'\bpast\s+(\d+)\s+(?:year|years)\b',                       # for case: "past 2 year"
                   r'\b\d+\s+(?:year ago|years ago)\b',                        # for case: "6 year ago"                                      
                   r'\b\d+\s+(?:year back|years back)\b',                      # for case: "6 year back"                                      
                   r'not between (\d{4})(?: (?:to|and))? (\d{4})'              # for case: 'not between 2020 to 2021'/'not between 2020 and 2021'/'not between 2020 2021'
                  ],
  'year_patterns_2': [r'between (\d{4})(?: (?:to|and))? (\d{4})\s'],           # for case: 'between 2020 to 2021'/'between 2020 and 2021'/'between 2020 2021'
  'year_patterns_3': [r"\b(?:from\s+)?(\d{4})\s+(?:(?:to|and)\s+)?(\d{4})\b"], # for case: "(from) 2020 to/and/'' 2022",
               
  'month_patterns':[r'\blast\s+(\d+)\s+(?:month|months)\b',                    # for case: "last 6 month"
          r'\bprevious\s+(\d+)\s+(?:month|months)\b',                          # for case: "previous 3 months"
          r'\bpast\s+(\d+)\s+(?:month|months)\b',                              # for case: "past 2 months"
          r'\b\d+\s+(?:month ago|months ago)\b',                               # for case: "6 months ago" 
          r'\b\d+\s+(?:month back|months back)\b',                             # for case: "6 month back"                                      
          r'\bfrom\s+Month_(\d{2})\s+(\d{4})\s+to\s+Month_(\d{2})\s+(\d{4})\b', # for case: "from Month_01 2010 to Month_05 2020"
          r'\bnot\s+between\s+Month_(\d{2})\s+(\d{4})\s+(?:to|and)?\s+Month_(\d{2})\s+(\d{4})\b' # case: "not between Month_01 2020 to Month_05 2022"
                  ],
  'month_patterns_2':[r'\bbetween\s+Month_(\d{2})\s+(\d{4})\s+(?:to|and)?\s+Month_(\d{2})\s+(\d{4})\b'], # case: "between Month_01 2020 to Month_05 2022"

  'day_patterns':[r'\blast\s+(\d+)\s+(?:day|days)\b',                          # for case: "last 6 day/days"
                  r'\bprevious\s+(\d+)\s+(?:day|days)\b',                      # for case: "previous 3 day/days"
                  r'\bpast\s+(\d+)\s+(?:day|days)\b',                          # for case: "past 2 day/days"
                  r'\b\d+\s+(?:day ago|days ago)\b',                           # for case: "6 day/days ago"
                  r'\b\d+\s+(?:day back|days back)\b',                         # for case: "6 day/days back"
                  r'from\s+(\d+)\s+(Month_\d{2})\s+(?:(?:to|and)\s+(\d+)\s+(Month_\d{2}))?\s+(\d{4})'],                     # case: 'from 21 Month_02 to 7 Month_12 2022' 
  'day_patterns_2':[r'from\s+(\d+)\s+(Month_\d{2})\s+(\d{4})\s+(?:(?:to|and)\s+(\d+)\s+(Month_\d{2})\s+(\d{4}))?',          # case: "from 21 Month_02 2020 to 7 Month_12 2022"
                    r'not\s+between\s+(\d+)\s+(Month_\d{2})\s+(\d{4})\s+(?:(?:to|and)\s+(\d+)\s+(Month_\d{2})\s+(\d{4}))?'],# case: 'not between 21 Month_02 2020 to 7 Month_12 2022'  
  'day_patterns_3':[r'between\s+(\d+)\s+(Month_\d{2})\s+(\d{4})\s+(?:(?:to|and)\s+(\d+)\s+(Month_\d{2})\s+(\d{4}))?'],      # case: 'between 21 Month_02 2020 to 7 Month_12 2022' 
  'day_patterns_4':[r'not\s+between\s+(\d+)\s+(Month_\d{2})\s+(?:(?:to|and)\s+(\d+)\s+(Month_\d{2})\s+(\d{4}))?'],          # case: 'not between 21 Month_02 to 7 Month_12 2022'
  'day_patterns_5':[r'between\s+(\d+)\s+(Month_\d{2})\s+(?:(?:to|and)\s+(\d+)\s+(Month_\d{2})\s+(\d{4}))?'],                # case: 'between 21 Month_02 to 7 Month_12 2022'

  
  'current_patterns':[r'\b(?:this|current|present|existing)\s+(?:day|days|month|months|year|years|date|dates)\b'],          # for case: "current day|days|month|months|year|years|date|dates"

  'patterns_1': [ r'\bfrom\s+Month_(\d{2}|\d)\s+to\s+Month_(\d{2})\s+(\d{4})\b',                      # for case: "from Month_01 to Month_05 2020"
                  r'\bnot\s+between\s+Month_(\d{2})\s+(?:(?:to|and)\s+)?Month_(\d{2})\s+(\d{4})\b'],  # for case: "not between Month_01 to Month_05 2022"
  'patterns_1_2':[r'\bbetween\s+Month_(\d{2})\s+(?:(?:to|and)\s+)?Month_(\d{2})\s+(\d{4})\b'],        # for case: "between Month_01 to Month_05 2022"
  'patterns_2': [ r'\b(?:last|previous|past)\s+(?:month|months|year|years)\b', # for case: "last/previous/past month/months/year/years"
                  r'\b\d{1,2} Month_\d{2} \d{4}\b'],                           # for case: "25 Month_01 2010" OR "1 Month_01 2010"
   'patterns_3': [r'\bMonth_\d{2} \d{4}\b'],                                   # for case: "Month_01 2010"
   'patterns_3_1': [r'\bMonth_\d{2}\b'],                                       # for case: "Month_01" 
   'patterns_4': [r'\b\d{4}\b']                                                # for case: "2010" 
        }

#--------------------------------------------------------------------
# patterns: pick those cases who need to be optimized  
pattern_list=[ r"\b(?:from\s+)?(\d{4})\s+(?:(?:to|and)\s+)?(\d{4})\b"]         # for case: "(from) 2020 to/and/'' 2022"


#==============================================================================
# function: to extract param field from dictionary (like ckd -> Problem)
def paramfield(f_param,f_dict):    
    for f_key,f_value in f_dict.items():
        if f_param in f_value:
            return f_key


#==============================================================================
# function: to extract all 'dates' against given 'regex pattern' and return  list
def extract_dates(f_pattern,f_text):
    date_list = []
    start_pos = 0
    while True:
        match = re.search(f_pattern, f_text[start_pos:])                       # Use re.search() to find the next occurrence of a year
        if match:
            date = match.group()                                               # Get the matched date
            date_list.append(date)                                             # append result in list
            start_pos += match.end()                                           # Update the start position for the next search
        else:
            break
    return date_list





#******************************************************************************
# Function: To extract all dates for params (without dicision)
#******************************************************************************
def initial_param_date(f_params_dict,f_text):
    modify_text= ' '+f_text[1:-1]+' '                                           # remove:'.' from start & end of text
    modify_text= modify_text.replace(' of ',' ')


    #-----------------------------------------------------
    # replace 'month' with 'Month_01' from text using 'ld_month_dict' (like 'jan' to 'Month_01'
    for k_month,v_number in ld_month_pad_dict.items():
        modify_text= modify_text.replace(' '+k_month+' ',' '+v_number+' ')


    #-----------------------------------------------------
    # run all above patterns one-by-one and if condition meet
    # create {datetoken:datetext} dict and replace date with datetoken
    #-----------------------------------------------------
    all_datetoken_dict={}
    counter=1    
    for pattern_key,pattern_value in all_pattern_dict.items():
        for pattern in pattern_value:

            #-------------------------------
            # before run 'patterns_4',remove 'from/between' cases from text
            if pattern_key=='patterns_4':
                ext_pattren= r"(?:from|between)?\s*(\d+)\s+(?:(?:to|and|,)?)\s*(\d+)"
                ext_pattren_text_list= extract_dates(ext_pattren,modify_text)  # get result through above function
                if ext_pattren_text_list:                                      # if result not empty,then remove these from text
                    for pattern_text in ext_pattren_text_list:
                        modify_text= modify_text.replace(' '+pattern_text+' ',' ')
            
            #------------------------------- 
            match_1 = re.findall(pattern, modify_text)                         # fetch the values from text through pattern one-by-one
            if match_1:
                date_result= extract_dates(pattern,modify_text)
                for date in date_result:                                       # loop: replace all extracted date_text from 'modify_text' brfore next iteration
                    date= ' '.join(date.split())                               # remove extrac spaces
                    date_token= 'datetoken'+str(counter)                       # create 'datetoken' to replace date_text
                    all_datetoken_dict[date_token]= date                       # create {datetoken:datetext} dict
                    modify_text= modify_text.replace(' '+date+' ',' '+date_token+' ',1)   # replace 'datetext' with 'datetoken' from text
                    counter= counter+1                                         # increment
    all_datetoken_list= list(all_datetoken_dict.keys())                        # save all 'datetoken{num} in list'

        
    
    #-----------------------------------------------------
    # pick all 'unique params' from 'f_params_dict'
    all_param_list=[]
    for param_list in f_params_dict.values():
        for param in param_list:
            if param not in all_param_list:
                all_param_list.append(param)

    
    #-----------------------------------------------------
    # generate 'param_padtoken' dict using 'all_param_list'
    param_padtoken_dict={}
    num=1
    for param_1 in all_param_list:
        param_padtoken_dict[param_1]= f'paramtoken{num}'
        num=num+1
    
    
    #-----------------------------------------------------    
    # > replace all params from 'modify_text'  
    for param_2 in all_param_list:
        modify_text= modify_text.replace(param_2, param_padtoken_dict[param_2])
    modify_text_list= modify_text.split()                                     # split text into words/tokens  

    
    #-----------------------------------------------------    
    # 'SWAPPED dictionaries': to replace 'token/pad' with actal name
    param_padtoken_swapped_dict= {value: key for key, value in param_padtoken_dict.items()}

    
    #---------------------------------------------------------------
    # Set first step: find 'date', move backward until 'param' found
    #---------------------------------------------------------------
    first_date_param_dict={}
    for datetoken2 in all_datetoken_list:
        datetoken_index= modify_text_list.index(datetoken2)
        for num2 in range((datetoken_index-1), -1, -1):                        # back loop: start from datetoken index
            previous_word2= modify_text_list[num2]    
            if previous_word2 in param_padtoken_dict.values():                 # check if 'previous word' is param
                first_date_param_dict[datetoken2]= previous_word2
                break
    
    
    #---------------------------------------------------------------------
    # now using 'first_date_param_dict' get more params against 'datetoken'
    # output formate: {'datetoken1': ['paramtoken3','paramtoken1']
    #---------------------------------------------------------------------   
    date_params_dict={}
    for dp_key,dp_value in first_date_param_dict.items():
        param_index= modify_text_list.index(dp_value)                          # get param index number
        date_params_dict[dp_key]= [dp_value]                                   # insert first (above) 'date:param' in dict
        actual_param1= param_padtoken_swapped_dict[dp_value]                   # get actual param name for 'paramtoken'
        param1_field = paramfield(actual_param1,f_params_dict)                 # get param field name through above function        
        
        for num3 in range((param_index-1), -1, -1):                            # back loop: start from 'paramtoken' index
            previous_word3= modify_text_list[num3]
            if previous_word3 in all_datetoken_list:                           # stop loop: if given word is date
                break
            if previous_word3 in param_padtoken_dict.values():
                actual_param2= param_padtoken_swapped_dict[previous_word3]     # get actual param name for 'paramtoken'
                param2_field = paramfield(actual_param2,f_params_dict)         # get 'param field name' through above function
                if param2_field == param1_field:                               # condition: if next param field is same as previous param field, then insert 
                    date_params_dict[dp_key].append(previous_word3)
                else:                                                          # otherwise: stop/break the loop
                    break
    
    
    #---------------------------------------------------------------------
    # Generate final dict like {param:[date,type]}
    #---------------------------------------------------------------------
    params_date_dict={}
    for pad_param in param_padtoken_dict.values():                             # Access padparam one-by-one
        param_name= param_padtoken_swapped_dict[pad_param]                     # get actual param name for 'paramtoken'1
        
        for date_key,param_value in date_params_dict.items():
            actal_date= all_datetoken_dict[date_key]                           # get actual 'date text' agsint 'datetoken'
            if pad_param in param_value:
                try:
                    params_date_dict[param_name].append(actal_date)
                except:
                    params_date_dict[param_name]= [actal_date]
    return params_date_dict




#==============================================================================
# Main Function code: Get and finalize dates for each params
#==============================================================================
def param_date_module2(f_params_dict,f_text):
    finalize_param_date_dict={}
    f_text= ' '+f_text[1:-1]+' '
    initial_date_result= initial_param_date(f_params_dict,f_text)
    #print('Initial Dict=\n',initial_date_result,'\n')

    for param_name,param_date_list in initial_date_result.items():
        start_index= f_text.find(' '+param_name+' ')                           # find param index
        start_text= ' '+f_text[start_index:]+' '                                      # segmented the text using 'start_index'
        
        #=====================================================
        # Approach1: if all entities are same in list,then just add in time
        if (len(param_date_list)==2) and (param_date_list[0]==param_date_list[1]):
            try:
                finalize_param_date_dict[param_name].append(param_date_list[0])
            except:
                finalize_param_date_dict[param_name]=[param_date_list[0]]
                
        #=====================================================
        # Approach2: Move further to take decision  
        else:
            param_date_list= list(set(param_date_list))                        # pick unique values from list
            for param_date in param_date_list:                                 # loop: pick date one-by-one
                param_date_status=True                                         # Default Status is 'True'
                date_status= True

                #-------------------------------------------------------
                # Set Status: 'True' for Time,'False' for take decision
                if (len(param_date)==4) and param_date.isnumeric():
                    value= int(param_date)
                    if (value<1980) or (value>2025):                           # Decision: if number is come in given range, then ignore it
                        continue
                    else:
                        param_date_status= False
                        
                else:
                    pattren=r"\b(?:from\s+)?(\d{4})\s+(?:(?:to|and)\s+)?(\d{4})\b"  # for case: "(from) 2020 (to/and/'') 2022"
                    match_2 = re.findall(pattren, param_date)                  # fetch the values from text through pattern one-by-one
                    if match_2:
                        param_date_status= False

                        
                #-------------------------------------------------------
                # Take Decision:  decide given entity 'Is' date OR 'Not' 
                if param_date_status == True:
                    try:
                        if param_date not in finalize_param_date_dict[param_name]:
                            finalize_param_date_dict[param_name].append(param_date)
                    except:
                        finalize_param_date_dict[param_name]=[param_date]
                
                #-------------------------------------------------------
                if param_date_status == False:
                    
                    # replace 'month' with padtext (like 'jan' to 'Month_01')
                    for k_month,v_number in ld_month_pad_dict.items():
                        start_text= start_text.replace(' '+k_month+' ',' '+v_number+' ')
                    
                    # remove 'finalize_param_date_dict' values from text (like 'Month_01 2000')
                    for date_text_list in finalize_param_date_dict.values():
                        for date_text in date_text_list:
                            start_text= start_text.replace(' '+date_text+' ',' ')

                    # 're.finditer': find all indexs of given word/number occurrences 
                    matches = [match.start() for match in re.finditer(' '+param_date+' ', start_text)]  
                    
                    #----------------------
                    if len(matches)==1:                                        # '1 occurrences': take decision
                        end_index= matches[0]                                  # find date index from 'above segmented text' 
                        segmented_text= start_text[:end_index]                 # Segment the 'start_text' using 'end_index'             
                        segmented_text= ' '+segmented_text+' '
                        for word_key,symbol_value in sorted_date_decision_word_dict.items():  # replace word with symbol using 'date_decision_word_dict'
                            segmented_text=segmented_text.replace(' '+word_key+' ',' '+symbol_value+' ')
                        segmented_text_list= segmented_text.split()            # convert text into list
                        segmented_text_list.reverse()                          # revert list
                        segmented_text_list= segmented_text_list[:3]           # take 3 index after param (like 'ckd 1')            
                        for word in segmented_text_list:                       # loop
                            try:                                               # Extra variable: just to check if given word is 'number'
                                extra= float(word)                                     
                                date_status= True
                                break
                            except: pass                                       # if word is not 'number'
                            if word == '!=':                                   # set 'False' if word is '!=' (Enitity is not time)
                                date_status= False    
                                break
                            if word == '=':                                    # set 'True' if word is '=' (Enitity is a time)                               
                                date_status= True
                                break  
                        if date_status== True:                                 # Insert in 'final dict'                     
                            try:
                                finalize_param_date_dict[param_name].append(param_date)
                            except:
                                finalize_param_date_dict[param_name]=[param_date]
                    #----------------------
                    else:                                                      # 'More than 1 occurrences': then just insert in 'final dict'
                        try:
                            finalize_param_date_dict[param_name].append(param_date)
                        except:
                            finalize_param_date_dict[param_name]=[param_date]
    return finalize_param_date_dict
  
       
    


#******************************************************************************
#******************************************************************************
'''
from Modules.Grouper_Field.Data_Params_Extraction import param_extraction
from Modules.Code_Field.Code_Params_Extraction import code_extraction 
from Modules.For_All.Data_Params_Extraction_Optimization import param_optimize

#text= 'suffer depression screening ckd and copd from 2020 to 2023 and end at 2024 hba1c is -2 for last 2 years and depression in jan 2020'
#text= 'the diabetes patient in not between 2020 to 2021 and ckd in 2025 to 2030'
#text= 'hba1c levels are low specifically from 2.6 to 3.9 froms 2020 and 2022 and bmi is between 30 and 40 in 2020'
#text= "ckd is between 2020 to 2022 in jan"
text= "ckd is above 2000 and snf copd is below 2000"

text_clean_result= text_clean(text)
initial_extracted_params= param_extraction(text_clean_result)
param_and_code_extaction= code_extraction(text_clean_result,initial_extracted_params)
optimize_params= param_optimize(text_clean_result,param_and_code_extaction)


result= all_param_date(optimize_params[1],optimize_params[0])
print('\nFinal Dic=\n',result)
'''
