# program to demonstrate the LLM halucination 

from langchain_ollama import ChatOllama

# create a model
model = ChatOllama(model="llama3")

# create a prompt
prompt = "who is John Kulkarni?"

# ask the question to the model
response = model.invoke(prompt)

# print the response
print(f"response: {response.content}")