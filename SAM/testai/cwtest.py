#use region us-east-1 to connect to dynamodb
import boto3
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

#create python funtion update_pettracker_table(prompt, result)    
import boto3
import datetime



def update_pettracker_table(prompt, result):
    print("update")
#update  dynamodb table named pettracker with a new entry with model_id = "anthropic.claude-v1" and DT = str(datetime.now()) and prompt = prompt and result = result           
    table = dynamodb.Table('PetTracker')
    table.put_item(Item={'Model-Id': 'anthropic.claude-instant-v1', 'DT': str(datetime.datetime.now()), 'prompt': prompt, 'result': result})
    return "success"    



#create function to scan dynamodb table named pettracker and return all items
def scan_dynamodb_table():
    print("scan ")
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('PetTracker')
    response = table.scan()
    return response['Items']

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

#use try catch logic to call update_pettracker_table() and return the result        
try:
    result = update_pettracker_table("cat", "cat")
    print(result)       
    
except Exception as e:
    print("Error updating tracker table", e)
    
else:
    print("successfully updated table")

#call scan_dynamodb_table(pettracker) and iterate through the items and print each item 

print("scan")   

result = scan_dynamodb_table()

for item in result:
    print(item)
    
#call update_pettracker_table(prompt, result) and print the result
#update_pettracker_table("cat", "cat")
#scan_dynamodb_table()

