# -*- coding: utf-8 -*-

"""
    Module: QB project
    Extract years,months and days from text, and generate date response for Adhoc
    'Function1 output'= dict:{'year':[1,2],'month':[1,2],'day':[1,2]}
    'Function2 output'= 2022-08-07T05:00:00.000Z'

"""

import re
import calendar
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta

from Modules.For_All.All_Module_Dictionaries import date_operator_dict,ld_month_pad_dict



#==============================================================================
# all 'dates' cases/pattern
all_pattern_dict={
    'years_case_1_1':[ r'\blast\s+(\d+)\s+(?:year|years)\b',                   # case: "last 6 year"
                       r'\bprevious\s+(\d+)\s+(?:year|years)\b',               # case: "previous 3 year"
                       r'\bpast\s+(\d+)\s+(?:year|years)\b',                   # case: "past 2 year"
                     ],
    'years_case_1_2':[ r'\b(\d+)\s+(?:year ago|years ago)\b',                  # case: "6 year ago"                                         
                       r'\b(\d+)\s+(?:year back|years back)\b',                # case: "6 year back"                                         
                     ],
    'month_case_1_1':[ r'\blast\s+(\d+)\s+(?:month|months)\b',                 # case: "last 6 month"
                       r'\bprevious\s+(\d+)\s+(?:month|months)\b',             # case: "previous 3 months"
                       r'\bpast\s+(\d+)\s+(?:month|months)\b',                 # case: "past 2 months"
                     ],
    'month_case_1_2':[ r'\b(\d+)\s+(?:month ago|months ago)\b',                # case: "6 months ago"    
                       r'\b(\d+)\s+(?:month back|months back)\b',              # case: "6 months back"    
                     ],
    'days_case_1_1': [ r'\blast\s+(\d+)\s+(?:day|days)\b',                     # case: "last 6 day/days"
                      r'\bprevious\s+(\d+)\s+(?:day|days)\b',                  # case: "previous 3 day/days"
                      r'\bpast\s+(\d+)\s+(?:day|days)\b',                      # case: "past 2 day/days"
                     ],
    'days_case_1_2': [ r'\b(\d+)\s+(?:day ago|days ago)\b',                    # case: "6 day/days ago"    
                       r'\b(\d+)\s+(?:day back|days back)\b',                  # case: "6 day/days ago"    
                     ],

    'years_case_2_1': [r'not between (\d{4})(?: (?:to|and))? (\d{4})'],        # for case: 'not between 2020 to 2021'/'not between 2020 and 2021'/'not between 2020 2021'             
    'years_case_2_2': [r'between (\d{4})(?: (?:to|and))? (\d{4})'],            # for case: 'between 2020 to 2021'/'between 2020 and 2021'/'between 2020 2021'
    'years_case_2':[r"\b(?:from\s+)?(\d{4})\s+(?:(?:to|and)\s+)?(\d{4})\b"],   # case: "(from) 2020 to/and/'' 2022"  

    'month_case_2': [r"\bfrom\s+Month_(\d{2})\s+(\d{4})\s+to\s+Month_(\d{2})\s+(\d{4})\b"],                     # case: "from Month_01 2010 to Month_05 2020"  
    'month_case_2_1': [r'\bnot\s+between\s+Month_(\d{2})\s+(\d{4})\s+(?:to|and)?\s+Month_(\d{2})\s+(\d{4})\b'], # case: "not between Month_01 2020 to Month_05 2022"
    'month_case_2_2': [r'\bbetween\s+Month_(\d{2})\s+(\d{4})\s+(?:to|and)?\s+Month_(\d{2})\s+(\d{4})\b'],       # case: "not between Month_01 2020 to Month_05 2022"
    
    'month_case_3': [r'\bfrom\s+Month_(\d{2}|\d)\s+to\s+Month_(\d{2})\s+(\d{4})\b'],                            # case: "from Month_1 to Month_02 2022"
    'month_case_3_1':[r'\bnot\s+between\s+Month_(\d{2})\s+(?:(?:to|and)\s+)?Month_(\d{2})\s+(\d{4})\b'],        # for case: "not between Month_01 to Month_05 2022",
    'month_case_3_2':[r'\bbetween\s+Month_(\d{2})\s+(?:(?:to|and)\s+)?Month_(\d{2})\s+(\d{4})\b'],              # for case: "between Month_01 to Month_05 2022",
    
    
    'days_case_2':[r'from\s+(\d+)\s+Month_(\d{2})\s+(\d{4})\s+(?:to|and)?\s+(\d+)\s+Month_(\d{2})\s+(\d{4})'],  # case: "from 21 Month_02 2020 and/to 7 Month_12 2022" 
    'days_case_2_1':[r'from\s+(\d+)\s+Month_(\d{2})\s+(?:(?:to|and)\s+(\d+)\s+Month_(\d{2}))?\s+(\d{4})'],      # case: 'from 21 Month_02 to/and 7 Month_12 2022'
    'days_case_2_2':[r'\bnot\s+between\s+(\d+)\s+Month_(\d{2})\s+(?:(?:to|and)\s+(\d+)\s+Month_(\d{2}))?\s+(\d{4})'],  # case: 'not between 21 Month_02 to/and 7 Month_12 2022'
    'days_case_2_3':[r'\bbetween\s+(\d+)\s+Month_(\d{2})\s+(?:(?:to|and)\s+(\d+)\s+Month_(\d{2}))?\s+(\d{4})'],        # case: 'between 21 Month_02 to/and 7 Month_12 2022'
    'days_case_2_4':[r'not\s+between\s+(\d+)\s+Month_(\d{2})\s+(\d{4})\s+(?:(?:to|and)\s+(\d+)\s+Month_(\d{2})\s+(\d{4}))?'],# case: 'not between 21 Month_02 2020 to/and 7 Month_12 2022'
    'days_case_2_5':[r'between\s+(\d+)\s+Month_(\d{2})\s+(\d{4})\s+(?:(?:to|and)\s+(\d+)\s+Month_(\d{2})\s+(\d{4}))?'],# case: 'between 21 Month_02 2020 to/and 7 Month_12 2022'
    
    
    'current_case': [r'\b(?:this|current|present|existing)\s+(?:day|days|month|months|year|years|date|dates)\b'],  # case: "this/current/present/existing month/months/year/years"
    'past_case': [r'\b(?:last|previous|past)\s+(?:month|months|year|years)\b'],           # case: "last/previous/past month/months/year/years"
    'other_case_1':[r'\d+']                                                               # case: extract all number from input text
}



