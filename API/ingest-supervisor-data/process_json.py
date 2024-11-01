import json
import logging
import boto3
import re
import traceback


# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

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
    
def process_custom_fields(custom_fields):
    filtered_fields = {}
    start_recording = False
    implementation=''

    for field in custom_fields:
        # Start recording from 'cf4' onwards
        if field['name'] =='cf4':
            start_recording = True
        elif field['name'] =='cf11':
            start_recording = False
            
        # if field['text'] == 'Implementation text':
        #     implementation=field['value']
        if start_recording:
            # Check if the value is not None before appending
            # if field['value'] != 'None':
            key = field['text'].strip().replace(" ", "_").replace("#", "").lower()
            filtered_fields[key]=field['value']
    
    return filtered_fields
    
    
def process_question_fields(questions):
    results = []
    for question in questions:
        if question['order'] >1:
            if question['type']['object_name'] in ('text_choice','typehead') and question['response']!= 'None':
                result = {
                        'order': question['order']
                        }
                if question['score'] != None:
                    result['score_value']= question['score'].get('score_value', '0')
                    result['score_max']= question['score'].get('score_max', '0')
                    # result['score_custom_as_percentage']= question['score'].get('score_custom_as_percentage', '0').strip('%')
                    if "Not Applicable" in question['response']['text'] or "Not Observed" in question['response']['text'] :
                        result['score_value']= '5.0'
                    if question['order']==38:
                        result['response'] = question['response']['text']
                    results.append(result)

                else:
                    result['score_value']=  '0.0'
                    result['score_max']= '0.0'
                    # 'score_custom_as_percentage': '0.0'
                    results.append(result)
            elif question['type']['object_name'] == 'form':
                result = {
                    'order': question['order'],
                    'response': {}
                }
                if question['order']==37:
                    for response in question['responses']:
                        if 'response' in response:
                            result['response'] = response['response']
                else:
                    for response in question['responses']:
                        if 'text' in response and 'response' in response:
                            key = response['text'].strip().replace(" ","_").lower()
                            result['response'][key] = response['response']
                results.append(result)

    return results

def process_question_blocks(blocks):
    results = []
    for block in blocks:
        if block.get('score') is not None: 
            result = {
                'title': block['title'],
                'order': block['order'],
                'score_value': block['score'].get('score_value', '0'),  
                'score_max': block['score'].get('score_max', '0'),  
                'score_quiz_as_percentage': block['score'].get('score_quiz_as_percentage', '0').strip('%')
            }
        else: 
            result = {
                'title': block['title'],
                'order': block['order'],
                'score_value': '0.0',
                'score_max': '0.0',
                'score_quiz_as_percentage': '0.0'
            }
        results.append(result)
    return results
 
def process_formula_results(formula_results):
    processed_results = []
    for formula in formula_results:
        if formula['formula_order'] > 9:
            continue
        processed_result = {
            'formula_order': formula['formula_order'],
            'name': formula['name'],
            # 'unique_identifier': formula['unique_identifier'],
            # 'formula': formula['formula'],
            'result': str(formula['result'])
        }
        processed_results.append(processed_result)
    return processed_results

def process_all_data(data):
    try:
        user_data = {
            'response_id': data['unique_identifier'],
            'timestamp': data['timestamp_utc'],
            'name': data['respondent']['name'],
            'last_name': data['respondent']['last_name'],
            'email': data['respondent']['email'],
            'respondent_id': data['respondent']['unique_identifier'],
            'pdf_url': process_outcomes(data['unique_identifier'], data['outcomes']),
            'survey_id': data['survey']['unique_identifier'],
            'survey_url': data['survey']['url']
            # 'survey_title': data['survey']['title'],
            # 'custom_fields': process_custom_fields(data.get("custom_fields", [])),
            # 'questions': process_question_fields(data.get("questions", [])),
            # 'question_blocks': process_question_blocks(data.get("question_blocks", [])),
            # 'formula_results': process_formula_results(data.get("formula_results", []))
        }
        
        # Merge filtered_data into user_data
        user_data.update(process_custom_fields(data.get("custom_fields", [])))
        
        user_data['questions'] = process_question_fields(data.get("questions", []))
        user_data['question_blocks'] = process_question_blocks(data.get("question_blocks", []))
        user_data['formula_results'] = process_formula_results(data.get("formula_results", []))
        
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