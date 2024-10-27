import requests
import json

# Define the URL of the API endpoint
url = 'https://defskuiy20.execute-api.us-east-1.amazonaws.com/dev/post-student-data'

# Create the data payload as a dictionary, and then convert it into a JSON string
data = json.dumps({
    "body": {
        "outcomes": [
            {
                "title": "Successful Submission"
            },
        ]
            
        },
    "headers": {
        "Content-Type": "application/json"
    },
    "httpMethod": "POST",
    "path": "/post-student-data",
    "queryStringParameters": {
        "sampleParam": "value"
    },
    "pathParameters": {
        "samplePathKey": "value"
    },
    "stageVariables": {
        "stageVariable1": "value"
    },
    "requestContext": {
        "accountId": "123456789012",
        "resourceId": "xyz123",
        "stage": "dev",
        "requestId": "c6af9ac6-7b61-11e6-9a3e-71f2b348d123",
        "identity": {
            "sourceIp": "123.123.123.123"
        },
        "resourcePath": "/post-student-data"
    }
})

# Make a POST request to the API endpoint
response = requests.post(url, data=data, headers={'Content-Type': 'application/json'})

# Print the status code and response data
print("Status Code:", response.status_code)
print("Response Body:", response.json())
