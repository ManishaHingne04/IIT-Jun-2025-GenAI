from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import sqlite3
import pandas as pd

# create in-memory database connection
connection = sqlite3.connect(':memory:')

# create the model
model = ChatOllama(model="llama3")

# template to create the query
query_template = """
You are a sqlite3 developer, writing sqlite3 queries.
Use the given schema and answer users question.

Question: {question}
Table: {table_name}
Schema: {schema}
Query:

Generate only the query nothing else.
"""

# template to format the result
result_template = """
You are a database summarizer.
Given the users question, generated query and results found, you need to format the results accordingly.

Question: {question}
Query: {query}
Results: {results}

Print only the formatted results nothing else.
"""

def create_sqlite_database(file_name, table_name):
    # read the CSV file into a DataFrame
    df = pd.read_csv(file_name)

    # create the table and insert the data
    df.to_sql(table_name, connection, index=False, if_exists='replace')

file_name = 'titanic.csv'

# extract the file name to name the table
table_name = file_name.split('.')[0]
create_sqlite_database(file_name='titanic.csv', table_name=table_name)


def extract_schema_from_database():
    # get the table schema
    cursor = connection.cursor()

    # get the table schema
    cursor.execute(f"PRAGMA table_info({table_name})")

    # fetch the schema
    result = cursor.fetchall()
    
    # format the schema (list of dictionaries)
    schema = [{"column": info[1], "type": info[2]} for info in result]

    # close the cursor
    cursor.close()

    return schema

def generate_query(question):
    # create the prompt
    prompt_template = ChatPromptTemplate.from_template(template=query_template)
    prompt = prompt_template.invoke({
        "question": question,
        "table_name": table_name,
        "schema": extract_schema_from_database()
    })

    # get the query from the model
    response = model.invoke(prompt)

    # return the query
    return response.content

def execute_query(query):
    # get the cursor
    cursor = connection.cursor()

    # execute the query
    cursor.execute(query)

    # get the result
    result = cursor.fetchall()

    # close the cursor
    cursor.close()

    return result

def format_result(question, query, result):
    # create the prompt
    prompt_template = ChatPromptTemplate.from_template(template=result_template)
    prompt = prompt_template.invoke({
        "question": question,
        "query": query,
        "results": result
    })

    # get the formatted result from the model
    response = model.invoke(prompt)

    # return the formatted result
    return response.content


while True:
    # get the question from the user
    question = input("Enter your question (or 'exit' to quit): ")

    # check if the user wants to exit
    if question.lower() == 'exit':
        break

    # generate the query
    query = generate_query(question)

    # execute the query
    result = execute_query(query)

    # format the result
    formatted_result = format_result(question, query, result)

    # print the formatted result
    print(formatted_result)
    print("-" * 80)


# close the connection
connection.close()
