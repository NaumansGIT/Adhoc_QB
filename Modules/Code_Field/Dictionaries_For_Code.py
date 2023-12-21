# -*- coding: utf-8 -*-
"""
    Project: Adhoc-QB    
    All dictionary for 'code'
"""

import pandas as pd
from Modules.For_All.Text_Preprocessing import text_clean


#======================================================================
# Create 'NonNumeric_Code_Dictionary' for all fields with preprocessing
# (like {'Problem:[code...])
#======================================================================

df_nonnumeric_code = pd.read_excel('other/Adhoc_QB_CH_Code_Entities_31_10_2023.xlsx',sheet_name='Mix_codes')
column_names= df_nonnumeric_code.columns                                # Get all columns names

all_fied_nonnumeric_codes={}                                            # Result: {'Problem:[code...])
replace_with_actual_code_dict={}                                        # Result: {'a0021':'A0021'}
for column in column_names:
    df_column=df_nonnumeric_code[column]                                # get all data from specifice column
    df_column= df_column.dropna()                                       # remove N/A field
    
    column_code_list=[]
    for code in df_column:
        clean_code= text_clean(code)                                    # clean code using module
        column_code_list.append(clean_code)                             # append in list
        replace_with_actual_code_dict[clean_code]= code                 # insert in 'code_replace_dict' (like {'a0021':'A0021'})
    all_fied_nonnumeric_codes[column]= list(set(column_code_list))      # insert unique column list in dict like {'Problem':[...]}



#======================================================================
# Create 'Numeric_Code_Dictionary' for all fields with preprocessing
#======================================================================

df_numeric_code = pd.read_excel('other/Adhoc_QB_CH_Code_Entities_31_10_2023.xlsx',sheet_name='Numerical_codes')
column_names= df_numeric_code.columns                               # Get all columns names

all_fied_numeric_codes={}                                           # Result: {'Problem:[code...])
for column in column_names:
    df_column=df_numeric_code[column]                               # get all data from specifice column
    df_column= df_column.dropna()                                   # remove N/A field
    
    column_code_list=[]
    for code in df_column:
        clean_code= text_clean(int(code))                           # clean code using module
        column_code_list.append(clean_code)                         # append in list
        replace_with_actual_code_dict[clean_code]= code             # insert in 'code_replace_dict' (like {'a0021':'A0021'})
    all_fied_numeric_codes[column]= list(set(column_code_list))     # insert complete column list in dict like {'Problem':[...]}

#--------------------------------------
#add decimal code in dict
more_code=['796.2','796.3']
all_fied_numeric_codes['VitalSign'].extend(more_code)

for code in more_code:
    replace_with_actual_code_dict[code]= code




