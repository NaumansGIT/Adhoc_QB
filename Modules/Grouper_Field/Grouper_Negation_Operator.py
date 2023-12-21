# -*- coding: utf-8 -*-
"""
    Module: QB project
    Pick Negation Operator 
    (like '=','!=')
"""

import pandas as pd


#-----------------------------------------------------------------------
# create 'negation_dict' after apply preprocessing (like 'not suffering':not_suffering)
df = pd.read_excel('other/Adhoc_QB_Other_Entities_31_10_2023.xlsx',sheet_name='All_Operators')

initial_negation_dict = df.set_index("Negation_text").to_dict().get('Negation_replace_text ')
negation_dict={}
for key,value in initial_negation_dict.items():
    key= " ".join(str(key).lower().split())
    value= " ".join(str(value).lower().split())
    negation_dict[key]= value

# Sort 'negation_dict' dict w.r.to lengthwise
sorted_negation_dict= dict(sorted(negation_dict.items(), key=lambda x: len(x[0]), reverse=True))



#-----------------------------------------------------------------------
# function: to extract param field from dictionary (like ckd -> Problem)
def paramfield(f_param,f_dict):    
    for f_key,f_value in f_dict.items():
        if f_param in f_value:
            return f_key
        


#==============================================================
# function start from here
#==============================================================
def negation_oprt(f_param,f_text,f_params_dict):
    
    #-------------------------------------------
    # replace some text with 'negation_dict' values
    #-------------------------------------------
    updated_text= ' '+f_text+' '
    for key,value in sorted_negation_dict.items():
        updated_text= updated_text.replace(' '+key+' ',' '+value+' ')
    
    
    #-------------------------------------------
    # create 'param_token_dic' and 
    # replace all params with token from text
    #-------------------------------------------
    param_token_dict={}
    num=1
    for param_list in f_params_dict.values():
        for param in param_list:
            param_token_dict[param]= f'paramtoken{num}'                          # create 'param_token dict'
            updated_text= updated_text.replace(param,param_token_dict[param])  # replace all params with token
            num= num+1
    # Create 'SWAPPED dictionaries' 
    param_token_swapped_dict= {value: key for key, value in param_token_dict.items()}
    

    
    #------------------------------------------------------------
    # Segment the text and pick required part from input text 
    # Break: take text before param until other field param found
    #------------------------------------------------------------
    text_into_word = updated_text.split()                                     # split the 'token base text'
    param_token = param_token_dict[f_param]                                   # pick the 'f_param' token from 'param_token_dict'
    param_index = text_into_word.index(param_token)                           # pick 'paramtoken' index
    param_field = paramfield(f_param,f_params_dict)                           # get the param field through above function
    
    segmented_text_list=[]
    for num in range((param_index-1), -1, -1):                                # back loop: start before 'paramtoken'
        previous_word= text_into_word[num]   
        segmented_text_list.append(previous_word)                             # append in 'segmented_text_list'
    
        if previous_word in param_token_swapped_dict.keys():                  # check previous word is 'paramtoken'
            nested_param_name= param_token_swapped_dict[previous_word]        # get actual name of param 
            nested_param_field = paramfield(nested_param_name,f_params_dict)  # get the param field through above function            
            if param_field != nested_param_field:
                break

    #------------------------------------------------------------
    # pick  3 word from "segmented_text_list" 
    # if word is not a 'paramtoken',then append in list
    #------------------------------------------------------------
    segmented_text_list_updated=[]
    if len(segmented_text_list) >2:
        target_index=3
        for word in segmented_text_list:
            if word not in param_token_swapped_dict.keys():
                segmented_text_list_updated.append(word)
                target_index= target_index-1
            if target_index==0:
                break
    else:
        segmented_text_list_updated= segmented_text_list[:]

    #------------------------------------------------------------
    # search for 'operator' in 'segmented_text_list_updated'
    #------------------------------------------------------------
    param_operator='='                                                        # Default operator
    for entity in segmented_text_list_updated:
        if entity in sorted_negation_dict.values():
            param_operator='!='
            
    result= [f_param,param_operator]
    return result

    
    

#=============================================================================
'''
from Modules.For_All.Text_Preprocessing import text_clean
from Modules.Grouper_Field.Data_Params_Extraction import param_extraction
#from Modules.Code_Field.Code_Params_Extraction import code_extraction 
from Modules.For_All.Data_Params_Extraction_Optimization import param_optimize


input_text=' All  patients of age is not between 50 to 60  contain  hypertension ckd copd and depression and a of diabetes Mellitus '
param= 'copd 1'
text_clean_result= text_clean(input_text)
initial_extracted_params= param_extraction(text_clean_result)
final_extracted_params= param_optimize(text_clean_result,initial_extracted_params)

result= negation_oprt(param , final_extracted_params[0],final_extracted_params[1])
print(result)
'''



