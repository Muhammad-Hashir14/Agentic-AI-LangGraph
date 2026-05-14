import streamlit as st
from langgraph_backend import chatbot
from langchain_core.messages import HumanMessage
import uuid
# st.session_state -> dict -> 


#helper funtions

def generate_threadid():

    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_threadid()
    st.session_state["chat_threads"].append(thread_id)
    st.session_state['thread_id'] = thread_id
    st.session_state['message_history'] = []

def add_threads(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

def load_conversations(thread_id):
    CONFIG = {'configurable': {'thread_id': thread_id}}
    state_values = chatbot.get_state(config=CONFIG).values
    messages = state_values.get('messages', [])
    message_history = []
    for message in messages:
        if message.type == 'human':
            message_history.append({'role': 'user', 'content': message.content})
        else:
            message_history.append({'role': 'assistant', 'content': message.content})

    st.session_state['message_history'] = message_history
    st.session_state['thread_id'] = thread_id



if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_threadid()

if "chat_threads" not in st.session_state:
    st.session_state['chat_threads'] = []

add_threads(st.session_state['thread_id'])


# loading the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

st.sidebar.title("LangGraph Chatbot")

if st.sidebar.button("New Chat"):
    reset_chat()
    st.rerun()

st.sidebar.text("My Conversations")
for thread_id in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(thread_id)):
        load_conversations(thread_id)
        st.rerun()

#{'role': 'user', 'content': 'Hi'}
#{'role': 'assistant', 'content': 'Hi=ello'}

user_input = st.chat_input('Type here')
CONFIG = {'configurable': {'thread_id': st.session_state["thread_id"]}}


if user_input:

    # first add the message to message_history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    response = chatbot.invoke({'messages': [HumanMessage(content=user_input)]}, config=CONFIG)
    
    ai_message = response['messages'][-1].content
    # first add the message to message_history
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
    with st.chat_message('assistant'):
        st.text(ai_message)