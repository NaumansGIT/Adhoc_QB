# -*- coding: utf-8 -*-
"""
    Module: Replace passed params with Adhoc_param name
"""


import pandas as pd
from Modules.For_All.Text_Preprocessing import text_clean


#======================================================
# create dict from sheet 
df = pd.read_excel('other/Adhoc_QB_CH_Attribution_Entities_31_10_2023.xlsx',sheet_name='Param_Mapping')
initial_df1_dict = df.set_index("Param_Name").to_dict().get('Adhoc_Mapping')
initial_df2_dict = df.set_index("Provider_Name").to_dict().get('Adhoc_ProviderName_Mapping')
initial_df3_dict = df.set_index("Practice_Name").to_dict().get('Adhoc_PracticeName_Mapping')


replace_attribute_param_dict = {}
for key,value in initial_df1_dict.items():
    key= text_clean(key)
    value= " ".join(str(value).split())
    replace_attribute_param_dict[key]= value


replace_attribute_providername_dict = {}
for key,value in initial_df2_dict.items():
    key= text_clean(key)
    replace_attribute_providername_dict[key]= str(value)
    

replace_attribute_practicename_dict = {}
for key,value in initial_df3_dict.items():
    key= text_clean(key)
    replace_attribute_practicename_dict[key]= str(value)
    



#======================================================
# Main function: Code
#======================================================
def replace_attribute_param(f_param):
    param_update= f_param.split()                                 # remove pad.No from f_param, split text into list
    param_update= " ".join(param_update)                          # join all remaining list enities    
    try:    
        adhoc_param= replace_attribute_param_dict[param_update]   # get result from above dict
    except:                                                       # in case of error: set same input param name
        adhoc_param= param_update    
    return adhoc_param






#======================================================

'''
param='manage healthcare professional'
result= replace_attribute_param(param)
print(result)
'''
    
    


    
    
    
    
    
    
    
