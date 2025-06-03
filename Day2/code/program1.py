# import required packages
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI

# load all the keys from .env file
load_dotenv()

# print(os.getenv('OPENAI_API_KEY'))

# create an object of ChatOpenAI to access the LLM
llm = ChatOpenAI(model="gpt-4o", max_completion_tokens=100)

# prompt: input to the LLM
prompt = "what is special about 19 march?"

# invoke the LLM to get the response
response = llm.invoke(prompt)

# read only the answer from the response
print(response.content)