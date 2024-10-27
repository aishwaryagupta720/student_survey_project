import json
import logging
import traceback
import psycopg2
from psycopg2 import OperationalError, InterfaceError, DatabaseError
from db_operations import get_db_connection,execute_query
from get_data_from_id import get_all_questions,get_organization,get_all_students
from collections import defaultdict

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


competencies = ['communication_results','teamwork_results','self_development_results','professionalism_results',
                'leadership_results','critical_thinking_results','technology_results','equity_results',
                'overall_career_readiness_results']
                
question_mapping={
    'communication' : {
        4:'Oral Communication',
        5:'Written Communication' ,
        6:'Non-verbal Communication',
        7:'Active Listening'
    },
    'teamwork' : {
        9:'Build Relationships for Collaboration',
        10:'Respect Diverse Perspectives',
        11:'Integrate Strengths'
    },
    'self_development' : {
        13:'Awareness of Strengths & Challenges',
        14:'Professional Development',
        15:'Networking'
    },
    'professionalism' : {
        17:'Act With Integrity',
        18:'Demonstrate Dependability',
        19:'Achieve Goals'
    },
    'leadership' : {
        21:'Inspire, Persuade, & Motivate',
        22:'Engage Various Resources & Seek Feedback',
        23:'Facilitate Group Dynamics'
    },
    'critical_thinking' : {
        25:'Display Situational Awareness',
        26:'Gather & Analyze Data',
        27:'Make Effective & Fair Decisions'
    },
    'technology' : {
        29:'Leverage Technology',
        30:'Adapt to New Technologies',
        31:'Use Technology Ethically'
    },
    'equity' : {
        33:'Engage Multiple Perspectives',
        34:'Use Inclusive & Equitable Practices',
        35:'Advocate'
    }
}

observer_question_mapping={
    'communication' : {
        5:'Oral Communication',
        6:'Written Communication' ,
        7:'Non-verbal Communication',
        8:'Active Listening'
    },
    'teamwork' : {
        10:'Build Relationships for Collaboration',
        11:'Respect Diverse Perspectives',
        12:'Integrate Strengths'
    },
    'self_development' : {
        14:'Awareness of Strengths & Challenges',
        15:'Professional Development',
        16:'Networking'
    },
    'professionalism' : {
        18:'Act With Integrity',
        19:'Demonstrate Dependability',
        20:'Achieve Goals'
    },
    'leadership' : {
        22:'Inspire, Persuade, & Motivate',
        23:'Engage Various Resources & Seek Feedback',
        24:'Facilitate Group Dynamics'
    },
    'critical_thinking' : {
        26:'Display Situational Awareness',
        27:'Gather & Analyze Data',
        28:'Make Effective & Fair Decisions'
    },
    'technology' : {
        30:'Leverage Technology',
        31:'Adapt to New Technologies',
        32:'Use Technology Ethically'
    },
    'equity' : {
        34:'Engage Multiple Perspectives',
        35:'Use Inclusive & Equitable Practices',
        36:'Advocate'
    }
}
                
    
def build_observer_query(emails,student_email):
    """
    Dynamically builds the SQL query based on the filters provided.
    """
    
    email_string = ', '.join(f"'{email}'" for email in emails)

    question_query = f"""
        SELECT 
            competency,
            elements->>'order' AS question_order,
            AVG((elements->>'score_value')::numeric) AS score_values
        FROM 
            observer_response sr
        CROSS JOIN LATERAL (
            VALUES
                ('communication', sr.communication),
                ('teamwork', sr.teamwork),
                ('self_development', sr.self_development),
                ('professionalism', sr.professionalism),
                ('leadership', sr.leadership),
                ('critical_thinking', sr.critical_thinking),
                ('technology', sr.technology),
                ('equity', sr.equity)
        ) AS c(competency, elements_json)
        CROSS JOIN LATERAL
            jsonb_array_elements(c.elements_json) AS elements
        WHERE
            sr.email in ({email_string}) AND sr.student_email = '{student_email}'
        GROUP BY
            competency,
            question_order
        ORDER BY
            competency, question_order;
    """
    
    comp_query=f"""
                    SELECT 
                    sr.communication_results->>'result' AS communication_results,
                    sr.teamwork_results->>'result' AS teamwork_results,
                    sr.self_development_results->>'result' AS self_development_results,
                    sr.professionalism_results->>'result' AS professionalism_results,
                    sr.leadership_results->>'result' AS leadership_results,
                    sr.critical_thinking_results->>'result' AS critical_thinking_results,
                    sr.technology_results->>'result' AS technology_results,
                    sr.equity_results->>'result' AS equity_results,
                    sr.overall_career_readiness_results->>'result' AS overall_career_readiness_results
                FROM 
                    observer_response sr
                WHERE
                    sr.email in ({email_string}) AND sr.student_email = '{student_email}'
                """
    
    return comp_query,question_query


