import boto3
import json
from html_file import html_template

def lambda_handle_template(event, context):
    ses_client = boto3.client('ses', region_name='us-east-1')  # Ensure this is your SES region

    # Example event input that might contain double quotes in HTML
    template_name = 'CareerReadinessTemplate'
    subject_part = 'Career Readiness Inventory Report'
    html_part = html_template
    text_part = 'Hi {{student_first_name}},\nThank you for taking time to reflect on the skills employers value the most. Here is your report site where you can view your results:\n{{report_link}}\nThank you,\nCareer Launch'

    template_data = {
        'TemplateName': template_name,
        'SubjectPart': subject_part,
        'TextPart': text_part,
        'HtmlPart': html_part
    }

    try:
        # Create or update the template
        response = ses_client.update_template(Template={'TemplateName': template_name,
                                                       'SubjectPart': subject_part,
                                                       'TextPart': text_part,
                                                       'HtmlPart': html_part})
        return {
            'statusCode': 200,
            'body': json.dumps('Template updated successfully.')
        }
    except ses_client.exceptions.TemplateDoesNotExistException:
        # If the template does not exist, create it
        ses_client.create_template(Template=template_data)
        return {
            'statusCode': 200,
            'body': json.dumps('Template created successfully.')
        }
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {
            'statusCode': 400,
            'body': json.dumps(f"An error occurred: {str(e)}")
        }


def send_email():
    ses_client = boto3.client('ses', region_name='us-east-1')
    template_name = 'CareerReadinessTemplate'  
    recipient = 'aishwaryagupta720@gmail.com'
    template_data = {
        'name': 'Aishwarya',
        'report_link': 'https://app.careerreadinessinventory.academy/reportr-download/f41b1e90-b648-4c54-b6bc-bce044021236/21754540-8b81-4090-8184-022b849ab2a7'
    }

    try:
        response = ses_client.send_templated_email(
            Source='aishwaryagupta720@gmail.com',
            Destination={'ToAddresses': [recipient]},
            Template=template_name,
            TemplateData=json.dumps(template_data)
        )
        print('Email sent! Message ID:', response['MessageId'])
    except Exception as e:
        print('Error sending email:', e)


def lambda_handler(event, context):
    send_email()
