# -*- coding: utf-8 -*-
"""
    "SMART QB / Parameters Optimization" : Function for QB project
    function optimize the extracted parameters w.r.to input text
    
    Example: Patient has Allergy with Aspirin -
             "Aspirin" is Medication or Allergy?
"""


#----------------------------------------
#  load 'SMART_params' & 'Default Param' sheet  
import pandas as pd
sp_df = pd.read_excel('other/Adhoc_QB_Other_Entities_31_10_2023.xlsx',sheet_name='Smart_Param')
dp_df = pd.read_excel('other/Adhoc_QB_CH_Param_Entities_31_10_2023.xlsx',sheet_name='Default_Params')

#----------------------------------------
# Default_param_dict: convert 'excel sheet' into 'dict'
initial_default_param_dict = dp_df.set_index("Param_Name").to_dict().get('Default_Field')

default_param_dict={}
for key,value in initial_default_param_dict.items():
    key= " ".join(str(key).lower().split())
    value= " ".join(str(value).split())
    default_param_dict[key]= value





#********************************************************************
# Main function start from here
#********************************************************************
def param_optimize(f_text,f_params_dict):
    final_param_dict={}                                                      # to save end result
    final_text= '. '+f_text+' .'
    
    
    #==========================================
    # append all 'uniqiue params' in list
    #==========================================
    unique_params_list=[]
    for param_list in f_params_dict.values():               
        for param_1 in param_list:
            param_1= param_1.replace(' ','_')
            if param_1 not in unique_params_list:
                unique_params_list.append(param_1)
    
    
    #================================================
    # create dict (like key:param,value:columns_name 
    # (like 'aspirin': ['Problem', 'Medication'])
    #================================================
    param_with_columnname={}
    for dict_key,dict_value_list in f_params_dict.items():
        for param_2 in dict_value_list:
            if param_2 in param_with_columnname:                             # Check if the value already exists as a key in the new dictionary
                param_with_columnname[param_2].append(dict_key)
            else:                                                   
                param_with_columnname[param_2] = [dict_key]

    
    
    #========================================================
    # Sort with 'param_with_columnname' dict with lengthwise
    # (like depression screening , depression ...)
    #========================================================
    sorted_param_with_columnname= dict(sorted(param_with_columnname.items(), key=lambda x: len(x[0]), reverse=True))


    
    #==========================================
    # SMART QB: check the length of dict value & take decision
    #==========================================
    for param_key,param_value in sorted_param_with_columnname.items():
        smartqb_param_status=False                                             # to save SMART_QB param status, set default 'False'
        increment=1
        
        param_wo_underscore= param_key
        param_key= param_key.replace(' ','_')
        final_text= final_text.replace(param_wo_underscore , param_key)
    
        
        #--------------------------------------------------------------
        if len(param_value) ==1:
            prm_key_with_no= param_key+' A'+str(1) 
            final_text= final_text.replace((' '+param_key+' '),(' '+prm_key_with_no+' ')) 
            try:                                                              # 'try': add in list if key already exist in dict
                final_param_dict[param_value[0]].append(prm_key_with_no)
            except:                                                           # 'except' add "key:value" in dict 
                final_param_dict[param_value[0]]= [prm_key_with_no]

        
            
        #--------------------------------------------------------------
        if len(param_value) >1:
            final_text= final_text.replace(' '+param_key+' ',' padtoken ')
            text_into_list= final_text.split()
            param_index_list = [index for index, item in enumerate(text_into_list) if item == 'padtoken']
        
            for param_index in param_index_list:

                #--------------------------------------------------------------
                # take words before params (previous words target: 3)
                words_list_bf_param=[]                                        # to store words before param
                bf_param_target_index=3
                loop_iteration= 1
                loop_break=0
                while( len(text_into_list)>0 and param_index>0):              # set codition for run ( not empty & index >0)
                    previous_word_index= param_index - loop_iteration         # pick 'word_index' before param
                    previous_word= text_into_list[previous_word_index]        # pick word using above index
                    
                    loop_iteration= loop_iteration+1                          # loop increament
                    if (not previous_word.isdigit()) and (previous_word!='padtoken') and (previous_word not in unique_params_list):                          # if previous word is not 'param',then append in list 
                        words_list_bf_param.append(previous_word)           
                        loop_break= loop_break+1 
                    if (previous_word_index<1) or (loop_break==bf_param_target_index):   # set condition for stop/break the loop
                        break
                words_list_bf_param.reverse()                                 # reverse list order

                
                #--------------------------------------------------------------
                # take words after params (next words target: 1 )
                words_list_af_param=[]                                       # to store words after param
                text_list_af_param= text_into_list[param_index:]             # take index after 'param' from list
                
                if len(text_list_af_param) >1:
                    next_word= text_into_list[param_index+1]                 # pick word using above index
                    if (next_word != 'padtoken') and (next_word not in unique_params_list):  # take next words only if not params
                        words_list_af_param.append(next_word) 

                
                #--------------------------------------------------------------
                # Merge all list_of_words and convert in 'str text'
                segmented_text_list=[]
                segmented_text_list.extend(words_list_bf_param)               # add word_list before param in list
                segmented_text_list.extend(words_list_af_param)               # add word_list after param in list
                segmented_text= " ".join(segmented_text_list)                 # join list of word (str text)
                segmented_text= ' ' +segmented_text+ ' '                      # add space (at start & end)

                
                #--------------------------------------------------------------
                # Search in 'SMART QB' sheet w.r.to extracted column name and insert result in 'smartqb_param_status' dict
                for colm_name in param_value:                                 # loop: on param_value (list)
                    colm_data= sp_df[colm_name].dropna()                      # get complete column data & remove 'nan'
                    for data in colm_data:                                    # take selected column entity 'one-by-one' 
                        data= " ".join(data.split())
                        data= ' ' +data+ ' '  
                        if data in segmented_text:
                            prm_key_with_no= param_key+' A'+str(increment)
                            text_into_list[param_index]= (prm_key_with_no)
                            final_text= " ".join(text_into_list)
                            smartqb_param_status=True 
                            try:                                                   # 'try': add in list if key already exist in dict
                                final_param_dict[colm_name].append(prm_key_with_no)
                            except:                                                # 'except' add "key:value" in dict 
                                final_param_dict[colm_name]= [prm_key_with_no]
                            increment= increment+1
                final_text= final_text.replace('padtoken',param_key)   

            
            #--------------------------------------------------------------
            if smartqb_param_status == False :                                    
                if param_wo_underscore in default_param_dict.keys():            # pick 'default' param field 
                    default_param_field= default_param_dict[param_wo_underscore]
                    try:
                        final_param_dict[default_param_field].append(param_key+' A'+str(1))
                    except:                        
                        final_param_dict[default_param_field]= [param_key+' A'+str(1)]
                    final_text= final_text.replace(param_key,param_key+' A'+str(1))
                    
                else:
                    for colm_name_2 in param_value:                            # take column 'one-by-one'
                        param_increment= param_key+' A'+str(1)
                        try:                                                   # 'try': add in list if key already exist in dict
                            final_param_dict[colm_name_2].append(param_increment)
                        except:                                                # 'except': add "key:value" in dict (key:value) 
                            final_param_dict[colm_name_2]= [param_increment]
                    final_text= final_text.replace(param_key,param_key+' A'+str(1))

    
        
    
    #--------------------------------------------------------------  
    # Replace '_' from 'text' and dictionary     
    #--------------------------------------------------------------
    final_text= final_text.replace('_',' ')                                   # replace '_' with ' ' from final_text          
    final_param_dict_updated={}
    for key,value_list in final_param_dict.items():                           # replace '_' with ' ' from final_dictionary     
        for value in value_list:
            value= value.replace('_',' ')
            try:                                                              # 'try': add in list if key already exist in dict
                final_param_dict_updated[key].append(value)
            except:                                                           # 'except' add "key:value" in dict 
                final_param_dict_updated[key]= [value]
                       

    return final_text,final_param_dict_updated

    

#====================================================================
#====================================================================
'''
from Modules.Text_Preprocessing import text_clean
from Modules.Data_Params_Extraction import param_extraction

#input_text='depression screening  '
input_text='Digoxin Level,Ejection Fraction,Eye Exam,Functional Status Assessment,GFR'

clean_text= text_clean(input_text)
initial_extracted_params= param_extraction(clean_text)
Final_extracted_params= param_optimize(clean_text,initial_extracted_params)


print('\ninitial= ',clean_text)
print('update=',Final_extracted_params[0])
print('\ninitial params=\n',initial_extracted_params)
print('\nFinal params=\n',Final_extracted_params[1])
'''

        
