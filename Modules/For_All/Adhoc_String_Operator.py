# -*- coding: utf-8 -*-
"""
    Module: QB project
    Pick/Extract operators from 'Code' params
    Final Response is in list ['param','operator']
"""

import pandas as pd
from Modules.For_All.Single_Param_Segmentation import param_segm_text



#----------------------------------------------------------
# create 'text_to_symbol_dict' & 'all_operator_text_list'
df = pd.read_excel('other/Adhoc_QB_Other_Entities_31_10_2023.xlsx',sheet_name='Code_Operators')
initial_negation_dict = df.set_index("Text").to_dict().get('Symbols')

text_to_symbol_dict={}
all_operator_text_list=[]
for key,value in initial_negation_dict.items():
    key= " ".join(str(key).lower().split())
    value= " ".join(str(value).lower().split())
    text_to_symbol_dict[key]= value                                    # insert in 'dict'
    if key not in all_operator_text_list:
        all_operator_text_list.append(key)                             # append in 'list'
all_operator_text_list = sorted(all_operator_text_list, key=len, reverse=True)    


#==============================================================
# Function: to extract oprt from text
#==============================================================
def extract_string_oprt(f_text):
    f_text= ' '.join(f_text.split())
    f_text= ' '+f_text+' '
    
    operator= 'contains'                                                # set default operator
    for entity in all_operator_text_list:                               # replace all operator 'text' with 'symbole'
        oprt_symbole= text_to_symbol_dict[entity]
        f_text= f_text.replace(' '+entity+' ',' '+oprt_symbole+' ')
    f_text_list= f_text.split()                                         # convert text into list
    f_text_list.reverse()    
    for word in f_text_list:                                # back loop: before 'paramtoken'
        if word in text_to_symbol_dict.values(): 
            operator= word
            break
    return operator



#==============================================================
# Main function: Start
#==============================================================
def string_operator(f_param,f_text,f_param_dict):
    segmented_text= param_segm_text(f_param,f_text,f_param_dict)        # get 'text for param' through above module
    modify_text= ' '+segmented_text+' '                                 # add spaces: before & after
    modify_text= modify_text.replace(' '+f_param+' ',' paramtoken ')    # replace 'param' with 'token'    
    oprt_result= extract_string_oprt(modify_text)
    return oprt_result
    
    



#=============================================================================

'''
from Modules.For_All.Text_Preprocessing import text_clean
from Modules.Grouper_Field.Data_Params_Extraction import param_extraction
from Modules.Code_Field.Code_Params_Extraction import code_extraction 
from Modules.For_All.Data_Params_Extraction_Optimization import param_optimize

input_text='All patients of age 50 contain hypertension and does not include a of diabetes mellitus	and not contain A18.01 for last 6 month'
param= 'a18.01 1'

clean_text= text_clean(input_text)
grouper_params= param_extraction(clean_text)
param_and_code_extaction= code_extraction(clean_text,grouper_params)
optimize_params= param_optimize(clean_text,param_and_code_extaction)

result= string_operator(param , optimize_params[0],optimize_params[1])
print(' \n>> ',result)
'''




