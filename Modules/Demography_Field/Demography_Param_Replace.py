# -*- coding: utf-8 -*-
"""
Created on Fri Sep 22 15:41:02 2023

@author: Haroo
"""

import pandas as pd
from Modules.For_All.Text_Preprocessing import text_clean

#------------------------------------------------------
demography_replacement_dict={}
df= pd.read_excel('other/Adhoc_QB_CH_Param_Entities_31_10_2023.xlsx',sheet_name='Demogr_Syn_Replace') 
df_to_dictionary= df.set_index("Demography_Entity").to_dict().get('Code')
for k_dict,v_dict in df_to_dictionary.items():
    k_dict= text_clean(k_dict)                      # clean text using 'Text Preprocessing' Module
    demography_replacement_dict[k_dict]=str(v_dict) 

#------------------------------------------------------