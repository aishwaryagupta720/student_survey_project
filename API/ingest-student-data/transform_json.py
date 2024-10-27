import json
import logging
import boto3
import re
import traceback


# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# initialise user data dictionary
user_data={}

def process_outcomes(id,outcomes):
    outcome = outcomes[0]  # Assuming only one outcome 
    text = outcome.get('text', '')
    
    url_match = re.search(r'href="([^"]+)"', text)
    if not url_match:
        url=""
        return url

    # Extract the full URL
    full_url = url_match.group(1)
    
    modified_url = full_url.replace('*|SESSION_SIGNATURE|*', id)
    
    return modified_url

def process_questions(questions):
    
    # Mapping from question titles to keys
    mappings = {
        'Communication': 'communication',
        'Teamwork': 'teamwork',
        'Self-Development': 'self_development',
        'Professionalism': 'professionalism',
        'Leadership': 'leadership',
        'Critical Thinking': 'critical_thinking',
        'Technology': 'technology',
        'Equity': 'equity',
        'Social Capital': 'social_capital',
        'Life Design': 'life_design',
        'Career Mobility': 'career_mobility',
        'When are you completing this inventory': 'work_experience',
        'degree/certificate/class': 'demographics'
    }
    
    answer_dict = {}
    current_key = None
    
    for question in questions:
        if question['order']<3:
            continue
        # Determine if the title contains any of the keys for the mappings and set the current category key
        if question['type']['object_name']=='plaintext' and any(key in question['title'] for key in mappings):
            current_key = mappings[next(key for key in mappings if key in question['title'])]
            answer_dict[current_key] = []

        # Check if there's an active current_key
        if current_key:
            if question['type']['object_name'] in ['text_choice', 'typeahead']:
                # Process text_choice and typehead type questions
                question_details = { 'order': question['order']}
                if question['score']!=None:
                    question_details['score_value']= float(question['score']['score_value'])
                    question_details['score_max']= float(question['score']['score_max'])
                    if isinstance(question['response'], dict) :
                        if "Not Applicable" in question['response']['text'] or "Not Observed" in question['response']['text'] :
                            question_details['score_value']= 5.0
                else:
                    question_details['score_value']=  0.0
                    question_details['score_max']= 0.0
                    
                if current_key in ['social_capital','life_design','career_mobility','work_experience','demographics']:
                    question_text = re.sub(r'[\n\r\u201C\u201D\"\']+','', question['title'])
                    question_details['question']=question_text.replace('&nbsp;', ' ').replace('\n', ' ').strip()
                    if question['order'] == 75 or question['responses'] !=[]:
                        question_details['response'] = response['response']
                    elif 'text' in question['response']:
                        question_details['response']= question['response'].get('text', 'None')
                    else:
                        question_details['response']=None
                    
                    if question_details['response'] !=None:
                        question_details['response']= question_details['response'].replace('&nbsp;', ' ').replace('\n', ' ').strip()
                
                answer_dict[current_key].append(question_details)
                
            elif question['type']['object_name'] == 'form':
                # isNone = True
                # Process form type questions
                form_responses = {
                    'order': question.get('order'),
                    'question': question.get('title'),
                    'responses':[]
                }
                if question['order'] == 76:
                    for response in question.get('responses', []):
                        form_responses['response'] = response['response']
                        break
                else:
                    for response in question.get('responses', []):
                        if 'text' in response and 'response' in response:
                            options={}
                            options['text'] = response['text'].strip()
                            # if response['response'] != None : 
                            #     isNone=False
                            options['response'] = response['response']
                            form_responses['responses'].append(options)
                    if question['score']!=None:
                        form_responses['score_value']= float(question['score']['score_value'])
                        form_responses['score_max']= float(question['score']['score_max'])
                    else:
                        form_responses['score_value']=  0.0
                        form_responses['score_max']= 0.0
                    # if isNone:
                    #     form_responses['responses']=[]
                answer_dict[current_key].append(form_responses)
    # Find the index of the work and demographics questions
    work_index = None
    demographics_index = None
    
    for index, entry in enumerate(answer_dict['career_mobility']):
        if work_index is None:  # Check explicitly for None
            if entry.get('question') and 'completing this inventory' in entry['question']:
                work_index = index
        if demographics_index is None:  # Check explicitly for None
            if entry.get('question') and 'degree/certificate/class' in entry['question']:
                demographics_index = index
        if work_index is not None and demographics_index is not None:  # Once both are found, break the loop
            break
    # Extract work_experience and modify career_mobility before updating it
    answer_dict['work_experience'] = answer_dict['career_mobility'][work_index:demographics_index]
    answer_dict['demographics'] = answer_dict['career_mobility'][demographics_index:]
    answer_dict['career_mobility'] = answer_dict['career_mobility'][:work_index]

    
        
    
    return answer_dict



