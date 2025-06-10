from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import sqlite3

def create_sqlite_database():
    # open in-memory database connection
    connection = sqlite3.connect(':memory:')

    with open('titanic.csv', 'r') as file:
        # read the CSV file
        csv_data = file.read()
    
    # separate the lines
    lines = csv_data.split('\n')
    
    # read the header
    header = lines[0]

    # create the table using the header information
    
    # read the remaining lines
    for line in lines[1:]:

        # insert the data in the table
        pass


create_sqlite_database()