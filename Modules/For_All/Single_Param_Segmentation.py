# -*- coding: utf-8 -*-
"""
    Module: Project QB
    Enitity_to_Entity_Segmentation : Forr Single param
    Return : Segmented Text
"""


#==============================================================
# function:
#==============================================================
def param_segm_text(f_param,f_text,f_param_dict):
    modify_text= ' '+f_text+' '
    
    #------------------------------------
    # insert all params in list 
    all_param_list=[]
    for param_list in f_param_dict.values():
        all_param_list.extend(param_list)
    
    #------------------------------------
    # replace all params with 'token' except given param, replace given param with 'paramtoken'
    for param in all_param_list:
        if param == f_param:
            modify_text= modify_text.replace(' '+param+' ',' paramtoken ')
        elif param != f_param:
            modify_text= modify_text.replace(' '+param+' ',' padtoken ')
    
    #------------------------------------
    # segment the text (in list) for given param
    text_into_word= modify_text.split()
    param_index = text_into_word.index('paramtoken')
        
    segmented_text_list=[]
    for num in range(param_index, -1, -1):                   # 'start_text': before 'param'
        if text_into_word[num] =='padtoken':
            break
        else:
            segmented_text_list.append(text_into_word[num])  # append in list
    segmented_text_list.reverse()                            # reverse list 
    for word in text_into_word[(param_index+1):]:            # 'end_text': after 'param'
        if word =='padtoken':
            break
        else:
            segmented_text_list.append(word)
    
    #------------------------------------
    segmented_text= " ".join(segmented_text_list)           # covert list into text (str)
    segmented_text= ' '+segmented_text+' '                  # add space: before and after
    segmented_text= segmented_text.replace(' paramtoken ',' '+f_param+' ')
                                           
    return segmented_text
            
#==============================================================           

'''
from Modules.For_All.Text_Preprocessing import text_clean
from Modules.Grouper_Field.Data_Params_Extraction import param_extraction
from Modules.Code_Field.Code_Params_Extraction import code_extraction 
from Modules.For_All.Data_Params_Extraction_Optimization import param_optimize

input_text='All patients of age 50 contain hypertension and does not including a of diabetes Mellitus as ds 211 code	start with A52.2 276361009 fgh'
param= 'diabetes mellitus 1'

text_clean_result= text_clean(input_text)
initial_extracted_params= param_extraction(text_clean_result)
param_and_code_extaction= code_extraction(text_clean_result,initial_extracted_params)

optimize_params= param_optimize(text_clean_result,param_and_code_extaction)

result= param_segm_text(param , optimize_params[0],optimize_params[1])
print(' >> ',result)
'''



            
            
            
    
    