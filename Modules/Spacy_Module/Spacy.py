# -*- coding: utf-8 -*-
"""
    Module: Spacy
    Extract all names from text and return only one name
    that is near to param
"""

import spacy
import pandas as pd
from Modules.For_All.Adhoc_String_Operator import extract_string_oprt


# Load the large English language model
nlp = spacy.load("en_core_web_lg")

#-----------------------------------------------------------------
# create custome 'Name_Distionary_list' for NER  
df_overall = pd.read_excel('Modules\Spacy_Module\spacy_custom_data.xlsx',sheet_name='Data')
name_list= df_overall['NER_Name']

custom_ner_name = []
for word in name_list:
    word= ' '.join(str(word).lower().split())
    custom_ner_name.append({"label": "PERSON", "pattern": word})
ruler = nlp.add_pipe("entity_ruler")
ruler.add_patterns(custom_ner_name)


#-----------------------------------------------------------------
def remove_stopwords(f_text):
    final_text= []
    stopword_list= ['dr','mr','mrs','miss','sir','madam']
    f_text_list= f_text.split()
    for word in f_text_list:
        if word not in stopword_list:
            final_text.append(word)
    final_text= ' '.join(final_text)
    return final_text


#===============================================================
# Main Function: Name_Extraction
#===============================================================
def name_extraction(f_text_wo_pad,f_text_with_pad,f_param):
    #f_text_wo_pad= remove_stopwords(f_text_wo_pad)                      # remove stopwords (like 'sir,'madam')

    final_result={'name':None,'operator':None}                          # set output_dict
    doc = nlp(f_text_wo_pad) 
    #========================================================
    # extract all names from text using Spacy
    extracted_name_list=[]                            
    for ent in doc.ents:
        if ent.label_=='PERSON':
            extracted_name= ' '.join((ent.text).split())            # remove extra spaces
            extracted_name_list.append(extracted_name)

    
    #-----------------------------------------------
    # replace param with 'paramtoken'
    f_text_with_pad= ' '+f_text_with_pad+' '
    f_text_with_pad= f_text_with_pad.replace(' '+f_param+' ', ' paramtoken ')
    param_index= f_text_with_pad.find('paramtoken')
    segmented_text= ' '+f_text_with_pad[param_index:]+' '           # segment the input text w.r.to 'param'
    
    #-----------------------------------------------
    if not extracted_name_list:                                     # condition: if 'name_list' is 'Empty'
        final_result['name']= None

    elif extracted_name_list:                                       # condition: name_list is 'not empty '
        #-----------------------------------------------
        # if (len=1) only one name pick from text 
        if len(extracted_name_list) ==1:                           
            final_result['name']= extracted_name_list[0]
            
        else:
            #-----------------------------------------------
            # if (len>1) then,calculate the distance between param and each name and pick smallst distance 
            name_with_index={}
            for name in extracted_name_list:
                name_index= segmented_text.find(' '+name+' ')               # find name from 'segmented text'
                if name_index != -1:             
                    name_with_index[name]= name_index
            
            #-----------------------------------------------
            # find the name with the smallest value/distance
            try:
                extracted_name = min(name_with_index, key=lambda k: name_with_index[k])
                extracted_name = ' '.join(extracted_name.split())
            except:
                extracted_name= None
            final_result['name']= extracted_name
                
    #--------------------------------------------------------------
    # find 'operator' using 'extract_string_oprt' module 
    if final_result['name']:                                        # if name is not 'None'
        segmented_text= ' '+segmented_text+' '
        name_index= segmented_text.find(' '+final_result['name']+' ')
        segmented_text= segmented_text[:name_index]
        operator= extract_string_oprt(segmented_text)
        final_result['operator']= operator
    return final_result




#===============================================================
# Main Function: Name_Extraction
#===============================================================
def full_name_extraction(f_text,f_param):
    f_text= remove_stopwords(f_text)                                         # remove stopwords (like 'sir,'madam')
    final_result={'firstname':None,'lastname':None}                          # set output_dict
    doc = nlp(f_text)    
     
    #-----------------------------------------------
    # condition: if 'first' & 'last name' is not mention in text       
    if ('First Name' or 'Last Name') not in f_param.keys():        
        extracted_name_list=[]                            
        for ent in doc.ents:
            if ent.label_=='PERSON':
                extracted_name= ' '.join((ent.text).split())            # remove extra spaces
                extracted_name_list.append(extracted_name)                
                name_text_list= extracted_name_list[0].split()
                
                if len(name_text_list)==1:
                    final_result['firstname']= name_text_list[0]
                elif len(name_text_list)>1:
                    final_result['firstname']= name_text_list[0]
                    final_result['lastname']= name_text_list[1]
    return final_result

    
    
    
    

#===============================================================
#===============================================================
'''
text1 = " Admitting Providers name is not john and last name is robert "
text2= " Admitting Providers A1 name is john and last name A1 is robert "

#text1='patients with snf cost below 2000 in 2023 and appointment is created by John and also'
#text2='patients with snf A1 cost below 2000 in 2023 and appointment is created by A1 John and also'

param='Admitting Providers A1'
result= name_extraction(text1,text2,param)
print('\n',result)
'''

'''
text = "care provider is sir jhon smith and is in active state"
param={}
result= full_name_extraction(text,param)
print('\n',result)
'''



