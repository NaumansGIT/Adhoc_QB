
# -*- coding: utf-8 -*-
"""
    Module: QB project
    Pick/Extract values and operators from text according to params
    Final Response is in list ['value1','value2','operator']
"""

import re
from Modules.For_All.All_Module_Dictionaries import operator_dict,unique_operator_list,all_oprt_len_dict



#*********************************************************
# function: To extract 'values' & 'operator from text'
#*********************************************************
def extract_values_operator(f_text):
    final_result=[]                                                            # save result in list: ['value1','value2','oprt']
    operator_final=''
    input_text= ' '+ f_text +' '                                               # add spaces
    if not input_text:                                                         # check if input_text is 'empty', then return 'None'
        return [None, None, None]

    else:
        #======================================
        # Approach1: Pick data through regex
        pattern_list=[r"\b\s+?(-?\d+(?:\.\d+)?)\s+(?:(?:to|and)\s+)?(-?\d+(?:\.\d+)?)\b"]     # for case " (-)20(.) to/and/'' (-)40(.)"        
        for pattern in pattern_list:
            ptrn_match = re.findall(pattern, input_text)
            ptrn_match = [(num) for match in ptrn_match for num in match]      # convert result from "[('2020', '2022')]" to "[2022, 2023]"
            if ptrn_match:
                num_list= [float(ptrn_match[0]),float(ptrn_match[1])]
                value1= float(min(num_list))
                value2= float(max(num_list))

                
                #------------------------
                # pick opertor: from text
                ptrn_match = re.search(pattern, input_text)                    # use regex to extract 'pattern_match_text'
                ptrn_text= ptrn_match.group()                                  # get text
                ptrn_text= ' '.join(ptrn_text.split())                         # remove extra spaces from text
                ptrn_text_index= input_text.find(' '+ptrn_text+' ')            # find the index of 'pattern_match_text'
                segmented_text=input_text[:ptrn_text_index] +' '               # segment the 'input text' according to index
                operator= 'between'                                            # set default operator
                for word in ['not','between','from']:
                    if (word=='not') and (' '+word+' ') in segmented_text:
                        operator='not between'
                        break
                    elif (word in ['between','from']) and (' '+word+' ') in segmented_text:
                        operator='between'
                        break
                final_result.extend([value1,value2,operator])
                return final_result
            
        
        #======================================
        # if no data pick through regex, then 
        # 'Approach2': Pick/Extract values
        #--------------------------------------
        pattrn= r'-?\d+\.\d+\s|-?\d+\s'
        numeric_values = re.findall(pattrn, input_text)                        # pick all numeric values ('.'&'-' are optional)            

        if len(numeric_values)==1:                                             # set values w.r.to 'numeric_values' length
            value1= ' '.join(numeric_values[0].split())
            value2= None
            final_result.extend([float(value1),value2])
        elif len(numeric_values)>1:
            value1= ' '.join(numeric_values[0].split())
            value2= ' '.join(numeric_values[1].split())
            final_result.extend([float(value1),float(value2)])
        else:
            value1= None
            value2= None
            final_result.extend([value1,value2])
        
        
        #--------------------------------
        # condition: if value1 is empty
        #--------------------------------
        if not value1:
            return [None,None,None]
            
        #-----------------------------------------
        # pick operator: if 'value1' is not empty
        #-----------------------------------------
        if value1:
            for oprt_list in all_oprt_len_dict.values():                       # replace operators with symbols   
                for oprt in oprt_list:
                    if oprt in input_text:
                        input_text= input_text.replace((' '+oprt+' '), ' '+operator_dict[oprt]+' ')
            
            
            input_text_list = input_text.split()                               # split text into list
            value1_index= input_text_list.index(value1)            
            
            for num in range(value1_index, -1, -1):                            # back-loop: get first operator before 'value1'
                if input_text_list[num] in unique_operator_list:
                    operator_final= input_text_list[num]
                    break
            if not operator_final:                                             # in case no operator extract: set default: '='
                operator_final= '='
            operator_final= operator_final.replace('_',' ')
            final_result.append(operator_final)
        return final_result
        



#*********************************************************
# Main function start: from here
#*********************************************************
def value_operator(f_text):
    value_oprt_result= extract_values_operator(f_text)                         # get values and operator using above function
    num1= value_oprt_result[0]
    num2= value_oprt_result[1]
    oprt= value_oprt_result[2]
    if oprt not in ['between','not between']:                                  # Return two values only for 'between' & 'not between' 
        num2= None    
    if oprt == 'not between':                                                  # replace "not between" with "notBetween"
        oprt= 'notBetween'
    return [num1,num2,oprt]
    




#================================================================================
#================================================================================

'''
from Modules.For_All.Text_Preprocessing import text_clean

#input_text='patient cost is between 30 to -2.0'
input_text='value between -5 and 10 '
clean_text= text_clean(input_text)
result= value_operator(clean_text)
print('\n >> ',result)
'''


