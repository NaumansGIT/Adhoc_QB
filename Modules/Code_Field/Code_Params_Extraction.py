# -*- coding: utf-8 -*-
"""
    Module: Project QB
    Data_Code_Extraction 
    Extract all codes from input text w.r.to Dictionary (excel sheet) 
    Return: dict like {'Problem': ['a52.2', 'a52.72']..}
"""

from Modules.Code_Field.Dictionaries_For_Code import all_fied_nonnumeric_codes,all_fied_numeric_codes


#==========================================================
def code_extraction(f_text,f_params_dict):
    f_text= ' '+ f_text +' '                                            # add spaces (start & at end)
    final_extracted_param_dict= f_params_dict

    
    #===============================
    # Extract Non-Numeric code
    #-------------------------------
    for field_name_key,field_code_value in all_fied_nonnumeric_codes.items():
        extract_code_list=[]
        for code in field_code_value:
            start_index = f_text.find(' '+str(code)+' ')
            if start_index != -1:                
                end_index = start_index + len(code)                          # index of the last occurrence of the string in the text
                param_code = f_text[start_index:end_index+1]                 # pick words using start & end index
                param_code=" ".join(param_code.split())                      # remove extra spaces in selected data
                f_text= f_text.replace(' '+param_code+' ',' ')
                extract_code_list.append(param_code)                         # append extracted param in list using current key,value of length_dict 
        if extract_code_list:
            try:
                final_extracted_param_dict[field_name_key].extend(extract_code_list)
            except:
                final_extracted_param_dict[field_name_key]= extract_code_list

                
    #===============================
    # Extract Numeric code
    #-------------------------------
    modify_text= f_text.replace(' codes ',' code ')                             # replace 'codes' with 'code'
    
    #---------------------
    # replace 'f_params' with 'paramtoken' from text
    for param_list in f_params_dict.values():
        for param in param_list:
            modify_text= modify_text.replace(' '+param+' ',' paramtoken ')
            
    
    #----------------------
    if ' code ' in modify_text:                                                 # condition: if 'code' is in text
        segmented_text_list=[]                                                  # to save all text against 'code' 
        text_list= modify_text.split()                                          # convert text into list
        indices = [i for i, word in enumerate(text_list) if word == 'code']     # Using list comprehension to find all index
        for index in indices:                                                   # run index# one by one
            word_list=[]
            for next_word in text_list[index:]:                                 # loop: w.r.to start point(index)
                if next_word=='paramtoken':                                     # break loop: if 'next_word' is 'param'
                    break
                word_list.append(next_word)                                     # otherwise: append in 'word_list'
                list_to_text= ' '.join(word_list)                               # covert list into text string
            segmented_text_list.append(list_to_text)                            # append this 'text' in 'segmented_text_list'

        
        #--------------------------------
        # take 'segmented_text' one-by-one and extract codes from it
        for segmented_text in segmented_text_list:
            segmented_text= ' '+segmented_text+' '
            for field_name_key,field_code_value in all_fied_numeric_codes.items():
                extract_code_list=[]
                for code in field_code_value:
                    start_index = segmented_text.find(' '+str(code)+' ')
                    if start_index != -1:
                        end_index = start_index + len(code)                     # index of the last occurrence of the string in the text
                        param_code = segmented_text[start_index:end_index+1]    # pick words using start & end index
                        param_code=" ".join(param_code.split())                 # remove extra spaces in selected data
                        extract_code_list.append(param_code)                    # append extracted param in list using current key,value of length_dict                 
                if extract_code_list:
                    try:
                        final_extracted_param_dict[field_name_key].extend(extract_code_list)
                    except:
                        final_extracted_param_dict[field_name_key]= extract_code_list
    return final_extracted_param_dict

            




#==========================================================
'''
from Modules.For_All.Text_Preprocessing import text_clean
from Modules.Grouper_Field.Data_Params_Extraction import param_extraction

#text='Show all hba1c record with 294410005 code A52.2 33267	91300  ckd 3074F 796.2'
text= 'show all male patient with codes 3 294410005 and A52.2 and also suffering from ckd with codes 796.2 and copd'
clean_text= text_clean(text)

grouper_params= param_extraction(clean_text)
result= code_extraction(clean_text,grouper_params)
print(result)
'''



