# -*- coding: utf-8 -*-
"""
    Project : Adhoc Query Builder
    Module  : For LLM 
    Desciption: Take input text and after params extraction, 
                replace all params/Values/Times with 'Token' 
"""


from Modules.For_All.Text_Preprocessing import text_clean
from Modules.For_All.Merge_Param_Modules import merge_param_module
from Modules.For_All.Data_Params_Extraction_Optimization import param_optimize

from Modules.Grouper_Field.Data_Params_Extraction import param_extraction
from Modules.Code_Field.Code_Params_Extraction import code_extraction 
from Modules.Appointment_Field.Appointment_Params_Extraction import appointment_extraction
from Modules.Claim_Field.Claim_Params_Extraction import claims_extraction
from Modules.CarePovider_Field.CareProvider_Params_Extraction import careprovider_extraction
from Modules.CarePlan_Field.CarePlan_Params_Extraction import careplan_extraction
from Modules.Attributes_Field.Attribute_Params_Extraction import attribute_extraction
from Modules.Payer_Field.Payer_Params_Extraction import payer_extraction



field_pad_dict= {'Age':'AGE','Problem':'CONDITION','Procedure':'CONDITION',
                'Encounter':'CONDITION','Immunization':'CONDITION','Allergies':'CONDITION',
                'DOB':'DEMOGRAPHICS','Gender':'DEMOGRAPHICS','Ethnicity':'DEMOGRAPHICS',
                'Deceased Date':'DEMOGRAPHICS','Religion':'DEMOGRAPHICS','Marital Status':'DEMOGRAPHICS',
                'Race':'DEMOGRAPHICS','Medication':'RX','Labs':'TEST','Vital Sign':'TEST',
                'Claims':'COST','Appointments':'APPOINTMENT','Care Provider':'CARE_PROVIDER',
                'Care Plan':'CARE_PLAN','Payer':'PAYER'}


    
