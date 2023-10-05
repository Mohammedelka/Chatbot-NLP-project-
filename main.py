from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory,ConversationSummaryBufferMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
import streamlit as st
from streamlit_chat import message
from utils import *
# st.subheader("Depf Chatbot with Langchain, ChatGPT, Pinecone, and Streamlit")
st.subheader("Le DepfChatBot Votre assistant virtuel")
st.subheader("La Direction des Etudes et des Prévisions Financières (DEPF)")


if 'responses' not in st.session_state:
    st.session_state['responses'] = ["comment je peux vous aider?"]

if 'requests' not in st.session_state:
    st.session_state['requests'] = []

llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=os.getenv('OPENAI_API_KEY'))

if 'buffer_memory' not in st.session_state:
            st.session_state.buffer_memory=ConversationBufferWindowMemory(k=3,return_messages=True)

\


system_msg_template = SystemMessagePromptTemplate.from_template(template="""Je m'appelle DepfBot un assistant financier de La Direction des Etudes et des Prévisions Financières (DEPF)\
                                                                Répondez à la question le plus sincèrement possible en utilisant le contexte fourni,
et si la réponse n'est pas contenue dans le texte ci-dessous, dites 'peut être la question n'est pas assez claire !'\'""")


human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")

prompt_template = ChatPromptTemplate.from_messages([system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template])

conversation = ConversationChain(memory=st.session_state.buffer_memory, prompt=prompt_template, llm=llm, verbose=True)




# container for chat history
response_container = st.container()
# container for text box
textcontainer = st.container()


with textcontainer:
    query = st.text_input("Query: ", key="input")
    if query:
        with st.spinner("je type ..."):
            conversation_string = get_conversation_string()
            # st.code(conversation_string)
            refined_query = query_refiner(conversation_string, query)
            #st.subheader("Requête raffinée:")
            #st.write(refined_query)
            context = find_match(refined_query)
            #st.subheader("Context:")
            #st.write(context)
            #print(context)  
            response = conversation.predict(input=f"Context:\n {context} \n\n Query:\n{query}")
        st.session_state.requests.append(query)
        st.session_state.responses.append(response) 
with response_container:
    if st.session_state['responses']:

        for i in range(len(st.session_state['responses'])):
            message(st.session_state['responses'][i],key=str(i))
            if i < len(st.session_state['requests']):
                message(st.session_state["requests"][i], is_user=True,key=str(i)+ '_user')

          