from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import sqlite3

def function1():
    # open the database connection
    connection = sqlite3.connect('./students.db')

    # create a cursor object
    cursor = connection.cursor()

    # execute a query
    query = "select name, age, roll_no from students"
    cursor.execute(query)

    # get all the results
    rows = cursor.fetchall()
    print(rows)

    # close the connection
    connection.close()

# function1()


def function2():
    # users question
    question = "who is the topper?"

    # template
    template = """
    You are a sqlite3 developer, writing sqlite3 queries.
    Use the given schema and answer users question.

    Question: {question}
    Schema: {schema}
    Query:

    Generate only the query nothing else.
    """

    # define the schema
    schema = """
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        roll_no INTEGER UNIQUE NOT NULL,
        marks REAL NOT NULL,
        standard TEXT NOT NULL,
        division TEXT NOT NULL
    );
    """
    
    # create the prompt template
    prompt_template = ChatPromptTemplate.from_template(template=template)
    prompt = prompt_template.invoke({"question": question, "schema": schema})

    # create the model
    model = ChatOllama(model="llama3")

    # invoke the prompt and get the result 
    result = model.invoke(prompt)
    query = result.content
    print(f"query = {query}")

function2()