#******************************************************************************
# Start: 'date_operator' Function (code)
#******************************************************************************
def date_oprt(f_text,f_maininput):
    operator_list=['=','!=','>=','>','<=','<','contains','between','not_between']
    final_operator='='
    
    f_text= ' '+f_text+' '
    f_maininput= ' '+f_maininput+' '
    f_maininput= f_maininput.replace(' of ',' ')                              # remove 'of' from text
    
    #--------------------------------
    # replace 'month' with 'Month_01' from text using 'ld_month_dict'
    for k_month,v_number in ld_month_pad_dict.items():
        f_maininput= f_maininput.replace(' '+k_month+' ',' '+v_number+' ')
    
    
    f_maininput= f_maininput.replace(f_text,' datetoken ')                    # replace date/number with 'datetoken'
    for oprt_key,oprt_value in date_operator_dict.items():                    # replace operator 'text' with 'symbols'
        f_maininput= f_maininput.replace(' '+oprt_key+' ',' '+oprt_value+' ')
    
    f_maininput_list= f_maininput.split()                                     # split text into token/list
    date_index= f_maininput_list.index('datetoken')                           # find the index of 'datetoken'
    for num in range(date_index, -1, -1):                                     # loop: move backward from date 
        word= f_maininput_list[num]    
        if word in operator_list:                            # condition: check word is in 'operator list',stop loop
            final_operator= word
            break        
    return final_operator
    

    




