# -*- coding: utf-8 -*-
"""
    Module: Attribute_Name_Extraction
    Extract name from text and pass name w.r.to adhoc name
"""


from Modules.Attributes_Field.Attribute_Param_Mapping import replace_attribute_providername_dict,replace_attribute_practicename_dict

all_providername_list=list(replace_attribute_providername_dict.keys())
all_providername_list= sorted(all_providername_list,key=len,reverse=True)

all_practicename_list=list(replace_attribute_practicename_dict.keys())
all_practicename_list= sorted(all_practicename_list,key=len,reverse=True)


#======================================================
def extract_attribute_providername(f_text):
    f_text= ' '+f_text+' '
    extracted_name=''
    for name in all_providername_list:
        if (' '+name+' ') in f_text:
            extracted_name= name
            break
    if extracted_name:
        try:
            mapped_extracted_name= replace_attribute_providername_dict[extracted_name]
            return [mapped_extracted_name,None,'=']
        except:
            return [extracted_name,None,'=']
    else:
        return [None,None,None]
    

#======================================================
def extract_attribute_practicename(f_text):
    f_text= ' '+f_text+' '
    extracted_name=''
    for name in all_practicename_list:
        if (' '+name+' ') in f_text:
            extracted_name= name
            break
    if extracted_name:
        try:
            mapped_extracted_name= replace_attribute_practicename_dict[extracted_name]
            return [mapped_extracted_name,None,'=']
        except:
            return [extracted_name,None,'=']
    else:
        return [None,None,None]


#======================================================

'''
from Modules.For_All.Text_Preprocessing import text_clean
text='and the provide  name is Shahzaman Abbasi'
cleantext= text_clean(text)
result= extract_attribute_providername(cleantext)
print(result)

text='and the provide  name is acacia family practice 943480777  '
cleantext= text_clean(text)
result= extract_attribute_practicename(cleantext)
print(result) 
'''  


    
    
    
    
    
    
    
