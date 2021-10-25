import streamlit as st
import pandas as pd
import numpy as np
import urllib.parse, http.client, urllib.request, urllib.error, json
import requests
import json
from string import punctuation
import matplotlib.pyplot as plt


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
        conn.close()
        return document

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
            st.header("Sentiment Analysis")
            labels = 'Negative', 'Neutral', 'Positive'
            sizes = [result['confidenceScores']['negative'], result['confidenceScores']['neutral'], result['confidenceScores']['positive']]

            fig1, ax1 = plt.subplots()
            colors = ['red', 'blue', 'green', 'yellow']
            patches, text= ax1.pie(sizes, colors= colors, startangle=90)
            ax1.legend(patches, labels, loc="best")

            
            ax1.axis('equal')  
            st.pyplot(fig1)
            
        


            if result['sentiment']=="negative":
              emoji =":pensive:"
            if result['sentiment']=="neutral":
              emoji =":neutral_face:"
            if result['sentiment']=="positive":
              emoji =":grin:"
            st.info(emoji + "  "+ result['sentiment'] + " statement! ")


        if operation == 'Key Phrase Extraction' or operation == "Whole analysis":

            document = key_extraction(data)
            print(document)
            result = [x for x in document['keyPhrases']]

            
            



# # Pie chart, where the slices will be ordered and plotted counter-clockwise:
# labels = 'Negative', 'Neutral', 'Positive'
# sizes = [15, 30, 45]
# explode = (0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

# fig1, ax1 = plt.subplots()
# ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
#         shadow=True, startangle=90)
# ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# st.pyplot(fig1)
      