# -*- coding: utf-8 -*-
"""
    Module: Replace passed params with Adhoc_param name
"""


import pandas as pd
from Modules.For_All.Text_Preprocessing import text_clean


#======================================================
# create dict from sheet 
df = pd.read_excel('other/Adhoc_QB_CH_Appointment_Entities_31_10_2023.xlsx',sheet_name='Param_Mapping')
initial_df_dict = df.set_index("Param_Name").to_dict().get('Param_Mapping')

replace_app_param_dict = {}
for key,value in initial_df_dict.items():
    key= text_clean(key)
    value= " ".join(str(value).lower().split())
    replace_app_param_dict[key]= value



#======================================================
def replace_app_param(f_param):

    # remove pad.No from f_param
    param_update= f_param.split()                           # split text into list
    param_update= param_update[:-1]                         # ignore last index of list
    param_update= " ".join(param_update)                    # join all remaining list enities    
    try:    
        adhoc_param= replace_app_param_dict[param_update]   # get result from above dict
    except:                                                 # in case of error: set same input param name
        adhoc_param= param_update    

    return adhoc_param
    


#======================================================
'''
param='phone visit 1'
result= replace_app_param(param)
print(result)
'''
    
    
    


    
    
    
    
    
    
    
