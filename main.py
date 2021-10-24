import streamlit as st
import pandas as pd
import numpy as np
import urllib.parse, http.client, urllib.request, urllib.error, json

textAnalyticsEndpoint = 'textprocessinginstance.cognitiveservices.azure.com'
textAnalyticsKey = st.secrets["textAnalyticsKey"]


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
        result = " ".join(x for x in document['keyPhrases'])
        conn.close()

    except Exception as ex:
        print(ex)
        return ""

    return result


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
        result = document['sentiment']
        conn.close()

    except Exception as ex:
        print(ex)
        return ""

    return result


from string import punctuation


def clean (data):
    cleaned_data = ''.join(c for c in data if c==" " or (c.isalpha() and c!=" ")).lower()
    return cleaned_data



st.set_page_config(page_title=None, page_icon=None, layout='centered', initial_sidebar_state='auto', menu_items=None)
st.title('Sentiment Analysis & Key Phrases Extraction')

st.header("Enter the text below! ")
data = st.text_area("", "")

data = clean(data)

operation = st.selectbox("", ('Sentiment Analysis', 'Key Phrase Extraction', 'Whole analysis'))

if st.button('Perform'):

    with st.spinner("Computing Results"):
        if operation == 'Sentiment Analysis' or operation == "Whole analysis":
            result = sentiment_analyze(data)
            if result=="negative":
              emoji =":pensive:"
            if result=="neutral":
              emoji =":neutral_face:"
            if result=="positive":
              emoji =":grin:"
            st.write(emoji + "  "+ result + " statement! ")


        if operation == 'Key Phrase Extraction' or operation == "Whole analysis":
            result = key_extraction(data)
            st.write(result)
      