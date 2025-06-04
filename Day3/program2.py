# prompt
# - input given to the LLM
# - types
#   - SystemPrompt or SystemMessage
#     - used to set the context of the conversation
#   - HumanPrompt or HumanMessage
#     - used to send the input from user
#   - AIPrompt or AIMessage
#     - answer given by the LLM

from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# create the model
llm = ChatOllama(model="llama3")

def function1():
    # sending the messages using tuples
    messages = [
        # setting the context of the conversation
        ("system", "You are a comedian"),

        # sending the input from user
        ("human", "tell me a joke about python"),
    ]

    # invoke the model
    response = llm.invoke(messages)
    print(response.content)

# function1()    


def function2():
    messages = [
        # setting the context of the conversation
        SystemMessage(content="You are a comedian"),

        # sending the input from user
        HumanMessage(content="tell me a joke about python"),
    ]

    # invoke the model
    response = llm.invoke(messages)
    print(response.content)

function2()