# -*- coding: utf-8 -*-
"""
    QB project: LLM Date Module
    Extract and replace all times from text with token 
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
date_decision_dict={}
for word,symbol in df_to_dict_initial.items():
    word= text_clean(word)
    if word !='nan':
        date_decision_dict[word]= symbol

# sort dict w.r.to length
date_decision_dict = dict(sorted(date_decision_dict.items(), key=lambda item: len(item[0]), reverse=True))


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


#====================================================
# function: to extract all 'dates' against given 'regex pattern' and return list
def extract_dates(f_pattern,f_text):
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
        if ('from' in entity) or ('not between' in entity) or ('between' in entity):
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
def replace_time_with_token(f_text):
    time_pad_dict,value_pad_dict={},{}                                         # to save final result in dict
    
    f_text= ' '+f_text+' '                                               
    modify_text= f_text.replace(' of ',' ')

    #-----------------------------------------------------
    # replace 'month' with 'Month_01' from text using 'ld_month_dict' 
    #-----------------------------------------------------
    for k_month,v_number in ld_month_pad_dict.items():
        modify_text= modify_text.replace(' '+k_month+' ',' '+v_number+' ')
        f_text= f_text.replace(' '+k_month+' ',' '+v_number+' ')
        
        
    #-----------------------------------------------------
    # run Reg-pattren and extract all dates 
    #-----------------------------------------------------    
    timecount,valuecount= 0,0
    tempory_text= modify_text                                                  # text: to extract dates and remove from text  
    initial_date_list=[]
    for pattern_key,pattern_value in all_pattern_dict.items():
        for pattern in pattern_value:
            match_1 = re.findall(pattern, tempory_text)                        # fetch the values from text through pattern one-by-one
            if match_1:
                date_list= extract_dates(pattern,tempory_text)                 # extract all date from text using above function
                initial_date_list.extend(date_list)
                for date in date_list:
                    tempory_text = tempory_text.replace(' '+date+' ',' ')      # remove extractted time from text
    
    #-----------------------------------------------------
    # get 'indexes' of all 'dates' from 'text'  using above function
    #-----------------------------------------------------
    date_index_dict= find_date_indices(initial_date_list,modify_text)            
    date_index_dict = {value: key for key, indices in date_index_dict.items() for value in indices}
    date_index_dict= dict(sorted(date_index_dict.items()))                     # sort:'date_index_dict' w.r.to index number      


    #-----------------------------------------------------
    for date in list(date_index_dict.values()):
        date_index= modify_text.find(' '+date+' ')                
        segmented_text= ' '+modify_text[:date_index]+' '                       # text segmentation: from 'start' to 'index'                                            
        for word,symbol in date_decision_dict.items():                         # replace words with symbols using 'sorted_date_decision_word_dict'
            segmented_text= segmented_text.replace(' '+word+' ',' '+symbol+' ')
        segmented_text_list= segmented_text.split()                            # conert string into list
        segmented_text_list.reverse()                                          # reverse above list                                             
                
        #--------------------------------------------
        # Condition: set 'date_status' (True/False)
        date_status= None
        decision_index=3
        for num in range(decision_index):
            consider_word= segmented_text_list[num]                                
            if consider_word=='=':
                date_status= True
                break
            elif consider_word=='!=':
                date_status= False
                break    
        
        #--------------------------------------------
        # 'True': replace time from text with token and add in 'time-dict'
        if date_status==True:                                  
            pad_token= 'TIME'+str(timecount)                                   # create 'time-token' for replace 
            timecount= timecount+1                                             # increament in token.No
            second_start= (date_index+len(date))+1                             # set second start index for 'text' 
            modify_text= modify_text[:date_index]+' '+pad_token+' '+modify_text[second_start:]                                                     
            time_pad_dict[pad_token]= date                                     # add 'time-with-token' in dict  
        
        # 'False': replace Value from text with token and add in 'value-dict'
        else:                                  
            pad_token= 'VALUE'+str(valuecount)                                 # create 'value-token' for replace 
            valuecount= valuecount+1                                           # increament in token.No
            second_start= (date_index+len(date))+1                             # set second start index for 'text' 
            modify_text= modify_text[:date_index]+' '+pad_token+' '+modify_text[second_start:]                                                     
            value_pad_dict[pad_token]= date                                    # add 'value-with-token' in dict  
        
    
    #-----------------------------------------------------
    # replace 'VALUE-Token' with actual word 
    #-----------------------------------------------------
    for value_token,actual_value in value_pad_dict.items():
        modify_text= modify_text.replace(' '+value_token+' ',' '+actual_value+' ')
    modify_text= ' '.join(modify_text.split())
    return {'text':modify_text,'times':time_pad_dict}
    
    
    
    
#******************************************************************************
#******************************************************************************
'''
#text= 'hba1c levels are low specifically from 2.6 to 3.9 in from 2020 and 2022 and bmi is between 30 and 40 in last 2 months and also in 2020'
text='african male patients that are suffering from ckd,copd and depression screening in 2020 and underwent depression screening in last 6 months with hba1c is 50 in 2025'

result= replace_time_with_token(text)
print('\n\nText:',result['text'])
print('\nTime Dic: ',result['times'])
'''



