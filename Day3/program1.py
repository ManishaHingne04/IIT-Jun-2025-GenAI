# import required packages
from langchain_ollama import ChatOllama

# create the model 
llm = ChatOllama(model="llama3")

# get prompt from user
prompt = input("Enter your input: ")

# pass the prompt to the model
response = llm.invoke(prompt)

# show the result to the user
print(response.content)