from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
import json

class RagPipeline():
    def __init__(self):
        # get the model
        self.__model = ChatOllama(model="llama3")

        # load the config
        self.__load_config()

        # get the prompt templates
        self.__query_prompt = self.__config["queryPrompt"]
        self.__result_prompt = self.__config["resultPrompt"]

    def __get_schema(self):
        return """
        CREATE TABLE employee (
            id INT AUTO_INCREMENT,
            name VARCHAR(255),
            email VARCHAR(255),
            salary DECIMAL(10,2),
            address VARCHAR(255),
            phone VARCHAR(20),
            PRIMARY KEY (id)
        );
        """

    def __load_config(self):
        # load the config file
        with open("config.json", "r") as f:
            self.__config = json.load(f)

    def create_query(self, question):
        # create the prompt
        prompt_template = ChatPromptTemplate.from_template(template=self.__query_prompt)
        prompt = prompt_template.invoke({
            "question": question, 
            "table": "employee", 
            "schema": self.__get_schema()
        })

        # get the query
        response = self.__model.invoke(prompt)

        return response.content
    
    def format_result(self, question, query, results):
        # create the prompt
        prompt_template = ChatPromptTemplate.from_template(template=self.__result_prompt)
        prompt = prompt_template.invoke({
            "question": question, 
            "query": query, 
            "results": results
        })

        # get the result
        response = self.__model.invoke(prompt)
        
        return response.content
