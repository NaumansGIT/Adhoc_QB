# -*- coding: utf-8 -*-
"""
    Operator Dictionaries for QB Modules
"""

import pandas as pd


#==============================================================================
# Operators Dictionary
#==============================================================================

# load excel file, perform preprocessing and create new Datafram
df_main_initial= pd.read_excel('other/Adhoc_QB_Other_Entities_31_10_2023.xlsx',
                               sheet_name='All_Operators',usecols=["Operators_Text","Operators_Symbols"])

rows = []                                                               # create an empty list to store the accessed rows 
for index, row in df_main_initial.iterrows():                           # Iterate over each row of 'df_main'
    Operators_Text= row['Operators_Text']                               # Access row data entity one-by-one
    Operators_Text= " ".join(str(Operators_Text).lower().split())
    Operators_Symbol= row['Operators_Symbols']      
    Operators_Symbol= " ".join(str(Operators_Symbol).lower().split())
    rows.append({'Operators_Text':Operators_Text,'Operators_Symbols':Operators_Symbol})
df_main = pd.DataFrame(rows)                                            # Create new updated 'DataFrame' 


# create operator_dict by using 'df_main' (like 'is':'=')
operator_dict = df_main.set_index("Operators_Text").to_dict().get('Operators_Symbols')         
unique_operator_list= list(set(operator_dict.values()))


# divide the operators w.r.to len (data:length)
df_segment= df_main['Operators_Text']

# get the len of data and create dict (data:length)
data_len_dic = {data:(len( str(data).split() )) for data in df_segment}            
max_len= max( data_len_dic.values() )

all_oprt_len_dict={}
for num in range(max_len, 0, -1):
    list_name = f"word_length_{num}_list"
    all_oprt_len_dict[list_name] = []
    
    for key_1,value_1 in data_len_dic.items(): 
        if value_1==(num):
            all_oprt_len_dict[f"word_length_{num}_list"].append(str(key_1))






#==============================================================================
# Dictionaries_Date (Low/high)
#==============================================================================
# ld_month_pad_dict (like 'jan':'Month_01')
#------------------------------------------

# load Excel sheet
low_date_df = pd.read_excel("other/Adhoc_QB_Other_Entities_31_10_2023.xlsx", sheet_name='For_Date')
ld_month_pad_dict_df = low_date_df.set_index("Month_Name").to_dict().get('Month_Token')     # convert 'df' into 'dict'

ld_month_pad_dict={}
for key_month,value_month in ld_month_pad_dict_df.items():
    key_month=" ".join(str(key_month).lower().split())                            # apply preprocessing
    value_month= " ".join(str(value_month).split())
    if key_month != 'nan':                                                   # check for 'nan'
        ld_month_pad_dict[key_month]= value_month                       




#-------------------------------------------
# Date Operator dictionary (like 'after':'>')
#-------------------------------------------
# convert sheet into dict
sheet_to_dict = low_date_df.set_index("Date Operators").to_dict().get('Replace with')  

date_operator_dict={}
for key_oprt,value_symb in sheet_to_dict.items():
    key_oprt=" ".join(str(key_oprt).lower().split())                         # apply preprocessing on 'key'
    if key_oprt != 'nan':                                                    # check for 'nan'
        value_symb= " ".join(value_symb.lower().split())                     # apply preprocessing on 'value'
        date_operator_dict[key_oprt]= value_symb                               # insert into dict

# Sort dict w.r.to lengthwise
date_operator_dict= dict(sorted(date_operator_dict.items(), key=lambda x: len(x[0]), reverse=True))


#==============================================================================













