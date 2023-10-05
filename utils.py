from sentence_transformers import SentenceTransformer
import pinecone
import openai
import streamlit as st
import os

os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
openai.api_key = os.getenv('OPENAI_API_KEY')
model = SentenceTransformer('all-MiniLM-L6-v2')

pinecone.init(api_key='509434ef-757b-41f1-ae2f-27827d2c0ff5', environment='us-west4-gcp-free')


index = pinecone.Index('langchain-chatbot')

def find_match(input):
    input_em = model.encode(input).tolist()
    result = index.query(input_em, top_k=2, includeMetadata=True)
    return result['matches'][0]['metadata']['text']+"\n"+result['matches'][1]['metadata']['text']

def query_refiner(conversation, query):
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"Compte tenu de la requête utilisateur et du journal de conversation suivants, formulez une question qui serait la plus pertinente pour fournir à l'utilisateur une réponse à partir d'une base de connaissances.\n\njournal de conversation: \n{conversation}\n\n requête: {query}\n\nune requête raffinée:",
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    return response['choices'][0]['text']

def get_conversation_string():
    conversation_string = ""
    for i in range(len(st.session_state['responses'])-1):
        
        conversation_string += "Human: "+st.session_state['requests'][i] + "\n"
        conversation_string += "Bot: "+ st.session_state['responses'][i+1] + "\n"
    return conversation_string