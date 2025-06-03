from langchain_ollama import OllamaLLM

# create an object of OllamaLLM to access the LLM
# llm = OllamaLLM(model="llama3")
llm = OllamaLLM(model="deepseek-r1")

# create the prompt
prompt = "what is your name?"

# execute the prompt
response = llm.invoke(prompt)
print(response)

