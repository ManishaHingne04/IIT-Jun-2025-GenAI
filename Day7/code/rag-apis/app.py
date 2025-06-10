from database import Database
from flask import Flask, request
from flask_cors import CORS
from rag_pipeline import RagPipeline

# create the database connection
database = Database()

# create the RAG pipeline
pipeline = RagPipeline()

# create the flask app
app = Flask(__name__)

# enable CORS
CORS(app)

@app.route('/', methods=['GET'])
def root():
    return "Welcome to the RAG APIs"

@app.route('/ask-question', methods=['POST'])
def ask_question():
    # get the question from request json
    question = request.json.get('question')

    # prepare the query
    query = pipeline.create_query(question)
    print(f"Query: {query}")

    # get the result
    result = database.execute_query(query)
    print(f"Result: {result}")

    # format the result
    formatted_result = pipeline.format_result(question, query, result)
    print(f"Formatted Result: {formatted_result}")

    return formatted_result


# start the app
app.run(port=8090, host="0.0.0.0", debug=True)

