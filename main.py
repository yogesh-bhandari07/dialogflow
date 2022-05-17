from cgitb import handler
from inspect import Parameter
from typing import Any,Dict
from urllib import response
from fastapi import Body,FastAPI,Request,Form
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn
import json
import os
from google.cloud import dialogflow_v2beta1 as dialogflow
from google.api_core.exceptions import InvalidArgument
from fastapi.middleware.cors import CORSMiddleware


def dialogflowChat(query):
    
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'holibasil-26e7b545d7ff.json'

    DIALOGFLOW_PROJECT_ID = 'holibasil'
    DIALOGFLOW_LANGUAGE_CODE = 'en'
    SESSION_ID = 'me'

    text_to_be_analyzed = query

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise

    # print(response)

    simpleMessages=[]
    suggestionsMessages=[]
    listsMessages=[]
    responseDict={
        "simpleMessages":simpleMessages,
        "suggestionsMessages":suggestionsMessages,
        'listsMessages':listsMessages
    }

    countOfMsgs=len(response.query_result.fulfillment_messages)

    

    
        

    count=0
    for i in range(0,countOfMsgs):
        if "text" in response.query_result.fulfillment_messages[i]:
            response.query_result.fulfillment_messages[i]
            count=count+1
        elif "suggestions" in response.query_result.fulfillment_messages[i]:
            response.query_result.fulfillment_messages[i]
            count=count+1 
        elif ('list_select' in response.query_result.fulfillment_messages[0]):

            count=count+1 
        else :
            pass
    
    for i in range(0,count):
        if 'simple_responses' in response.query_result.fulfillment_messages[i]:
            simpleMessages.append(response.query_result.fulfillment_messages[i].simple_responses.simple_responses[0].text_to_speech)

        elif 'text' in response.query_result.fulfillment_messages[i]:
            simpleMessages.append(response.query_result.fulfillment_messages[i].text.text[0])
            # print(response.query_result.fulfillment_messages[i].text.text)


        elif 'suggestions' in response.query_result.fulfillment_messages[i]:
            suggestions_count= len(response.query_result.fulfillment_messages[i].suggestions.suggestions)
            for j in range(0,suggestions_count):
                suggestionsMessages.append(response.query_result.fulfillment_messages[i].suggestions.suggestions[j].title)
                
        elif 'list_select' in response.query_result.fulfillment_messages[i]:
            listsMessages_count= len(response.query_result.fulfillment_messages[i].list_select.items)
            for j in range(0,listsMessages_count):
                listsMessages.append(response.query_result.fulfillment_messages[i].list_select.items[j].title)
                




    return responseDict



app=FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# add static files and templates
app.mount("/static", StaticFiles(directory="./static"), name="static")
templates = Jinja2Templates(directory="./templates")




@app.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})



@app.post('/query',response_class=HTMLResponse)
async def home(request:Request,queryText:str=Form(...)):

    response = dialogflowChat(queryText)

    response["queryText"]=queryText
    
    responseJson = json.dumps(response)

    return responseJson

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)