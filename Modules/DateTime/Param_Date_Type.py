# -*- coding: utf-8 -*-
"""

"""

import pandas as pd
from Modules.For_All.Text_Preprocessing import text_clean


#------------------------------------------
# create 'Date_Type_Decision' dict
#------------------------------------------
df = pd.read_excel('other/Adhoc_QB_Other_Entities_31_10_2023.xlsx',sheet_name='For_Date')
df_to_dict_initial= df.set_index("Date_Type_Word").to_dict().get('Date_Type_oprt')

date_type_decision_dict={}
for word,symbol in df_to_dict_initial.items():
    word= text_clean(word)
    if word !='nan':
        date_type_decision_dict[word]= symbol
        
        

#========================================================
# Main Function: Code
#========================================================
def get_date_type(f_param,f_date,f_text):
    date_type= 'low_date'                                                      # set default value
    f_text=' '+f_text+' '                                                      # add spaces
    start_index= f_text.find(' '+f_param+' ')                                  # startindex: get the index of 'param'
    end_index= f_text.find(' '+f_date+' ')                                     # endindex: get the index of 'date'
    segmented_text= ' '+f_text[start_index:end_index]+' '                      # segment the text w.r.to indexes
    for work_key,replace_value in date_type_decision_dict.items():             # replace word from 'segmented_text' through 'date_type_decision_dict'
        segmented_text= segmented_text.replace(' '+work_key+' ',' '+replace_value+' ')
    segmented_text_list= segmented_text.split()                                # convert text into list
    segmented_text_list.reverse()                                              # revert list
    for word in segmented_text_list:                                           # take decision: for 'date_type'
        if word=='high':
            date_type='high_date'
            break
        elif word=='low':
            date_type= 'low_date'
            break
    return date_type
            
                            

#========================================================
'''
text='also ip encounter patient admitting 2022 and discharge at 2020'
param= 'ip'
date= '2020'
result= get_date_type(param,date,text)
print('\nresult:',result)
'''