def build_query(request):
    """
    Dynamically builds the SQL query based on the filters provided.
    """
    
    email= get_all_students(request['id'])
    observer_emails = request['evaluator_email']
    implementation_type = request['implementation_type']
    use_case,semester = request['filter'].split(":")
    
    question_query = f"""
        SELECT 
            competency,
            elements->>'order' AS question_order,
            sr.implementation_time,
            AVG((elements->>'score_value')::numeric) AS score_values
        FROM 
            student_response sr
        CROSS JOIN LATERAL (
            VALUES
                ('communication', sr.communication),
                ('teamwork', sr.teamwork),
                ('self_development', sr.self_development),
                ('professionalism', sr.professionalism),
                ('leadership', sr.leadership),
                ('critical_thinking', sr.critical_thinking),
                ('technology', sr.technology),
                ('equity', sr.equity)
        ) AS c(competency, elements_json)
        CROSS JOIN LATERAL
            jsonb_array_elements(c.elements_json) AS elements
        WHERE
            sr.email = %s
            AND sr.implementation_type = %s
            AND sr.use_case_id = %s
            AND sr.semester = %s
            AND sr.implementation_time IN ('pre', 'mid', 'post')
        GROUP BY
            competency,
            sr.implementation_time,
            question_order
        ORDER BY
            sr.implementation_time, competency, question_order;
    """
    
    comp_query = """ 
        SELECT 
            sr.implementation_time,
            sr.communication_results->>'result' AS communication_results,
            sr.teamwork_results->>'result' AS teamwork_results,
            sr.self_development_results->>'result' AS self_development_results,
            sr.professionalism_results->>'result' AS professionalism_results,
            sr.leadership_results->>'result' AS leadership_results,
            sr.critical_thinking_results->>'result' AS critical_thinking_results,
            sr.technology_results->>'result' AS technology_results,
            sr.equity_results->>'result' AS equity_results,
            sr.overall_career_readiness_results->>'result' AS overall_career_readiness_results
        FROM 
            student_response sr
        WHERE
            sr.email = %s
            AND sr.implementation_type = %s
            AND sr.use_case_id = %s
            AND sr.semester = %s
            AND sr.implementation_time IN ('pre', 'mid', 'post');
        """
            
    query_params = [email,implementation_type,use_case,semester]
    
    observer_comp_query,observer_question_query = build_observer_query(observer_emails,email)
    
    
    return question_query,comp_query,query_params,observer_question_query,observer_comp_query 
    
def get_range_name(score):
    ranges = {
        "Emerging Knowledge": (1.00, 1.75),
        "Understanding": (1.76, 2.5),
        "Early Application": (2.51, 3.25),
        "Advanced Application": (3.26, 4.00)
    }
    if score is None:
        return None  # Return None if the score is not available
    for range_name, (lower_bound, upper_bound) in ranges.items():
        if lower_bound <= score <= upper_bound:
            return range_name
    return "Out of Range"  # You might want to handle scores that don't fit any range


def transform_competency(student,evaluator):
    
    time_points = ['pre', 'mid', 'post']
    
    student_responses = {tp: dict(zip(competencies, map(float, resp))) for tp, *resp in student if tp in time_points}
    observer_responses = dict(zip(competencies, map(float, evaluator[0])))

    output = {}

    for comp in competencies:
        output[comp] = {
            "pre": get_range_name(student_responses.get('pre', {}).get(comp, None)),
            "mid": get_range_name(student_responses.get('mid', {}).get(comp, None)),
            "post": get_range_name(student_responses.get('post', {}).get(comp, None)),  # Handle 'post' if exists, else None
            "evaluator": get_range_name(observer_responses.get(comp))
        }
    for key in output['overall_career_readiness_results']:
        if output['overall_career_readiness_results'][key]==None:
            output[key] = False
        else:
            output[key] = True
   
    return output 

def transform_questions(student,observer):
    results = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))
    # Process responses
    for competency, question_number, time, score in student:
        question_name = question_mapping[competency].get(int(question_number), "Unknown Question")
        results[competency][question_name][time] = float(score)  # Convert Decimal to float for easier handling
    
    for competency, question_number, score in observer:
        question_name = observer_question_mapping[competency].get(int(question_number), "Unknown Question")
        results[competency][question_name]["evaluator"] = float(score) 
    
    return results 
 
    
def lambda_handler(event, context):
    
    # data = event.get('body', {})
    data = json.loads(event['body'])
    logger.info(data)

    try:
        student_questions,student_comp,query_params,observer_question,observer_comp = build_query(data)
        student_questions_response = execute_query(student_questions, query_params) 
        student_comp_response = execute_query(student_comp, query_params) 
        observer_comp_response = execute_query(observer_comp, []) 
        observer_questions_response = execute_query(observer_question, []) 
        # logger.info("student_questions_response result: %s", student_questions_response)
        logger.info("student_comp_response query result: %s", student_comp_response)
        logger.info("observer_comp_response query result: %s", observer_comp_response)
        # logger.info("observer_questions_response query result: %s", observer_questions_response)
        
        competencies = transform_competency(student_comp_response,observer_comp_response)
        # logger.info("competencies query result: %s", competencies)
        questions = transform_questions(student_questions_response,observer_questions_response)
        # logger.info("competencies query result: %s", questions)

        competencies.update(questions)


        return {
            'statusCode': 200,
            'body': json.dumps(competencies),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    except Exception as e:
        logger.error("Error processing request: %s", e, exc_info=True)  # Logs stack trace with the error

        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            }),
            'headers': {
                'Content-Type': 'application/json'
            }
        }