#******************************************************************************
# Start: 'extract_date' Function (code)
#******************************************************************************
def extract_date(f_text,f_maininput):
    final_dict= {'year':'','month':'','day':'','operator':''}
    #print(f_text,'\n')
    current_date = datetime.now()                                            # get current date & time
    current_year = current_date.year                                         # Extract current 'year'
    current_month = current_date.month                                       # Extract current 'month'
    current_day = current_date.day                                           # Extract current 'year'
    
    
    #-----------------------------------------------------
    # run all above patterns one-by-one and if condition meet
    #-----------------------------------------------------    
    for ptrn_dict_key,ptrn_dict_value in all_pattern_dict.items():
        for pattern in ptrn_dict_value:
            ptrn_match = re.findall(pattern, f_text)                         # fetch the values from text through pattern one-by-one
            #print('\n',ptrn_dict_key,'>> Pattren:',pattern)
            #print('ptrn_match=',ptrn_match)
            
            #-----------------------------------------------------
            # for 'years_case_1_1' pattren  (like "last 6 year")
            #-----------------------------------------------------
            if ptrn_match and ptrn_dict_key=='years_case_1_1' :
                target= int(ptrn_match[0])                                   # pick number from result
                target_date = current_date - timedelta(days=target*365)      # calculate 'target_date' from 'current_date'
                year1,month1,day1= current_year,current_month,current_day    # set year/month/day values
                year2,month2,day2= target_date.year,target_date.month,target_date.day
                final_dict['year']= [year2,year1]                            
                final_dict['month']= [month2,month1]                         # insert result in 'final_dict'
                final_dict['day']= [day2,day1]
                final_dict['operator']= 'between'
                return final_dict


            #-----------------------------------------------------
            # for 'years_case_1_2' pattren  (like "6 year ago/back")
            #-----------------------------------------------------
            if ptrn_match and ptrn_dict_key=='years_case_1_2' :
                target= int(ptrn_match[0])                                   # pick number from result
                target_date = current_date - timedelta(days=target*365)      # calculate 'target_date' from 'current_date'
                year= target_date.year
                month1,month2= '01','12'
                day1,day2= '01','31'
                final_dict['year']= [year,year]                            
                final_dict['month']= [month1,month2]                         # insert result in 'final_dict'
                final_dict['day']= [day1,day2]
                final_dict['operator']= 'between'
                return final_dict
        
            
            #-----------------------------------------------------
            # for 'month_case_1_2' pattren (like " 6 months ago/back")
            #-----------------------------------------------------
            if ptrn_match and ptrn_dict_key=='month_case_1_2' :
                target= int(ptrn_match[0])                                   # pick number from result
                target_date = current_date - relativedelta(months=target)    # calculate 'target_date' from 'current_date'
                year,month= target_date.year,target_date.month
                day1= '01'
                day2 = calendar.monthrange(int(year), int(month))[1]  # find the no. of days using month
                final_dict['year']= [year,year]                            
                final_dict['month']= [month,month]                         # insert result in 'final_dict'
                final_dict['day']= [day1,day2]
                final_dict['operator']= 'between'
                return final_dict
            
            
            #-----------------------------------------------------
            # for 'month_case_1_1' pattren (like "last 6 month")
            #-----------------------------------------------------
            if ptrn_match and ptrn_dict_key=='month_case_1_1' :
                target= int(ptrn_match[0])                                   # pick number from result
                target_date = current_date - relativedelta(months=target)    # calculate 'target_date' from 'current_date'
                year1,month1,day1= current_year,current_month,current_day    # set year/month/day values
                year2,month2,day2= target_date.year,target_date.month,target_date.day
                final_dict['year']= [year2,year1]                            
                final_dict['month']= [month2,month1]                         # insert result in 'final_dict'
                final_dict['day']= [day2,day1]
                final_dict['operator']= 'between'
                return final_dict
            
        
            #-----------------------------------------------------
            # for 'days_case_1_1' pattren (like "last 6 days")
            #-----------------------------------------------------
            if ptrn_match and ptrn_dict_key=='days_case_1_1' :
                target= int(ptrn_match[0])                                   # pick number from result
                target_date = current_date - timedelta(days=target)          # calculate 'target_date' from 'current_date'
                year1,month1,day1= current_year,current_month,current_day    # set year/month/day values
                year2,month2,day2= target_date.year,target_date.month,target_date.day
                final_dict['year']= [year2,year1]                            
                final_dict['month']= [month2,month1]                         # insert result in 'final_dict'
                final_dict['day']= [day2,day1]
                final_dict['operator']= 'between'
                return final_dict
            
            
            #-----------------------------------------------------
            # for 'days_case_1_2' pattren (like "last 10 days")
            #-----------------------------------------------------
            if ptrn_match and ptrn_dict_key=='days_case_1_2' :
                target= int(ptrn_match[0])                                   # pick number from result
                target_date = current_date - timedelta(days=target)          # calculate 'target_date' from 'current_date'
                year,month,day= target_date.year,target_date.month,str(target_date.day)
                final_dict['year']= [year]                            
                final_dict['month']= [month]                         # insert result in 'final_dict'
                final_dict['day']= [day]
                final_dict['operator']= '='
                return final_dict
            
            
            
            #-----------------------------------------------------
            # for 'years_case_2' pattren (like "from 2020 to 2022")
            #-----------------------------------------------------
            if ptrn_match and ptrn_dict_key=='years_case_2' :
                ptrn_match = [(num) for match in ptrn_match for num in match] # convert result from "[('2020', '2022')]" to "[2022, 2023]"
                year1 = min(int(number) for number in ptrn_match)             # pick smallest number from list
                year2 = max(int(number) for number in ptrn_match)             # pick smallest number from list
                if year2 >= current_year:                                     # check 'number2':
                    year2,month2,day2= current_year,current_month,current_day
                else:
                   year2,month2,day2 = year2,'12','31'
                final_dict['year']= [year1, year2] # insert result in 'final_dict'
                final_dict['month']= ['01',month2]
                final_dict['day']= ['01', day2]
                final_dict['operator']= 'between'
                return final_dict
            
            
            #-----------------------------------------------------
            # for 'years_case_2_1' pattren (like "not between 2020 and 2022")
            #-----------------------------------------------------
            if ptrn_match and ptrn_dict_key=='years_case_2_1' :
                ptrn_match = [(num) for match in ptrn_match for num in match] # convert result from "[('2020', '2022')]" to "[2022, 2023]"
                year1 = min(int(number) for number in ptrn_match)             # pick smallest number from list
                year2 = max(int(number) for number in ptrn_match)             # pick smallest number from list
                if year2 >= current_year:                                     # check 'number2':
                    year2,month2,day2= current_year,current_month,current_day
                else:
                   year2,month2,day2 = year2,'12','31'
                final_dict['year']= [year1, year2]                            # insert result in 'final_dict'
                final_dict['month']= ['01',month2]
                final_dict['day']= ['01', day2]
                final_dict['operator']= 'notBetween'
                return final_dict
            
            
            #-----------------------------------------------------
            # for 'years_case_2_2' pattren (like "between 2020 and 2022")
            #-----------------------------------------------------
            if ptrn_match and ptrn_dict_key=='years_case_2_2' :
                ptrn_match = [(num) for match in ptrn_match for num in match] # convert result from "[('2020', '2022')]" to "[2022, 2023]"
                year1 = min(int(number) for number in ptrn_match)             # pick smallest number from list
                year2 = max(int(number) for number in ptrn_match)             # pick smallest number from list
                if year2 >= current_year:                                     # check 'number2':
                    year2,month2,day2= current_year,current_month,current_day
                else:
                   year2,month2,day2 = year2,'12','31'
                final_dict['year']= [year1, year2]                            # insert result in 'final_dict'
                final_dict['month']= ['01',month2]
                final_dict['day']= ['01', day2]
                final_dict['operator']= 'between'
                return final_dict
            
            
            #-------------------------------------------------------------------
            # for 'month_case_2' pattren (like "from Month_01 2010 to Month_05 2020")
            #-------------------------------------------------------------------
            if ptrn_match and ptrn_dict_key=='month_case_2' :
                ptrn_match = [(num) for match in ptrn_match for num in match] # convert result from "[('01', '2010', '05', '2020')]" to "['01', '2010', '05', '2020']"                
                year_list=[ptrn_match[1],ptrn_match[3]]
                month_list=[ptrn_match[0],ptrn_match[2]]
                year1 = min(int(number) for number in year_list)                # pick smallest number from list
                year2 = max(int(number) for number in year_list)                # pick smallest number from list
                month1= month_list[0]                                           # pick first index
                day1= '01'
                if year2 > current_year:                                        # check condition and set values
                    year2,month2,day2= current_year,current_month,current_day
                else:
                   day2 = calendar.monthrange(int(year2), int(month_list[1]))[1]  # find the no. of days using month
                   year2,month2,day2 = year2,month_list[1],day2
                final_dict['year']= [year1, year2]                              # insert result in 'final_dict'
                final_dict['month']= [month1,month2]
                final_dict['day']= [day1, day2]
                final_dict['operator']= 'between'
                return final_dict
            
            
            #-------------------------------------------------------------------
            # for 'month_case_2_1' pattren (like not between Month_01 2020 to Month_05 2022")
            #-------------------------------------------------------------------
            if ptrn_match and ptrn_dict_key=='month_case_2_1' :
                ptrn_match = [(num) for match in ptrn_match for num in match]   # convert result from "[('01', '2010', '05', '2020')]" to "['01', '2010', '05', '2020']"                
                year_list=[ptrn_match[1],ptrn_match[3]]
                month_list=[ptrn_match[0],ptrn_match[2]]
                year1 = min(int(number) for number in year_list)                # pick smallest number from list
                year2 = max(int(number) for number in year_list)                # pick smallest number from list
                month1= month_list[0]                                           # pick first index
                day1= '01'
                if year2 > current_year:                                        # check condition and set values
                    year2,month2,day2= current_year,current_month,current_day
                else:
                   day2 = calendar.monthrange(int(year2), int(month_list[1]))[1]  # find the no. of days using month
                   year2,month2,day2 = year2,month_list[1],day2
                final_dict['year']= [year1, year2]                              # insert result in 'final_dict'
                final_dict['month']= [month1,month2]
                final_dict['day']= [day1, day2]
                final_dict['operator']= 'notBetween'
                return final_dict
            
                        
            #-------------------------------------------------------------------
            # for 'month_case_2_2' pattren (like "between Month_01 2020 to Month_05 2022)
            #-------------------------------------------------------------------
            if ptrn_match and ptrn_dict_key=='month_case_2_2' :
                ptrn_match = [(num) for match in ptrn_match for num in match] # convert result from "[('01', '2010', '05', '2020')]" to "['01', '2010', '05', '2020']"                
                year_list=[ptrn_match[1],ptrn_match[3]]
                month_list=[ptrn_match[0],ptrn_match[2]]
                year1 = min(int(number) for number in year_list)             # pick smallest number from list
                year2 = max(int(number) for number in year_list)             # pick smallest number from list
                month1= month_list[0]                                        # pick first index
                day1= '01'
                if year2 > current_year:                                     # check condition and set values
                    year2,month2,day2= current_year,current_month,current_day
                else:
                   day2 = calendar.monthrange(int(year2), int(month_list[1]))[1]  # find the no. of days using month
                   year2,month2,day2 = year2,month_list[1],day2
                final_dict['year']= [year1, year2]                           # insert result in 'final_dict'
                final_dict['month']= [month1,month2]
                final_dict['day']= [day1, day2]
                final_dict['operator']= 'between'
                return final_dict
            
            
            #-------------------------------------------------------------------
            # for 'month_case_3' pattren (like "from Month_1 to Month_02 2022")
            #-------------------------------------------------------------------
            if ptrn_match and ptrn_dict_key=='month_case_3' :
                ptrn_match = [num for match in ptrn_match for num in match] # convert result from "[('01', '2010', '05', '2020')]" to "['01', '2010', '05', '2020']"                
                year1,year2= ptrn_match[2],ptrn_match[2]
                month_list= int(ptrn_match[0]),int(ptrn_match[1])            # set years values
                month1,month2= min(month_list),max(month_list)               # set years values
                day1= 1                                                      # set start day=1
                day2= calendar.monthrange(int(year1), int(month2))[1]        # find the no. of days using month
                final_dict['year']= [year1, year2]                           # insert result in 'final_dict'
                final_dict['month']= [month1,month2]
                final_dict['day']= [day1, day2]
                final_dict['operator']= 'between'
                return final_dict
            
            
            #-------------------------------------------------------------------
            # for 'month_case_3_1' pattren (like "not between Month_01 to Month_05 2022")
            #-------------------------------------------------------------------
            if ptrn_match and ptrn_dict_key=='month_case_3_1' :
                ptrn_match = [num for match in ptrn_match for num in match] # convert result from "[('01', '2010', '05', '2020')]" to "['01', '2010', '05', '2020']"                
                year1= ptrn_match[2]
                if int(year1) > current_year:
                    year1,year2= current_year,current_year
                else:
                    year1,year2= ptrn_match[2],ptrn_match[2]
                month_list= int(ptrn_match[0]),int(ptrn_match[1])            # set years values
                month1,month2= min(month_list),max(month_list)               # set years values
                day1= 1                                                      # set start day=1
                day2= calendar.monthrange(int(year1), int(month2))[1]        # find the no. of days using month
                final_dict['year']= [year1, year2]                           # insert result in 'final_dict'
                final_dict['month']= [month1,month2]
                final_dict['day']= [day1, day2]
                final_dict['operator']= 'notBetween'
                return final_dict
            
            
            #-------------------------------------------------------------------
            # for 'month_case_3_2' pattren (like "between Month_01 to Month_05 2022")
            #-------------------------------------------------------------------
            if ptrn_match and ptrn_dict_key=='month_case_3_2' :
                ptrn_match = [num for match in ptrn_match for num in match] # convert result from "[('01', '2010', '05', '2020')]" to "['01', '2010', '05', '2020']"                
                year1= ptrn_match[2]
                if int(year1) > current_year:
                    year1,year2= current_year,current_year
                else:
                    year1,year2= ptrn_match[2],ptrn_match[2]
                month_list= int(ptrn_match[0]),int(ptrn_match[1])            # set years values
                month1,month2= min(month_list),max(month_list)               # set years values
                day1= 1                                                      # set start day=1
                day2= calendar.monthrange(int(year1), int(month2))[1]        # find the no. of days using month
                final_dict['year']= [year1, year2]                           # insert result in 'final_dict'
                final_dict['month']= [month1,month2]
                final_dict['day']= [day1, day2]
                final_dict['operator']= 'between'
                return final_dict
            
            
            #-------------------------------------------------------------------
            # for 'days_case_2_1' pattren (like "from 21 Month_02 to 7 Month_12 2022")
            #-------------------------------------------------------------------
            if ptrn_match and ptrn_dict_key=='days_case_2_1' :
                ptrn_match = [num for match in ptrn_match for num in match] # convert result from "[('01', '2010', '05', '2020')]" to "['01', '2010', '05', '2020']"                
                year1= ptrn_match[4]
                if int(year1) > current_year:
                    year1,year2= current_year,current_year
                else:
                    year1,year2= ptrn_match[4],ptrn_match[4]                                            # set start day=1
                day1,day2= int(ptrn_match[0]),int(ptrn_match[2]) 
                month1,month2= int(ptrn_match[1]),int(ptrn_match[3])
                final_dict['year']= [year1, year2]                           # insert result in 'final_dict'
                final_dict['month']= [month1,month2]
                final_dict['day']= [day1, day2]
                final_dict['operator']= 'between'
                return final_dict
            
            
            #-------------------------------------------------------------------
            # for 'days_case_2' pattren (like "from 21 Month_02 2020 and/to 7 Month_12 2022")
            #-------------------------------------------------------------------
            if ptrn_match and ptrn_dict_key=='days_case_2' :
                ptrn_match = [num for match in ptrn_match for num in match] # convert result from "[('01', '2010', '05', '2020')]" to "['01', '2010', '05', '2020']"                
                year_list= [int(ptrn_match[2]),int(ptrn_match[5])]
                year1,year2 = min(year_list),max(year_list)                 # pick smallest & Largest number from list                
                if int(year2) > current_year:                               # check largest year number w.r.to current year
                    year2= current_year
                day1,day2= int(ptrn_match[0]),int(ptrn_match[3]) 
                month1,month2= int(ptrn_match[1]),int(ptrn_match[4])
                final_dict['year']= [year1, year2]                           # insert result in 'final_dict'
                final_dict['month']= [month1,month2]
                final_dict['day']= [day1, day2]
                final_dict['operator']= 'between'
                return final_dict
            
            
            #-------------------------------------------------------------------
            # for 'days_case_2_2' pattren (like "not between 21 Month_02 to/and 7 Month_12 2022")
            #-------------------------------------------------------------------
            if ptrn_match and ptrn_dict_key=='days_case_2_2' :
                ptrn_match = [num for match in ptrn_match for num in match] # convert result from "[('01', '2010', '05', '2020')]" to "['01', '2010', '05', '2020']"                
                year1= ptrn_match[4]
                if int(year1) > current_year:
                    year1,year2= current_year,current_year
                else:
                    year1,year2= ptrn_match[4],ptrn_match[4]                                            # set start day=1
                day1,day2= int(ptrn_match[0]),int(ptrn_match[2]) 
                month1,month2= int(ptrn_match[1]),int(ptrn_match[3])
                final_dict['year']= [year1, year2]                           # insert result in 'final_dict'
                final_dict['month']= [month1,month2]
                final_dict['day']= [day1, day2]
                final_dict['operator']= 'notBetween'
                return final_dict
            
            
            #-------------------------------------------------------------------
            # for 'days_case_2_3' pattren (like "between 21 Month_02 to/and 7 Month_12 2022"")
            #-------------------------------------------------------------------
            if ptrn_match and ptrn_dict_key=='days_case_2_3' :
                ptrn_match = [num for match in ptrn_match for num in match] # convert result from "[('01', '2010', '05', '2020')]" to "['01', '2010', '05', '2020']"                
                year1= ptrn_match[4]
                if int(year1) > current_year:
                    year1,year2= current_year,current_year
                else:
                    year1,year2= ptrn_match[4],ptrn_match[4]                                            # set start day=1
                day1,day2= int(ptrn_match[0]),int(ptrn_match[2]) 
                month1,month2= int(ptrn_match[1]),int(ptrn_match[3])
                final_dict['year']= [year1, year2]                           # insert result in 'final_dict'
                final_dict['month']= [month1,month2]
                final_dict['day']= [day1, day2]
                final_dict['operator']= 'between'
                return final_dict
            
            
            #-------------------------------------------------------------------
            # for 'days_case_2_4' pattren (like "not between 21 Month_02 2020 and/to 7 Month_12 2022")
            #-------------------------------------------------------------------
            if ptrn_match and ptrn_dict_key=='days_case_2_4' :
                ptrn_match = [num for match in ptrn_match for num in match] # convert result from "[('01', '2010', '05', '2020')]" to "['01', '2010', '05', '2020']"                
                year_list= [int(ptrn_match[2]),int(ptrn_match[5])]
                year1,year2 = min(year_list),max(year_list)                 # pick smallest & Largest number from list                
                if int(year2) > current_year:                               # check largest year number w.r.to current year
                    year2= current_year
                day1,day2= int(ptrn_match[0]),int(ptrn_match[3]) 
                month1,month2= int(ptrn_match[1]),int(ptrn_match[4])
                final_dict['year']= [year1, year2]                           # insert result in 'final_dict'
                final_dict['month']= [month1,month2]
                final_dict['day']= [day1, day2]
                final_dict['operator']= 'notBetween'
                return final_dict
            
            
            
            #-------------------------------------------------------------------
            # for 'days_case_2_5' pattren (like "between 21 Month_02 2020 and/to 7 Month_12 2022")
            #-------------------------------------------------------------------
            if ptrn_match and ptrn_dict_key=='days_case_2_5' :
                ptrn_match = [num for match in ptrn_match for num in match] # convert result from "[('01', '2010', '05', '2020')]" to "['01', '2010', '05', '2020']"                
                year_list= [int(ptrn_match[2]),int(ptrn_match[5])]
                year1,year2 = min(year_list),max(year_list)                 # pick smallest & Largest number from list                
                if int(year2) > current_year:                               # check largest year number w.r.to current year
                    year2= current_year
                day1,day2= int(ptrn_match[0]),int(ptrn_match[3]) 
                month1,month2= int(ptrn_match[1]),int(ptrn_match[4])
                final_dict['year']= [year1, year2]                           # insert result in 'final_dict'
                final_dict['month']= [month1,month2]
                final_dict['day']= [day1, day2]
                final_dict['operator']= 'between'
                return final_dict
            
            
            

            #-------------------------------------------------------------------
            # for 'current_case' pattren (like "current month/months/year/years")
            #-------------------------------------------------------------------
            if ptrn_match and ptrn_dict_key=='current_case' :
                if ptrn_match[0] in ['this month','this months','existing month','existing months','present month',
                                     'present months','current month','current months']:
                    day1,month1,year1= 1,current_month,current_year
                    day2,month2,year2= current_day,current_month,current_year 
                    final_dict['year']= [year1, year2]                           # insert result in 'final_dict'
                    final_dict['month']= [month1,month2]
                    final_dict['day']= [day1, day2]
                    final_dict['operator']= 'between'
                    return final_dict
                elif ptrn_match[0] in ['this year','this years','existing year','existing years','present year',
                                     'present years','current year','current years']:
                    day1,month1,year1= 1,1,current_year
                    day2,month2,year2= current_day,current_month,current_year
                    final_dict['year']= [year1, year2]                           # insert result in 'final_dict'
                    final_dict['month']= [month1,month2]
                    final_dict['day']= [day1, day2]
                    final_dict['operator']= 'between'
                    return final_dict
                elif ptrn_match[0] in ['this day','this days','existing day','existing days','present day',
                                     'present days','current day','current days']:                
                    day1,month1,year1= current_day,current_month,current_year
                    final_dict['year']= [year1]                           # insert result in 'final_dict'
                    final_dict['month']= [month1]
                    final_dict['day']= [day1]
                    final_dict['operator']= '='
                    return final_dict
            
            
            #===============================================================
            # for 'past_case' pattren (like "last/previous/past month/months/year/years")
            #===============================================================
            if ptrn_match and ptrn_dict_key=='past_case' :
                if ptrn_match[0] in ['previous month','previous months','last month','last months','past month','past months']:
                    target_date = current_date - relativedelta(months=1)                    
                    year1,month1,day1= target_date.year,target_date.month,1
                    day2= calendar.monthrange(int(year1), int(month1))[1]       # find the no. of days w.r.to month
                    year2,month2,day2= target_date.year,target_date.month,day2
                    
                elif ptrn_match[0] in ['previous year','previous years','last year','last years','past year','past years']:
                    target_date = current_date - timedelta(days=1*365)          # calculate 'target_date' from 'current_date'
                    year1,month1,day1= target_date.year,1,1
                    year2,month2,day2= target_date.year,12,31
                final_dict['year']= [year1, year2]                              # insert result in 'final_dict'
                final_dict['month']= [month1,month2]
                final_dict['day']= [day1, day2]
                final_dict['operator']= 'between'
                return final_dict


            #===============================================================
            # for 'other_case_1' pattren (extract all numbers from text)
            #===============================================================
            if ptrn_match and ptrn_dict_key=='other_case_1' :
                #print('ptrn_match_len=',len(ptrn_match))
                #print('ptrn_match=',ptrn_match[0], len(ptrn_match[0]),'\n\n')
                
                #-------------------------------------
                # get date operator using above function
                #-------------------------------------
                final_date_oprt = date_oprt(f_text,f_maininput)  
                #print('Date_oprt=',final_date_oprt)
                
                
                #-------------------------------------------------------
                # for case: "24 Month_01 2022" 
                if len(ptrn_match)==3:                                         
                    year,month,day= ptrn_match[2],ptrn_match[1],ptrn_match[0] 
                    if int(year) > current_year:                               # check 'year': if greater than current year
                        year= current_year
                    final_dict['year']= [year]                                 # pass in list, to check length of list in 'low_high_date' function (later)
                    final_dict['month']= [month]  
                    final_dict['day']= [day]  
                    final_dict['operator']= final_date_oprt
                    return final_dict
                        
                    

                #-------------------------------------------------------
                # for case: " Month_01 2022" (different cases w.r.to operator)
                elif len(ptrn_match)==2:     
                                  
                    if final_date_oprt in ['=']:
                        year1,month1,day1= ptrn_match[1],ptrn_match[0],'01'
                        day2= calendar.monthrange(int(year1), int(month1))[1]  # find the no. of days using month
                        year2,month2,day2= ptrn_match[1],ptrn_match[0],day2
                        if int(year1) > current_year:                          # check 'year': if greater than current year
                            year1= current_year
                            year2= current_year
                        final_dict['year']= [year1, year2]                     # insert result in 'final_dict'
                        final_dict['month']= [month1,month2]
                        final_dict['day']= [day1, day2]
                        final_dict['operator']= 'between'
                        return final_dict

                    elif final_date_oprt in ['!=']:
                        year1,month1,day1= ptrn_match[1],ptrn_match[0],'01'
                        day2= calendar.monthrange(int(year1), int(month1))[1]  # find the no. of days using month
                        year2,month2,day2= ptrn_match[1],ptrn_match[0],day2
                        if int(year1) > current_year:                          # check 'year': if greater than current year
                            year1= current_year
                            year2= current_year
                        final_dict['year']= [year1, year2]                     # insert result in 'final_dict'
                        final_dict['month']= [month1,month2]
                        final_dict['day']= [day1, day2]
                        final_dict['operator']= 'notBetween'
                        return final_dict
                    
                    elif final_date_oprt in ['>=','<','<=']:
                        year,month,day= ptrn_match[1],ptrn_match[0],'01' 
                        if int(year) > current_year:                           # check 'year': if greater than current year
                            year= current_year
                        final_dict['year']= [year]                             # pass in list, to check length of list in 'low_high_date' function (later)
                        final_dict['month']= [month]  
                        final_dict['day']= [day]  
                        final_dict['operator']= final_date_oprt
                        return final_dict
                    
                    elif final_date_oprt in ['>']:
                        year,month,day= ptrn_match[1],ptrn_match[0],'31' 
                        if int(year) > current_year:                           # check 'year': if greater than current year
                            year= current_year
                        final_dict['year']= [year]                             # pass in list, to check length of list in 'low_high_date' function (later)
                        final_dict['month']= [month]  
                        final_dict['day']= [day]  
                        final_dict['operator']= final_date_oprt
                        return final_dict


                        
                #======================================================
                # for case: SINGLE ENTITY NUMBER (like 2022/jan...)
                elif len(ptrn_match)==1:                                                        
                    
                    #---------------------------
                    # for 'Year' (like ['2022'])
                    if len(ptrn_match[0])==4:
                        if final_date_oprt in ['=','!=']:                      # for operator '=' and '!='                
                            year1,month1,day1= ptrn_match[0],'01','01'
                            if int(year1) >= current_year:                     # check 'year': if greater than current year
                                year1= current_year
                                year2= current_year
                                month2= current_month
                                day2= current_day
                            else:    
                                year2,month2,day2= year1,'12','31'
                            final_dict['year']= [year1,year2]                  
                            final_dict['month']= [month1,month2]  
                            final_dict['day']= [day1,day2]  
                            final_dict['operator']= 'between'
                            return final_dict
                        
                        elif final_date_oprt in ['<','>=','<=']:               # for operators: '<','>=',<='                                    
                            year,month,day= ptrn_match[0],'01','01'
                            if int(year) > current_year:                       # check 'year': if greater than current year
                                year= current_year
                            final_dict['year']= [year]                         # pass in ist, to check length of list in 'low_high_date' function
                            final_dict['month']= [month]  
                            final_dict['day']= [day]  
                            final_dict['operator']= final_date_oprt
                            return final_dict
                            
                        elif final_date_oprt in ['>']:                         # for operators: '>'                                   
                            year,month,day= ptrn_match[0],'12','31'
                            if int(year) > current_year:                       # check 'year': if greater than current year
                                year= current_year
                            final_dict['year']= [year]                         # pass in ist, to check length of list in 'low_high_date' function
                            final_dict['month']= [month]  
                            final_dict['day']= [day]  
                            final_dict['operator']= final_date_oprt
                            return final_dict
                    
                    #---------------------------
                    # for 'Month' (like ['01'])
                    if len(ptrn_match[0])==2:
                        if final_date_oprt in ['=','!=']:                      # for operator '=' and '!='                
                            year1,month1,day1= current_year,ptrn_match[0],'01'
                            day2= calendar.monthrange(int(current_year), int(month1))[1]  # find the no. of days using month
                            year2,month2,day2= current_year,ptrn_match[0],day2
                            final_dict['year']= [year1,year2]                  
                            final_dict['month']= [month1,month2]  
                            final_dict['day']= [day1,day2]  
                            final_dict['operator']= 'between'
                            return final_dict
                        
                        elif final_date_oprt in ['>','<=']:                    # start date for jan '31/01/'2023
                            year,month= current_year,ptrn_match[0]
                            day= calendar.monthrange(int(year), int(month))[1] # find the no. of days using month                                    
                            final_dict['year']= [year]                         # pass in ist, to check length of list in 'low_high_date' function
                            final_dict['month']= [month]  
                            final_dict['day']= [day]  
                            final_dict['operator']= final_date_oprt
                            return final_dict
                        
                        elif final_date_oprt in ['<','>=']:                    # start date for jan '01/01/'2023                                    
                            year,month,day= current_year,ptrn_match[0],'01'
                            final_dict['year']= [year]                         # pass in ist, to check length of list in 'low_high_date' function
                            final_dict['month']= [month]  
                            final_dict['day']= [day]  
                            final_dict['operator']= final_date_oprt
                            return final_dict

                        
                        





