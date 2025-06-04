import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# Create a new ChatOllama object
model = ChatOllama(model="llama3")

# maintain the history of the conversation
# messages = []

# write the title
st.title("My Chatbot")
st.header("Welcome to my chatbot!")

# get the user input
prompt = st.chat_input("Enter your prompt")
if prompt:

    # get the response from the model
    response = model.invoke(f"{prompt}. Answer the question in one line.")

    # write the response to the screen
    st.write(response.content)