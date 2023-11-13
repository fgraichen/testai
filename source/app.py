
import json
import boto3
from botocore.exceptions import ClientError





from typing import Tuple

#even though this app is not using langchain - it is using the promp template feature for formatting prompts
from langchain.prompts import PromptTemplate

target_region = "us-east-1"
session_kwargs = {"region_name": target_region}
endpoint_url = 'https://bedrock-runtime.us-east-1.amazonaws.com'


session = boto3.Session(**session_kwargs)
client_kwargs = {**session_kwargs}

client_kwargs["endpoint_url"] = endpoint_url
boto3_bedrock = session.client(
        service_name="bedrock-runtime",
        **client_kwargs
    )




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
    artist = event['data']
    print(f"Artist is {artist}")
   
    response = run(artist)
  
    return {
        "statusCode": 200,
        "body": json.dumps({
            "data": response,
            # "location": ip.text.replace("\n", "")
        }),
    }


    
def run( 
        prompt: str,
        ) -> Tuple[str, str]:
    
    print('in run function')
      
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
    print("prompt into claude", test_prompt)
    body = json.dumps({"prompt": test_prompt, "max_tokens_to_sample": 500, 
         "temperature": 1,
         "top_k": 250,
         "top_p": 1,
         "stop_sequences": ["\n\nHuman:"],})
    
    modelId = "anthropic.claude-instant-v1"  # change this to use a different version from the model provider
    accept = "application/json"
    contentType = "application/json"
    
    print("Before claud invoke")
    try:
       response = boto3_bedrock.invoke_model(
         body=body, modelId=modelId, accept=accept, contentType=contentType
         )
       print("response after model invoke", response)
       response_body = json.loads(response.get("body").read())
       # each model returns code in a different format - Claude return the object in a completion field
       response = response_body.get("completion")
    except ClientError as e:
        print(e)
        return e
    print("response being returned", response)
    print("reponse", response)
    return response
    
    
   

    
    
