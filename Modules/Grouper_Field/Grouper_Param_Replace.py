# -*- coding: utf-8 -*-
"""
    Module: Replace passed params with Adhoc_param name
"""


import pandas as pd
from Modules.For_All.Text_Preprocessing import text_clean


#======================================================
# create dict from sheet like this "{depression screening: {'Encounter':'Depression Screening','Problem': 'Depression Screening'....
df = pd.read_excel('other/Adhoc_QB_CH_Param_Entities_31_10_2023.xlsx',sheet_name='Syn_Replace_Final')

replace_grouper_param_dict = {}
for index, row in df.iterrows():                 # Iterate through each row in the DataFrame
    param= row['Ad hoc_Param_Syn_Lower']
    param= text_clean(param)
    entity = row['Entity']
    entity= " ".join(entity.split())
    ad_hoc_param = row['Ad-hoc_Param']    
    try:
        replace_grouper_param_dict[param][entity]= ad_hoc_param
    except:
        replace_grouper_param_dict[param]= {entity:ad_hoc_param}

#======================================================
def replace_grouper_param(f_param,f_params_field):

    # remove pad.No from f_param
    param_update= f_param.split()                       # split text into list
    param_update= param_update[:-1]                     # ignore last index of list
    param_update= " ".join(param_update)                # join all remaining list enities    

    try:
        adhoc_param= replace_grouper_param_dict[param_update]     # get result from above dict
        adhoc_param= adhoc_param[f_params_field]        # pick name w.r.to field like 'Procedure'
    except:                                             # in case of error: set same input param name
        adhoc_param= f_param    

    return adhoc_param
    


#======================================================
'''
param='copd 1'
param_field= 'Problem'
result= replace_grouper_param(param,param_field)
print(result)
'''
    
    
    


    
    
    
    
    
    
    