#******************************************************************************
# Start: 'extract_date' Function (code)
#******************************************************************************
def covert_date_text(f_param,f_text,f_maininput):
    f_maininput= ' '+f_maininput+' '
    
    #-------------------------------------------------
    # take text after 'param'
    start_index= f_maininput.find(' '+str(f_param)+' ')
    segmented_text= f_maininput[start_index:]

    
    #---------------------------------------
    # Get complete date_dict through module
    final_response={}
    date_dict= extract_date(f_text,segmented_text)                               # get year/month/day using 'extract_date' function
    
    #----------------------------------------------------------------
    # Extract 'year' from data received from 'extract_date' function 
    # Reurn 'empty': if value is 'None'
    try:                                                                      
        year_list_leng= date_dict['year']
    except:                                                                   # in case: if value is 'None'
        return final_response
    
    #-----------------------------------------------------
    # Set/Format response w.r.to adhoc
    if date_dict and len(year_list_leng)==2:                                  # check: 'function_result' is not empty
        years= date_dict['year']
        months= date_dict['month']
        days= date_dict['day']
        oprt= date_dict['operator']
        
        final_response['value']=   f'{years[0]}-{months[0]:02}-{days[0]:02}T05:00:00.000Z'
        final_response['value1']=  f'{years[1]}-{months[1]:02}-{days[1]:02}T05:00:00.000Z' 
        final_response['operator']= oprt
        return final_response
    
    elif date_dict and len(year_list_leng)==1:                                # check: 'function_result' is not empty
        years= date_dict['year'][0]                                           # take first index of 'year'
        months= date_dict['month'][0]
        days= date_dict['day'][0]
        oprt= date_dict['operator']
        if len(str(days))==1:                                                      # check: if len(day)=1, then add '0' at start for adhoc response 
            days= '0'+days
        final_response['value']=   f'{years}-{months}-{days}T05:00:00.000Z'
        final_response['value1']=  None 
        final_response['operator']= oprt
        return final_response





#******************************************************************************
#******************************************************************************
'''
input_text='copd and ckd for from 2023 '
date= '2023'
param='ckd'

response= covert_date_text(param,date,input_text)
print('\nFinal Output:\n',response)
'''







