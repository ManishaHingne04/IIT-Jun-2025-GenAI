from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import sqlite3

# open the database connection
connection = sqlite3.connect('./students.db')

# create the model
model = ChatOllama(model="llama3")

# template to create the query
query_template = """
You are a sqlite3 developer, writing sqlite3 queries.
Use the given schema and answer users question.

Question: {question}
Schema: {schema}
Query:

Generate only the query nothing else.
"""

# template to format the result
result_template = """
You are a database summarizer.
Given the users question, generated query and results found, you need to format the results accordingly.

Following are some examples:

Question: what is the toppers name?
Query: select name from students where marks = (select max(marks) from students)
Results: [('John',)]
Formatted result: The toppers name is John.

Question: {question}
Query: {query}
Results: {results}

Print only the formatted results nothing else.
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

CREATE TABLE IF NOT EXISTS addresses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    studentId INTEGER,
    street TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    pinCode INTEGER NOT NULL,
    FOREIGN KEY (studentId) REFERENCES students(id)
);
"""


def generate_query(question):    
    # create the prompt template
    prompt_template = ChatPromptTemplate.from_template(template=query_template)
    prompt = prompt_template.invoke({"question": question, "schema": schema})

    # invoke the prompt and get the result 
    result = model.invoke(prompt)
    query = result.content
    # print(f"query = {query}")

    return query


def execute_query(query):
    print(f"query = {query}")

    # create a cursor object
    cursor = connection.cursor()

    # execute a query
    cursor.execute(query)

    # get all the results
    rows = cursor.fetchall()

    # commit the database
    # connection.commit()
    
    return rows


def format_result(question, query, results):
    # create the result prompt template
    prompt_template = ChatPromptTemplate.from_template(template=result_template)
    prompt = prompt_template.invoke({"question": question, "query": query, "results": results})
    
    # invoke the prompt and get the result
    final_result = model.invoke(prompt)
    print(final_result.content)


while True:
    # get the question from user
    question = input("Enter your question: ")

    if question == "exit":
        break

    # generate the query using the model
    query = generate_query(question)

    # answer the user's question
    results = execute_query(query)
    
    # format the results
    format_result(question, query, results)

# close the connection
connection.close()