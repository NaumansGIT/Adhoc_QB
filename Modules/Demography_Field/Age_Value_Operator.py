# -*- coding: utf-8 -*-
"""
    Module: QB project
    Pick/Extract value & operators for Age
    Final Response is in list ['value','value1','operator']
"""

import re
from Modules.For_All.Extract_Value_Operator_From_Text import value_operator
from Modules.For_All.All_Module_Dictionaries import operator_dict,all_oprt_len_dict


# case: (> 32 and/or/to/' ' < 50) 
pattern = r"(?:\s*(?:>|<|>=|<=)\s*\d+\s*(?:and|or|to)?\s*(?:>|<|>=|<=)\s*\d+)"


#==============================================================
# function start:
#==============================================================
def age_handler(f_param_list,f_text,f_param_dict):
    modify_text= ' '+f_text+' '
    
    
    #-------------------------------------------------
    # 'paramstoken#' dict (remove pad# from f_param)
    all_f_param_token_dict={}
    count=1
    for f_param in f_param_list:
        all_f_param_token_dict['paramtoken'+str(count)]= " ".join(f_param.split())
        count= count+1
    
    
    #-------------------------------------------------
    # insert all params in list
    all_param_list=[]
    for param_list in f_param_dict.values():
        all_param_list.extend(param_list)
    
    
    #-------------------------------------------------
    # replace all params with 'token'
    for pad_param,param_name in all_f_param_token_dict.items():
        modify_text= modify_text.replace(' '+param_name+' ',' '+pad_param+' ')

    for param2 in all_param_list:                                       # replace all 'other' params with 'paramtoken'
        modify_text= modify_text.replace(' '+param2+' ',' othertoken ')
    
    
    #-------------------------------------------------
    # find index of first param of f_param_list 
    modify_text_list= modify_text.split()
    for word in modify_text_list:
        if word in all_f_param_token_dict.keys():
            paramtoken_index= modify_text_list.index(word)
            break
    

    #-------------------------------------------------
    # Text Segmentation: 'Before' & 'After' param
    segmentedtext_list=[]
    for num1 in range((paramtoken_index-1), -1, -1):                    # text before param: back loop
        previous_word= modify_text_list[num1]
        if previous_word == 'othertoken':
            break
        else:
            segmentedtext_list.append(previous_word)                    # insert in 'segmentedtext_list'
    segmentedtext_list.reverse()                                        # reverse list
        
    for next_word in modify_text_list[paramtoken_index:]:               # text after param: forward loop
        if next_word == 'othertoken':
            break
        else:
            segmentedtext_list.append(next_word)
    
    
    #-------------------------------------------------
    # replace 'paramtoken' with actual name
    pad_segmented_text= ' '.join(segmentedtext_list)                       # convert list into string/text
    pad_segmented_text=' '+pad_segmented_text+' '
    segmented_text= pad_segmented_text
    for pad_param_2,param_name_2 in all_f_param_token_dict.items():
        param_name_2= param_name_2.split()                             # remove pad# from param
        param_name_2= param_name_2[:-1]
        param_name_2= ' '.join(param_name_2)
        segmented_text= segmented_text.replace(' '+pad_param_2+' ',' '+param_name_2+' ')     

    
    #-------------------------------------------------
    # replace 'operator text' with 'operator symbole'
    segmented_oprt_text= segmented_text
    for oprt_list in all_oprt_len_dict.values():                      
        for oprt in oprt_list:
            segmented_oprt_text= segmented_oprt_text.replace((' '+oprt+' '), ' '+operator_dict[oprt]+' ')
    

    #-----------------------------------------------------------
    # CASE: search through regex pattren (like '> 32 and < 50')  
    #-----------------------------------------------------------
    matches = re.findall(pattern, segmented_oprt_text)
    if matches:
        match= matches[0]
        match= re.findall(r'\d+', match)                        # extract all number
        valu1= min(match)
        valu2= max(match)
        operator= 'between'
        return [valu1,valu2,operator]
    
    
    #-------------------------------------------------
    # if above CASE fail,then run old cases: 
    #-------------------------------------------------
    f_param_wo_pad= f_param_list[0].split()
    f_param_wo_pad= f_param_wo_pad[:-1]
    f_param_wo_pad= ' '.join(f_param_wo_pad)    
    param_index= segmented_text.find(f_param_wo_pad)
    

    #-------------------------------------
    # case: 'after' param (like after 'age')  
    if f_param_wo_pad not in ['years of age','year of age','year old','years old']:
        segmented_text_updated= segmented_text[param_index:]
        segmented_text_updated=' '+segmented_text_updated+' '
        param_value_oprt= value_operator(segmented_text_updated)
        return param_value_oprt
        
    
    #-------------------------------------
    # case: 'before' param (like before 'year age')
    else:
        segmented_text_updated= segmented_text[:param_index]                          
        segmented_text_updated= ' '+segmented_text_updated+' '                      
        
        
        #-------------------------------
        # replace operator text with symboles
        for oprt_list in all_oprt_len_dict.values():                      
            for oprt in oprt_list:
                segmented_text_updated= segmented_text_updated.replace((' '+oprt+' '), ' '+operator_dict[oprt]+' ')
        
        
        #-------------------------------
        # take last 5 word for 'year age'
        segmented_text_updated_list= segmented_text_updated.split()
        segmented_text_updated_list= segmented_text_updated_list[-5:]
        segmented_text_updated= " ".join(segmented_text_updated_list)
        param_value_oprt= value_operator(segmented_text_updated)                        # pick value & operator through 'value_operator' module
        return param_value_oprt
        
        


                
    
#=============================================================================

'''
from Modules.For_All.Text_Preprocessing import text_clean
from Modules.Grouper_Field.Data_Params_Extraction import param_extraction
#from Modules.Code_Field.Code_Params_Extraction import code_extraction 
from Modules.For_All.Data_Params_Extraction_Optimization import param_optimize

#input_text='all patients male as asdda sdasf patient that older than 4 and younger than 5 and also suffering from diabetic'
#param_list= ['older than 1','younger than 1']

input_text=' Show me all those patients that were diagnosed with bipolar disorder in the last 5 months, with ages between 20 and 40'
param_list= ['ages 1']

text_clean_result= text_clean(input_text)
params_extracted= param_extraction(text_clean_result)
#param_and_code_extaction= code_extraction(text_clean_result,params_extracted)
optimize_params= param_optimize(text_clean_result,params_extracted)

result= age_handler(param_list , optimize_params[0],optimize_params[1])
print('\n >> ',result)
'''

