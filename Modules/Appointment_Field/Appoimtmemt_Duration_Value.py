# -*- coding: utf-8 -*-
"""
    Module: QB project
    Pick/Extract value & operators for Appointment Duration
    Return value in min (hr->min)
"""


from Modules.For_All.Extract_Value_Operator_From_Text import value_operator

word_check_list=['h','hr','hour','hours']

#==============================================================
# function start:
#==============================================================
def duration_value(f_text):
    f_text= ' '+f_text+' '
    fina_result= []
    check_status=None
    
    initial_value_result= value_operator(' '+f_text+' ')                # get result through 'value module'
    for word in word_check_list:
        word= ' '+word+' '
        word_index= f_text.find(word)
        if word_index != -1:
            check_status=True
            
    if check_status ==True:
        value1= initial_value_result[0]
        value2= initial_value_result[1]
        oprt=   initial_value_result[2]
        if value1:
            value1= value1*60
        if value2:
            value2= value2*60
        fina_result.extend([value1,value2,oprt])
        
    else:
        fina_result= initial_value_result
        
    return fina_result
        
        
    
    
#=============================================================================

'''
from Modules.For_All.Text_Preprocessing import text_clean
text='Duration is 1 min'
text= text_clean(text)
result= duration_value(text)
print('\n>>',result)
'''

