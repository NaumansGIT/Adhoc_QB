# -*- coding: utf-8 -*-
"""
    Module: For QB Project
    For text preprocessing (clean text)
"""

#import nltk
import re 
import contractions


word_replace_dict={',':' ','/':'_','y of age ':' year of age '}
number_words_dict = {          
    'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5',
    'six': '6', 'seven': '7', 'eight': '8', 'nine': '9', 'ten': '10',
    'eleven': '11', 'twelve': '12', 'thirteen': '13', 'fourteen': '14', 'fifteen': '15',
    'sixteen': '16', 'seventeen': '17', 'eighteen': '18', 'nineteen': '19', 'twenty': '20',
    'twenty one': '21', 'twenty two': '22', 'twenty three': '23', 'twenty four': '24', 'twenty five': '25',
    'twenty six': '26', 'twenty seven': '27', 'twenty eight': '28', 'twenty nine': '29', 'thirty': '30',
    'thirty one': '31', 'thirty two': '32', 'thirty three': '33', 'thirty four': '34', 'thirty five': '35',
    'thirty six': '36', 'thirty seven': '37', 'thirty eight': '38', 'thirty nine': '39', 'forty': '40',
    'forty one': '41', 'forty two': '42', 'forty three': '43', 'forty four': '44', 'forty five': '45',
    'forty six': '46', 'forty seven': '47', 'forty eight': '48', 'forty nine': '49', 'fifty': '50',
    'fifty one': '51', 'fifty two': '52', 'fifty three': '53', 'fifty four': '54', 'fifty five': '55',
    'fifty six': '56', 'fifty seven': '57', 'fifty eight': '58', 'fifty nine': '59', 'sixty': '60',
    'sixty one': '61', 'sixty two': '62', 'sixty three': '63', 'sixty four': '64', 'sixty five': '65',
    'sixty six': '66', 'sixty seven': '67', 'sixty eight': '68', 'sixty nine': '69', 'seventy': '70',
    'seventy one': '71', 'seventy two': '72', 'seventy three': '73', 'seventy four': '74', 'seventy five': '75',
    'seventy six': '76', 'seventy seven': '77', 'seventy eight': '78', 'seventy nine': '79', 'eighty': '80',
    'eighty one': '81', 'eighty two': '82', 'eighty three': '83', 'eighty four': '84', 'eighty five': '85',
    'eighty six': '86', 'eighty seven': '87', 'eighty eight': '88', 'eighty nine': '89', 'ninety': '90',
    'ninety one': '91', 'ninety two': '92', 'ninety three': '93', 'ninety four': '94', 'ninety five': '95',
    'ninety six': '96', 'ninety seven': '97', 'ninety eight': '98', 'ninety nine': '99', 'hundred': '100',

    '1st': '1', '2nd': '2', '3rd': '3', '4th': '4', '5th': '5',
    '6th': '6', '7th': '7', '8th': '8', '9th': '9', '10th': '10',
    '11th': '11', '12th': '12', '13th': '13', '14th': '14', '15th': '15',
    '16th': '16', '17th': '17', '18th': '18', '19th': '19', '20th': '20',
    '21st': '21', '22nd': '22', '23rd': '23', '24th': '24', '25th': '25',
    '26th': '26', '27th': '27', '28th': '28', '29th': '29', '30th': '30',
    '31st': '31', '32nd': '32', '33rd': '33', '34th': '34', '35th': '35',
    '36th': '36', '37th': '37', '38th': '38', '39th': '39', '40th': '40',
    '41st': '41', '42nd': '42', '43rd': '43', '44th': '44', '45th': '45',
    '46th': '46', '47th': '47', '48th': '48', '49th': '49', '50th': '50',
    '51st': '51', '52nd': '52', '53rd': '53', '54th': '54', '55th': '55',
    '56th': '56', '57th': '57', '58th': '58', '59th': '59', '60th': '60',
    '61st': '61', '62nd': '62', '63rd': '63', '64th': '64', '65th': '65',
    '66th': '66', '67th': '67', '68th': '68', '69th': '69', '70th': '70',
    '71st': '71', '72nd': '72', '73rd': '73', '74th': '74', '75th': '75',
    '76th': '76', '77th': '77', '78th': '78', '79th': '79', '80th': '80',
    '81st': '81', '82nd': '82', '83rd': '83', '84th': '84', '85th': '85',
    '86th': '86', '87th': '87', '88th': '88', '89th': '89', '90th': '90',
    '91st': '91', '92nd': '92', '93rd': '93', '94th': '94', '95th': '95',
    '96th': '96', '97th': '97', '98th': '98', '99th': '99', '100th': '100'}



#======================================================================
# Main code
#======================================================================
def text_clean(f_text):
    f_text=' '+str(f_text)+' '    
    for word_k,word_v in word_replace_dict.items():                           # replace words from text w.r.to 'word_replace_dict'
        f_text= f_text.replace(word_k,word_v)    
    f_text= contractions.fix(f_text.lower())                                  # loweer case + Expand text using 'contractions' (like i'm -> i am)
    clean_text = re.sub(r'[^\w\s\d\.\-\$\@]',' ', f_text)                     # Remove punctuation except these mention entities

    for word_k,word_v in number_words_dict.items():                           # replace words from text w.r.to 'word_replace_dict'
        clean_text= clean_text.replace(' '+word_k+' ',' '+word_v+' ')
    tokenize_text = clean_text.split()                            # tokenize text with 'space' (NTK)        
    
    final_word_list=[]
    for word in tokenize_text:
        final_word_list.append(word.rstrip('.'))
    clean_text= " ".join(final_word_list)                                        

    return clean_text

    
#======================================================================
'''
text='show me all patient that suffering for hba1c ckd and copd. and with email haroonkhan54000@gmail.com and value is -1.2.'
result= text_clean(text)
print('\n',result)
'''

