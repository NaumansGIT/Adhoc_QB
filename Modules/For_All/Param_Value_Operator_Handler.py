# -*- coding: utf-8 -*-
"""
    Module: QB project
    Extract 'Value','Operator' from text but it take two text and remove 
    2nd text from from 1st text, then extract values & operator  
    Use for those fields that contain both 'time' 'and' values like 'Lab/Cost...'
"""


import re
from Modules.For_All.Extract_Value_Operator_From_Text import value_operator
from Modules.For_All.All_Module_Dictionaries import ld_month_pad_dict


#===========================================================================
# Function: After remove specific text,extract 'Values' & 'Operator'
#===========================================================================
def param_value_handler(f_maintext,f_datetext): 
    modify_text=' '+f_maintext+' '
    f_datetext=' '+f_datetext+' '
    for month_key,month_value in ld_month_pad_dict.items():                     # replace all month from text with 'pad' (like 'jan':'Month_01')
        modify_text= modify_text.replace(' '+month_key+' ',' '+month_value+' ')

    #--------------------------------------    
    matches = [match.start() for match in re.finditer(f_datetext, modify_text)] # 're.finditer': find all occurrences of the word 
        
    if len(matches)==1:                                                        # '1 occurrences': simply replace text
        modify_text= modify_text.replace(f_datetext,' ')
        result= value_operator(modify_text)                                    # get result 'value_operator' through function
        return result

    elif len(matches)>1:                                                       # 'More than 1 occurrences'
        endindex= max(matches)                                                 # pick max number from 'matched index list'
        segmented_text= modify_text[:endindex]                                 # text segmentation: from 'start' to 'max#' index 
        result= value_operator(segmented_text)                                 # get result 'value_operator' through function
        return result
    
    else:
        [None,None,None]
        


#==============================================================================
# Main Function: Code
#==============================================================================
def param_text_value_oprt(f_param,f_all_param_date_dict,f_segment_text_dict):
    '''
    print(f_param)
    print(f_all_param_date_dict)
    print(f_segment_text_dict)
    '''
    if f_param in f_all_param_date_dict.keys():                                # pick 'date text_list' from 'f_all_param_date_dict'
        text_to_remove_list= f_all_param_date_dict[f_param]
        text_to_remove= text_to_remove_list[0]
    else:
        text_to_remove= ''
    main_text= f_segment_text_dict[f_param]                                    # pick 'mainText' from 'f_segment_text_dict'
    
    #---------------------------------------------------------
    # case1: if 'remove_to_text_list' is empty (no time given)
    if not text_to_remove:
        output= value_operator(main_text)                                      # get result through 'value_operator' module  
        return output
    
    #---------------------------------------------------------
    # case2: if 'remove_to_text_list' is notempty (time given)
    else:
        output= param_value_handler(main_text,text_to_remove)               # get result through 'param_value_handler' module 
        return output




#============================================================================
'''
from Modules.For_All.Text_Preprocessing import text_clean
from Modules.Grouper_Field.Data_Params_Extraction import param_extraction
from Modules.For_All.Data_Params_Extraction_Optimization import param_optimize
from Modules.DateTime.Extract_All_Params_Date import all_param_date
from Modules.For_All.All_Params_Segmentation import params_segm_text


#text= 'suffered from  depression screening for last 6 years and undergo depression screening and end from jan 2022 to dec 2023 with hba1c is greater than  to -5 from march 2000 to june 2022 and depression for previous 10 days'
text= 'hba1c value is 40 in from 2000 to 2025'
param= 'hba1c 1'

clean_text= text_clean(text)
initial_param= param_extraction(text)
optimize_params= param_optimize(clean_text,initial_param)
segment_text_dict= params_segm_text(optimize_params[1],optimize_params[0])
all_param_date_dict= all_param_date(optimize_params[1],optimize_params[0])

result= param_text_value_oprt(param,all_param_date_dict,segment_text_dict)
print('\n',result)
'''





