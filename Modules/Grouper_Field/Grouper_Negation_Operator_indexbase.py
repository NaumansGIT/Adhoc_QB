# -*- coding: utf-8 -*-
"""
    Module: QB project
    Pick Negation Operator 
    (like '=','!=')
"""

import pandas as pd

'''
from Modules.Text_Preprocessing import text_clean
from Modules.Data_Params_Extraction import param_extraction
from Modules.Extracted_Params_Optimization import param_optimize
'''

#==============================================================
# create 'negation_dict' after apply preprocessing (like 'not suffering':not_suffering)
# and sort dict w.r.to length 
#==============================================================
df = pd.read_excel('other/Adhoc_QB_Other_Entities_31_10_2023.xlsx',sheet_name='All_Operators')

initial_negation_dict = df.set_index("Negation_text").to_dict().get('Negation_replace_text ')
negation_dict={}
for key,value in initial_negation_dict.items():
    key= " ".join(str(key).lower().split())
    value= " ".join(str(value).lower().split())
    negation_dict[key]= value

# Sort 'negation_dict' dict w.r.to lengthwise
sorted_negation_dict= dict(sorted(negation_dict.items(), key=lambda x: len(x[0]), reverse=True))

#==============================================================
# function start from here
#==============================================================
def negation_oprt(f_param,f_text,f_extracted_param):
    
    #-------------------------------------------
    # replace some text with 'negation_dict' values
    #-------------------------------------------
    updated_text= ' '+f_text+' '
    for key,value in sorted_negation_dict.items():
        updated_text= updated_text.replace(' '+key+' ',' '+value+' ')

    #-------------------------------------------
    # create 'param_token_dic' and 
    # replace all params with token from text
    #-------------------------------------------
    param_token_dict={}
    num=1
    for param_list in f_extracted_param.values():
        for param in param_list:
            param_token_dict[param]= f'padtoken{num}'                          # create 'param_token dict'
            updated_text= updated_text.replace(param,param_token_dict[param])  # replace all params with token
            num= num+1
    
    #-------------------------------------------
    # segment the text and pick required part 
    #-------------------------------------------
    if f_param in f_text:
        text_into_word = updated_text.split()                         # split the 'token base text'
        param_token = param_token_dict[f_param]                       # pick the 'f_param' token from 'param_token_dict'
        param_index = text_into_word.index(param_token)
        
        target_index=3                                                # number of words consider of negation decision
        final_operator='='                                            # set default 'final_operator' value '='
        for num in range(param_index, -1, -1):
            text_word= text_into_word[num]                            # pick text_token w.r.to index
            if (not text_word.isdigit()) and (text_word not in param_token_dict.values()):            # check token in 'param_token_dict'
                if text_word in sorted_negation_dict.values():
                    final_operator='!='
                target_index= target_index-1
            if target_index==0:
                break
            
        #-------------------------------------------
        # replace paraam_token with actual param name 
        # (retrive 'value' against 'key' from dict)
        #-------------------------------------------
        final_param = [key for key, value in param_token_dict.items() if value == param_token]
        final_param= final_param[0]                                   # result saved in list,so get first index
    else:                                                             # if param is not in text
        final_param= f_param
        final_operator= '='
        

    result= [final_param,final_operator]
    return result
    


#=============================================================================
'''
#input_text= "show me the list of patients without hba1c value,less than -7.1 also their age is greater than or equals to 36 Gender is less than male."
#input_text= "list of patients that are not suffering from ckd copd and depression screening but with low thyroid and without hba1c value"
#param= 'hba1c'
#output= negation_oprt('ckd 1','the patient age 1 is not 55 and not suffer from ckd 1 and copd 1 depression 1 and a1c 1 is 5',{'Age': ['age 1'], 'Problem': ['ckd 1', 'depression 1', 'copd 1'], 'Results': ['a1c 1']})

input_text= 'All patients of age 50 with hypertension is not a pay female'
param= 'female 1'
dic= {'Age': ['female 1'], 'Procedure': ['depression screening 2']}
output= negation_oprt(param,input_text,dic)

print("\nfinal_result=",output)

'''
'''
input_text='All patients of age 50 contain hypertension and does not including a of diabetes Mellitus'
param= 'diabetes mellitus 1'
text_clean_result= text_clean(input_text)
initial_extracted_params= param_extraction(text_clean_result[1])
final_extracted_params= param_optimize(text_clean_result[1],initial_extracted_params)

result= negation_oprt(param , final_extracted_params[0],final_extracted_params[1])
print(result)
'''




