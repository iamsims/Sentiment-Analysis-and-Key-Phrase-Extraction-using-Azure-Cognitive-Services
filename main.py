import streamlit as st
import pandas as pd
import numpy as np
import urllib.parse, http.client, urllib.request, urllib.error, json
import requests
import json
from string import punctuation

textAnalyticsEndpoint = 'textprocessinginstance.cognitiveservices.azure.com'
textAnalyticsKey = st.secrets["textAnalyticsKey"]

def spell_correct(data):
    api_key = st.secrets["spellCheckKey"]
    endpoint = "https://api.bing.microsoft.com/v7.0/SpellCheck"

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Ocp-Apim-Subscription-Key': api_key,
    }

    text = {'text': data}
    params = {
    'mkt':'en-us',
    'mode':'proof'
    }
    response = requests.post(endpoint, headers=headers, params=params, data=text)

    json_response = response.json()

    for token in json_response['flaggedTokens']:
        data = data.replace(token['token'], token['suggestions'][0]['suggestion'])


    if (json_response['flaggedTokens']!=[]):
        st.write("You probably meant: "+ data)
   
    return data

def key_extraction(data):
    headers = {
    'Content-Type' : 'application/json',
    'Ocp-Apim-Subscription-Key' : textAnalyticsKey,
    }
    body = {
        'documents' : [
          {
              'language' : 'en',
              'id' : '1',
              'text' : data
          },       
        ]
    }

    try:
        conn = http.client.HTTPSConnection(textAnalyticsEndpoint)
        conn.request('POST', '/text/analytics/v3.0/keyPhrases', str(body), headers)
        response = conn.getresponse()

        jsonData = response.read().decode('UTF-8') #decoded to bytes to strings 
        data = json.loads(jsonData)

        document = data['documents'][0]
        result = [x for x in document['keyPhrases']]
        conn.close()
        return result

    except Exception as ex:
        print(ex)



def sentiment_analyze(data):
    headers = {
    'Content-Type' : 'application/json',
    'Ocp-Apim-Subscription-Key' : textAnalyticsKey,
            }

    body = {
        'documents' : [
          {
              'language' : 'en',
              'id' : '1',
              'text' : data
          },       
        ]
    }


    try:
        conn = http.client.HTTPSConnection(textAnalyticsEndpoint)
        conn.request('POST', '/text/analytics/v3.0/sentiment', str(body), headers)
        response = conn.getresponse()
        jsonData = response.read().decode('UTF-8') 
        data = json.loads(jsonData)

        document = data['documents'][0]
        # result = document['sentiment']
        conn.close()
        return document

    except Exception as ex:
        print(ex)





def clean (data):
    try:
        data = spell_correct(data)
        data = ''.join(c for c in data if c==" " or (c.isalpha() and c!=" ")).lower()
        return data

    except Exception as ex:
        print(ex)


st.title('Sentiment Analysis & Key Phrases Extraction')
st.header("Enter the text below! ")
data = st.text_area("", "")

operation = st.selectbox("", ('Sentiment Analysis', 'Key Phrase Extraction', 'Whole analysis'))

if st.button('Perform'):
    data = clean(data)

    with st.spinner("Computing Results"):

        if operation == 'Sentiment Analysis' or operation == "Whole analysis":
            result = sentiment_analyze(data)
            print(result)




            if result['sentiment']=="negative":
              emoji =":pensive:"
            if result['sentiment']=="neutral":
              emoji =":neutral_face:"
            if result['sentiment']=="positive":
              emoji =":grin:"
            st.write(emoji + "  "+ result['sentiment'] + " statement! ")


        if operation == 'Key Phrase Extraction' or operation == "Whole analysis":
            result = key_extraction(data)
            


            
      