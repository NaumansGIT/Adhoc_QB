# -*- coding: utf-8 -*-
"""
    Module: Replace passed params with Adhoc_param name
"""


import pandas as pd
from Modules.For_All.Text_Preprocessing import text_clean


#======================================================
# create dict from sheet 
df = pd.read_excel('other/Adhoc_QB_CH_Care_Plan_Entities_31_10_2023.xlsx',sheet_name='Param_Mapping')
initial_df_dict = df.set_index("Param_Name").to_dict().get('Param_Mapping')

replace_cplan_param_dict = {}
for key,value in initial_df_dict.items():
    key= text_clean(key)
    value= " ".join(str(value).split())
    if key not in replace_cplan_param_dict.keys():
        replace_cplan_param_dict[key]= value



#======================================================
# Main Function
#======================================================
def replace_careplan_param(f_param):
    param_update= " ".join(f_param.lower().split())                # lower + remove extra spaces by split & join    
    try:    
        adhoc_param= replace_cplan_param_dict[param_update]        # get result from above dict
    except:                                                        # in case of error: set same input param name
        adhoc_param= param_update    
    return adhoc_param
    


#======================================================
'''
param='In Progress'
result= replace_careplan_param(param)
print(result)
'''
    
    
    


    
    
    
    
    
    
    
