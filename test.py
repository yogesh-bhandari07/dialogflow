import os
from google.cloud import dialogflow_v2beta1 as dialogflow
from google.api_core.exceptions import InvalidArgument

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'holibasil-26e7b545d7ff.json'

DIALOGFLOW_PROJECT_ID = 'holibasil'
DIALOGFLOW_LANGUAGE_CODE = 'en'
SESSION_ID = 'me'

text_to_be_analyzed = "hello"

session_client = dialogflow.SessionsClient()
session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
query_input = dialogflow.types.QueryInput(text=text_input)
try:
    response = session_client.detect_intent(session=session, query_input=query_input)
except InvalidArgument:
    raise



countOfMsgs=len(response.query_result.fulfillment_messages)
count=0
for i in range(0,countOfMsgs):
    if "platform" in response.query_result.fulfillment_messages[i]:
        print(response.query_result.fulfillment_messages[i])
        count=count+1
    else :
        pass

for i in range(0,count):
    if 'simple_responses' in response.query_result.fulfillment_messages[i]:
        print(response.query_result.fulfillment_messages[i].simple_responses.simple_responses[0].text_to_speech)
    elif 'suggestions' in response.query_result.fulfillment_messages[i]:
        suggestions_count= len(response.query_result.fulfillment_messages[i].suggestions.suggestions)
        for j in range(0,suggestions_count):
            print(response.query_result.fulfillment_messages[i].suggestions.suggestions[j].title)



