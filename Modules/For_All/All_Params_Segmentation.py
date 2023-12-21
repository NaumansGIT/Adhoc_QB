# -*- coding: utf-8 -*-
"""
    Module: Project QB
    Enitity_to_Entity_Extraction/Segmentation
    Divide input text into segments w.r.to param
"""

from Modules.For_All.All_Module_Dictionaries import operator_dict,all_oprt_len_dict

'''
from Modules.Text_Preprocessing import text_clean
from Modules.Data_Params_Extraction import param_extraction
from Modules.Extracted_Params_Optimization import param_optimize
'''

#===============================================================
# Text-to_symbole function
# serach in "all_oprt_len_dict" (from max to low ) for operator and replace with symbol 
#===============================================================
def text_oprt_into_symbol(f_text):
    f_text= ' '+" ".join(f_text.split()) +' '            
    for oprt_list in all_oprt_len_dict.values():                       
        for oprt in oprt_list:
            if oprt in f_text:
                f_text= f_text.replace((' '+oprt+' '), ' '+operator_dict[oprt]+' ')
    return f_text



#===============================================================
# Main "Enitity_to_Entity_Extraction" functional start
#===============================================================
def params_segm_text(f_extracted_param,f_input_text):

    #--------------------------------------------
    # pick unique params name, save in list and 
    # sort it w.r.to length
    #--------------------------------------------
    all_params_list=[]
    for param_list in f_extracted_param.values():
        for param in param_list:
            if param not in all_params_list:
                all_params_list.append(param)
    len_func = lambda entity: len(entity)                   # sort it w.r.to length           
    all_params_list.sort(key=len_func,reverse=True)
    
    
    #--------------------------------------------
    # generate 'padtoken' dict and 
    # replace params name with this dict
    #--------------------------------------------
    pad_params_dict={}
    num=1
    for param in all_params_list:
        pad_params_dict[param]= f'padtoken{num}'
        num=num+1

    # replace params from input_text with this dict
    input_pad_text= f_input_text
    for param in all_params_list:
        input_pad_text= input_pad_text.replace(param, pad_params_dict[param])
 

    #--------------------------------------------
    # Now Apply 'Entity to Entity' Segmentation 
    #--------------------------------------------
    final_entity_text_segmentation={}                                      # dict: to save final result
    split_pad_text= input_pad_text.split()
    
    for entity_key,entity_value in pad_params_dict.items():
        if entity_key in f_input_text:
            start_index,end_index=None,None                                    # set initial values 'None'
            param_index= (split_pad_text.index(entity_value))                  # pick param_index from list          
            
            #--------------------------------------------      
            # pick start & end point/index
            start_index= param_index+1                                                     
            text_for_end_list= split_pad_text[start_index:]   
            for word in text_for_end_list: 
                if word in pad_params_dict.values():
                    end_index= split_pad_text.index(word)
                    break
             
            #--------------------------------------------
            # Segment the text using 'start_index' & 'end_index' 
            final_segmented_text= " ".join(split_pad_text[start_index:end_index])
    
            #--------------------------------------------
            # pick previous 2 words in 'years old' cases
            if entity_key in ['years old 1','year old 1','year age 1','years age 1']:           
                text_before= ' '.join(split_pad_text[:param_index])            # pick text from start to 'year old' param
                symbol_text= text_oprt_into_symbol(text_before)                # function call: convert operator text into operator
                symbol_text_list= symbol_text.split()                          # convert text into list
                text_extension_list=symbol_text_list[-2:]                      # pick last 2 values        
                text_extension= ' '.join(text_extension_list)
                final_segmented_text= text_extension +' '+ final_segmented_text
    
            #--------------------------------------------
            # replace 'padtoken_param' with actual params
            for key,value in pad_params_dict.items():                                                           
                if entity_value == value:
                    param= key
            
            #--------------------------------------------             
            # insert segmented entity text against entity in dict
            final_entity_text_segmentation[param]= final_segmented_text        
        
        else:                                                               # if 'param' name is not in text like {param1:depression screning 1,param2:depression screning 2},text='is not depression screning 1') 
            final_entity_text_segmentation[entity_key]=' ' 
    return final_entity_text_segmentation
    

#=============================================================================
'''
#input_text='show me the list of patients that are not 32 years old and all of them are male and suffering from copd from last 2 month and depression screening from 2022 all result must be in detail '
#input_text='cbc is ok lvef fg statin therapy bjhgj ckd and patient are 25 years old jcxcxcx'
#input_text= ' patient is ckd jlhghg hkgfkhjg and also suffered from depression for last 6 month is not between 455 year old  ghj  ggg and copd is ok'
input_text='the patient not contain 32 year old fg fg ddf  '

text_clean_result= text_clean(input_text)
initial_extracted_params= param_extraction(text_clean_result[1])
final_extracted_params= param_optimize(text_clean_result[1],initial_extracted_params)
result= entity_to_entity(final_extracted_params[1] , final_extracted_params[0])

print('\nparam=',final_extracted_params[1])
print(result)
'''
        