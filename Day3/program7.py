from flask import Flask, render_template, request
from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

# create the ollama model
model = ChatOllama(model="llama3")

# maintain the chat conversation
messages = [
    SystemMessage(content="You are a assistant chatbot")
]

# create a flask application
app = Flask(__name__)

@app.route('/', methods=['GET'])
def root():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():

    # get the message sent by the user
    message = request.json['message']

    # append the message to the conversation
    messages.append(HumanMessage(content=message))
    
    # invoke the model
    response = model.invoke(messages)

    # get the response and add it back to the messages
    messages.append(AIMessage(content=response.content))

    return { 'result': response.content }


# start the flask app
app.run(host="0.0.0.0", port=5400, debug=True)