def process_custom_fields(custom_fields):
    
    # Mapping from custom field text to answer dictionary keys
    mapping = {
        'Organization Name': 'org_name',
        'Org Type': 'org_type',
        'Inventory Version': 'inventory_version',
        'Implementation Type': 'implementation_type',
        'Use Case ID': 'use_case_id',
        'Semester/Quarter': 'semester',
        'Attempt Type': 'attempt_type',
    }
    
    exclude_fields = [
    "First Name",
    "Last Name",
    "Student Email",
    "Evaluator #1 First Name",
    "Evaluator #1 Last Name",
    "Evaluator #1 Email",
    "Evaluator #2 First Name",
    "Evaluator #2 Last Name",
    "Evaluator #2 Email"
]
    
    # Initialize a dictionary to store the processed results
    processed_data = {}
    processed_data['custom_fields']=[]
    
    # Iterate over the custom fields and map them to the new keys
    for field in custom_fields:
        # Check if the field text is in the mapping
        if field['text'] in mapping:
            # Map the value to the new key in the processed_data dictionary
            new_key = mapping[field['text']]
            processed_data[new_key] = field['value']
        elif field['text'] not in exclude_fields:
            options={
                'key':field['text'],
                'value': field['value']
            }
            processed_data['custom_fields'].append(options)
    
    
    return processed_data
    

def process_results(question_blocks,formula_results ):
    # Example category mapping
    category_mapping = {
        'Communication': 'communication_results',
        'Teamwork': 'teamwork_results',
        'Self-Development': 'self_development_results',
        'Professionalism': 'professionalism_results',
        'Leadership': 'leadership_results',
        'Critical Thinking': 'critical_thinking_results',
        'Technology': 'technology_results',
        'Equity': 'equity_results',
        'Overall Career Readiness': 'overall_career_readiness_results'
    }
    implementation_map = {
        'Pre-Inventory Flag':'pre',
        'Post-Inventory Flag':'post',
        'Mid-Inventory Flag': 'mid'
    }

    # Initialize a dictionary to hold the results
    results = {value: {} for value in category_mapping.values()}
    
    # Function to extract data from question_blocks
    def process_questions(question):
        for key, value in category_mapping.items():
            if key in question['title']:
                if 'score' in question and question['score'] != None:
                    entry = {
                        'score_value': float(question['score'].get('score_value')),
                        'score_max': float(question['score'].get('score_max')),
                        'score_quiz_as_percentage': float(question['score'].get('score_quiz_as_percentage').replace("%",""))/100,
                    }
                    results[value].update(entry)
                else:
                    entry = {
                        'score_value': None,
                        'score_max': None,
                        'score_quiz_as_percentage': None,
                    }
                    results[value].update(entry)
    
    # Function to extract data from formula_results
    def process_formulas(formula):
        for key, value in category_mapping.items():
            if key in formula['name']:  # Assuming the formula name relates to the category
                entry = {
                    'result': float(formula.get('result'))
                }
                results[value].update(entry)
        
        for flag, timing in implementation_map.items():
            if flag in formula['name'] and int(formula.get('result', 0)) == 1:
                results['implementation_time'] = timing

    # Process each question
    for question in question_blocks:
        process_questions(question)

    # Process each formula result
    for formula in formula_results:
        process_formulas(formula)

    return results


def process_all_data(data):
    try:
        user_data = {
            'response_id': data['unique_identifier'],
            'timestamp': data['timestamp_utc'],
            'email': data['respondent']['email'],
            'name': data['respondent']['name'],
            'last_name': data['respondent']['last_name'],
            'respondent_id': data['respondent']['unique_identifier'],
            'pdf_url': process_outcomes(data['unique_identifier'], data['outcomes']),
            'survey_id': data['survey']['unique_identifier'],
            'survey_url': data['survey']['url'],
            'survey_title': data['survey']['title'],
            'duration': data['duration']
        }
        
        user_data.update(process_custom_fields(data.get("custom_fields", [])))
        user_data.update(process_questions(data.get("questions", [])))
        user_data.update(process_results(data.get("question_blocks", []),data.get("formula_results", [])))
        
        return user_data

    except KeyError as e:
        error_msg = f"Missing key error: {str(e)} - Check data structure and ensure all keys are present."
        logger.error(error_msg + f" At line: {traceback.format_exc()}")
        raise Exception(error_msg)
    except ValueError as e:
        error_msg = f"Value error: {str(e)} - Check data types of fields."
        logger.error(error_msg + f" At line: {traceback.format_exc()}")
        raise Exception(error_msg)
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.error(error_msg + f" At line: {traceback.format_exc()}")
        raise Exception(error_msg)
