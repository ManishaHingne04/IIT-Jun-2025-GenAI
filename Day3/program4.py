from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# create the model 
model = ChatOllama(model="llama3", temperature=0.5)

# create a collection to maintain the history of the conversation
messages = [
    # note: this line is optional
    SystemMessage(content="You are an assistant"),
]

while True:
    prompt = input(">>> ")
    if prompt.lower() == 'exit':
        break

    # add the input from user to the messages collection
    messages.append(HumanMessage(content=prompt))

    # sending the whole conversation to the model
    response = model.invoke(messages)
    
    # append the result to the messages conversion
    messages.append(AIMessage(content=response.content))
    
    print(response.content)

print("Goodbye!")