#=====================================================
# "Text_for_LLM" function
#=====================================================
def replace_params_with_token(f_text):
    #print("'Main Input':",f_text,'\n')
    
    #-----------------------------------------
    # text preprocessing
    final_clean_text_wo_dot= text_clean(f_text)
    
    #-----------------------------------------
    # Extract all initial params from text through modules 
    attribute_params_extraction= attribute_extraction(final_clean_text_wo_dot)
    claim_params_extraction= claims_extraction(attribute_params_extraction[1])    
    payer_params_extraction=  payer_extraction(claim_params_extraction[1])
    appointment_params_extraction= appointment_extraction(payer_params_extraction[1])
    careprovider_params_extraction= careprovider_extraction(appointment_params_extraction[1])
    careplan_params_extraction= careplan_extraction(careprovider_params_extraction[1])
    grouper_params_extraction= param_extraction(careplan_params_extraction[1])
    

    #-----------------------------------------
    # Merge all extracted params in one 'dict'
    merge_above_params_dict= merge_param_module([attribute_params_extraction[0],claim_params_extraction[0],
                                                 payer_params_extraction[0],appointment_params_extraction[0],
                                                 careprovider_params_extraction[0],careplan_params_extraction[0],
                                                 grouper_params_extraction])
    
    #-------------------------------------
    # Extract code from text using 'all_params_extraction_dict'
    all_params_extraction_dict= code_extraction(final_clean_text_wo_dot,merge_above_params_dict)

    #-----------------------------------------
    # Return 'None', if extracted params dict is empty
    if not all_params_extraction_dict:
        return None
    else:   pass
    
    #-----------------------------------------
    # SMART QB ( Parameters optimization)
    final_params_extaction= param_optimize(final_clean_text_wo_dot,all_params_extraction_dict)
    optimized_paraam_dict= final_params_extaction[1]
    modify_clean_text= final_params_extaction[0]
    
    
    #-----------------------------------------
    # Params Grouping
    param_grouping_dict={}
    for param_field,param_name_list in optimized_paraam_dict.items():
        if param_field in ['Problem','Procedure','Encounter','Immunization','Allergies']:
            try:    param_grouping_dict['CONDITION'].extend(param_name_list)
            except: param_grouping_dict['CONDITION']= param_name_list
            
                
        elif param_field in ['DOB','Gender','Ethnicity','Deceased Date','Religion','Marital Status','Race']:
            try:    param_grouping_dict['DEMOGRAPHICS'].extend(param_name_list)
            except: param_grouping_dict['DEMOGRAPHICS']= param_name_list
            

        elif param_field in ['Age']:
            try:    param_grouping_dict['AGE'].extend(param_name_list)
            except: param_grouping_dict['AGE']= param_name_list
            

        elif param_field in ['Medication']:
            try:    param_grouping_dict['RX'].extend(param_name_list)
            except: param_grouping_dict['RX']= param_name_list
            
            
        elif param_field in ['Labs','VitalSign']:
            try:    param_grouping_dict['TEST'].extend(param_name_list)
            except: param_grouping_dict['TEST']= param_name_list
            
            
        elif param_field in ['Total Spend','Risk Score','Inpatient Spend','Hospital outpatient Spend','Pharmacy Spend',
                             'Professional outpatient Spend','SNF Spend','Home Health Spend','Hospice Spend','DME Spend',
                             'Radiology Visit','Readmission Count','ER Visit']:
            try:    param_grouping_dict['COST'].extend(param_name_list)
            except: param_grouping_dict['COST']= param_name_list
            

        elif param_field in ['Admitting Provider Name','Admitting Provider NPI','Attending Provider Name','Attending Provider NPI',
                            'Created By','Duration','Start Date','End Date','Visit Type']:
            try:    param_grouping_dict['APPOINTMENT'].extend(param_name_list)
            except: param_grouping_dict['APPOINTMENT']= param_name_list


        elif param_field in ['Startdate','Enddate','First Name','Last Name','NPI','Role','Specialty','Status','Zipcode','State',
                             'City','Phone','Email','Full Name']:
            try:    param_grouping_dict['CARE_PROVIDER'].extend(param_name_list)
            except: param_grouping_dict['CARE_PROVIDER']= param_name_list


        elif param_field in ['AuthorizationStatus CarePlan','AuthorizedBy CarePlan','AuthorizedDate CarePlan','CreatedBy CarePlan',
                             'CreatedDate CarePlan','StartDate CarePlan','EndDate CarePlan','ModifiedBy CarePlan','ModifiedDate CarePlan']:
            try:    param_grouping_dict['CARE_PLAN'].extend(param_name_list)
            except: param_grouping_dict['CARE_PLAN']= param_name_list 
            
            
        elif param_field in ['Coverage ID Payer','Coverage type Payer','Coverage Display Name Payer','Start Date Payer',
                             'End Date Payer','Patient Name Payer','Patient First Name Payer','Patient Last Name Payer',
                             'Subscriber ID Payer','Display Name Payer','Source Payer','Insurance Type Code Payer']:
            try:    param_grouping_dict['PAYER'].extend(param_name_list)
            except: param_grouping_dict['PAYER']= param_name_list    
            

        elif param_field in ['Attributed Group','Attributed Practice','Attributed Practice Name','Attributed Program',
                             'Attributed Program Type','Attributed Provider Emp Status','Attributed Provider Id',
                             'Attributed Provider Name']:
            try:    param_grouping_dict['ATTRIBUTE'].extend(param_name_list)
            except: param_grouping_dict['ATTRIBUTE']= param_name_list
            
            
    #-----------------------------------------------------
    # create 'param_token_dict'
    param_token_dict= {}
    age_no, demography_no, condition_no, rx_no, test_no= 0, 0, 0, 0, 0
    cost_no, appointment_no, careprovider_no, careplan_no, paye_no= 0, 0, 0, 0, 0

    for param_field,param_name_list in param_grouping_dict.items():
        sorted_params_list = sorted(param_name_list, key=lambda x: modify_clean_text.find(x))
        for param_name in sorted_params_list: 
            if param_field == 'AGE':
                pad_token_with_no= param_field + str(age_no)  
                param_token_dict[pad_token_with_no]= param_name
                age_no= age_no+1

            elif param_field == 'DEMOGRAPHICS':
                pad_token_with_no= param_field + str(demography_no)  
                param_token_dict[pad_token_with_no]= param_name
                demography_no= demography_no+1
            
            elif param_field == 'CONDITION':
                pad_token_with_no= param_field + str(condition_no)  
                param_token_dict[pad_token_with_no]= param_name
                condition_no= condition_no+1

            elif param_field == 'RX':
                pad_token_with_no= param_field + str(rx_no)  
                param_token_dict[pad_token_with_no]= param_name
                rx_no= rx_no+1
            
            elif param_field == 'TEST':
                pad_token_with_no= param_field + str(test_no)  
                param_token_dict[pad_token_with_no]= param_name
                test_no= test_no+1
            
            elif param_field == 'COST':
                pad_token_with_no= param_field + str(cost_no)  
                param_token_dict[pad_token_with_no]= param_name
                cost_no= cost_no+1

            elif param_field == 'APPOINTMENT':
                pad_token_with_no= param_field + str(appointment_no)  
                param_token_dict[pad_token_with_no]= param_name
                appointment_no= appointment_no+1

            elif param_field == 'CARE_PROVIDER':
                pad_token_with_no= param_field + str(careprovider_no)  
                param_token_dict[pad_token_with_no]= param_name
                careprovider_no= careprovider_no+1
            
            elif param_field == 'CARE_PLAN':
                pad_token_with_no= param_field + str(careplan_no)  
                param_token_dict[pad_token_with_no]= param_name
                careplan_no= careplan_no+1
                
            elif param_field == 'PAYER':
                pad_token_with_no= param_field + str(paye_no)  
                param_token_dict[pad_token_with_no]= param_name
                paye_no= paye_no+1
                        
    #-----------------------------------------------------
    # replace param with token using 'param_token_dict'
    for token,param in param_token_dict.items():
        modify_clean_text= modify_clean_text.replace(' '+param+' ',' '+token+' ')
  
    return {'text':modify_clean_text,'params':param_token_dict}

  

#==================================================================================================

'''
#text= ' african male patients that are suffering from ckd,copd and depression screening and underwent depression screening with hba1c and bmi is 50 '
text='show me all the patient with snf costs above 2000 and dme costs below 1900 in 2020'

result= replace_params_with_token(text)
print('\n\nText:',result['text'])
print('\nParam Dic: ',result['params'])
'''



