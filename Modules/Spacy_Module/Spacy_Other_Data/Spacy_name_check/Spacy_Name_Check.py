# -*- coding: utf-8 -*-
"""
    Python Script: Use to check 'name_extraction' through spacy 
"""

import spacy
import pandas as pd


# Load the large English language model
nlp = spacy.load("en_core_web_lg")

'''
#----------------------------------------------
# create custome 'Name_Distionary_list' for NER  
df_overall = pd.read_excel('Spacy_Name_Cases.xlsx')
name_list= df_overall['Names']

custom_ner_name = []
for word in name_list:
    word= ' '.join(word.lower().split())
    custom_ner_name.append({"label": "PERSON", "pattern": word})
ruler = nlp.add_pipe("entity_ruler")
ruler.add_patterns(custom_ner_name)
'''

#----------------------------------------------
def name_extraction(f_text):
    f_text= ' '+f_text+' '
    doc = nlp(f_text)    
    extracted_name_list=[]                            
    for ent in doc.ents:
        if ent.label_=='PERSON':
            extracted_name_list.append(ent.text)
    return extracted_name_list

#----------------------------------------------
df = pd.read_excel('Spacy_Name_Cases.xlsx')
df['SpacyResult'] = ""   

# Iterate through each row of 'df'
for index, row in df.iterrows():
    text = ' '.join(row['Text'].split())  
    result= name_extraction(text)
    df.at[index, 'SpacyResult'] = result

#----------------------------------------------
df.to_excel('Spacy_Name_Result.xlsx', index=False)
print('\n>>>>>> Task: Completed')


