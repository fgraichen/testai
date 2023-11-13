
import json
import os
#from typing import Dict
import boto3
from botocore.exceptions import ClientError

#bedrock imports
# -- I just included the code from utils import bedrock, print_ww
#from botocore.config import Config
from typing import Optional
#import requests
from typing import Tuple
#from uuid import uuid4
#even though this app is not using langchain - it is using the promp template feature for formatting prompts
from langchain.prompts import PromptTemplate

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('pettracker')

import datetime
import time


bedrock_client = boto3.client(service_name='bedrock-runtime')


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
   

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e
    print(f"event is {event}")
    body = event
    artist = event['data']
    print(f"Artist is {artist}")
    aws_region = "us-east-1"
    model_id = "anthropic.claude-v1"
   
    

   
    #Assuming a role - likely don't need these anymore
    #bedrock_key_json=get_secret('bedrock-keys')
    #bedrock_assumed_role=bedrock_key_json['assumed_role']

    #if you have to used keys for your client access  - this implementation assume a role
    #bedrock_access_key=bedrock_key_json['bedrock_access_key']
    #bedrock_secret_key=bedrock_key_json['bedrock_secret_key']


    response = run(artist)
    #return response
    return {
        "statusCode": 200,
        "body": json.dumps({
            "data": response,
            # "location": ip.text.replace("\n", "")
        }),
    }



def update_pettracker_table(prompt, result):    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('pettracker')
    timestamp = str(datetime.datetime.now())
    response = table.put_item(
       Item={
            'model_id': 'claude',
            'DT': timestamp,
            'prompt': prompt,
            'result': result
        }
    )
    return response


    


    
def run( 
        prompt: str,
        ) -> Tuple[str, str]:
    
    
    human_prompt = """You are a pet naming expert whose sole purpose is to create a pet name based on the name of the song provided. 
                   Rules: 
                   1 The name must be creative 
                   2 you must provide at least four options 3 length of name should not exceed two syllables 
                   4 your choice should take into account the lyrics of the song and not just the title 
                   5 explain your choices 
                   6 The song you are basing your selection on is {title}
                   Here is an example
                  <Example>
                   Human: Dear Prudence by the Beatles
                   Assistant:
                   Prudy
                   Sunshine
                   Dearie
                   Sunny
                   <\example>""".format(title=prompt)
    prompt_template = PromptTemplate.from_template(
       "\n\nHuman:{input}\n\nAssistant:")   
    test_prompt = prompt_template.format(input=human_prompt)
    body = json.dumps({"prompt": test_prompt, "max_tokens_to_sample": 500, 
         "temperature": 1,
         "top_k": 250,
         "top_p": 1,
         "stop_sequences": ["\n\nHuman:"],})
    modelId = "anthropic.claude-instant-v1"  # change this to use a different version from the model provider
    accept = "application/json"
    contentType = "application/json"
    
    response = bedrock_client.invoke_model(
      body=body, modelId=modelId, accept=accept, contentType=contentType
      )
   
    response_body = json.loads(response.get("body").read())
    
    response = response_body.get("completion")
    #response_data = response.get["data"]
    #print("response data", response_data)
    print("response being returned", response)
    
#invoke the update_tracker_table with try catch logic   
    try:
       update_pettracker_table(test_prompt, response)
    except Exception as e:
       print("Error updating tracker table", e)
    else:
       print("successfully updated table")
    #response = {
    #    "statusCode": 200,
    #    body: json.dumps(response)
    #}
    print("reponse", response)
    return response
    
    
   

    
    
