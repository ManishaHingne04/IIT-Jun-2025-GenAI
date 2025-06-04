from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# create the model 
model = ChatOllama(model="llama3")

while True:
    prompt = input(">>> ")
    if prompt.lower() == 'exit':
        break

    # sending the whole conversation to the model
    response = model.invoke(prompt)

    print(response.content)

print("Goodbye!")