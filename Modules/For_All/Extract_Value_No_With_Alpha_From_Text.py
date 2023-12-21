
# -*- coding: utf-8 -*-
"""
    Module: QB project
    Pick/Extract values that contain number and alphabet 
"""

import re




#*********************************************************
# Main function start: from here
#*********************************************************
def extract_alphanumeric(f_text):
    pattern = re.compile(r'\b[a-zA-Z0-9]+\b')
    matches = pattern.findall(f_text)
    return matches
    




#================================================================================
#================================================================================


from Modules.For_All.Text_Preprocessing import text_clean

#input_text='patient cost is between 30 to -2.0'
input_text='scriber id is FX123FF55 '
clean_text= text_clean(input_text)
result= extract_alphanumeric(input_text)

print('\n >> ',result)


