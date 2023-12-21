# -*- coding: utf-8 -*-
"""
    Module: QB project
    Merge all data_params from different module in one 'final_dict'
"""


#==========================================================
def merge_param_module(f_module_output_list):
    
    final_params_dict={}
    for module_output in f_module_output_list:
        for param_key,param_value_list in module_output.items():
            try:
                final_params_dict[param_key].extend(param_value_list)
            except:
                final_params_dict[param_key]= param_value_list
    
    return final_params_dict





#==========================================================
'''
from Modules.For_All.Text_Preprocessing import text_clean
from Modules.Grouper_Field.Data_Params_Extraction import param_extraction
from Modules.Code_Field.Code_Params_Extraction import code_extraction 

text='All patients of age 50 contain hypertension diabetes mellitus	ckd copd and hba1c and  A52.71 293627001 91300 A52.72'
clean_text= text_clean(text)
grouper_params= param_extraction(clean_text)
code_params= code_extraction(clean_text)

result= merge_param_module([grouper_params,code_params])
'''



