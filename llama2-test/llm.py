from langchain_community.llms import Ollama # LLM 
from langchain_core.prompts import ChatPromptTemplate # Prompt 
from langchain_core.output_parsers import StrOutputParser # Parser


llm = Ollama(model="llama2")

prompt = ChatPromptTemplate.from_messages([
    ("system", "Tu eres un guia turistico enfocado en el area de la Costa Sur en Guatemala, debes de responder todo en español"),
    ("user", "{input}")
])

output_parser = StrOutputParser()

chain = prompt | llm | output_parser

response = chain.invoke({
    "input": "Me puedes dar informacion sobre los lugares turisticos en la Costa Sur de Guatemala?"
})

print(response)
