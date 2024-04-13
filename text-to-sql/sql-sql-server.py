from operator import itemgetter

from langchain_community.utilities import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI


from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

from langchain_community.llms import Ollama

db = SQLDatabase.from_uri("mssql+pymssql://ia2:Password!@localhost:1433/ComputerDB") # Cadena de conexión
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
# llm = Ollama(model="llama2")

execute_query = QuerySQLDataBaseTool(db=db)
write_query = create_sql_query_chain(llm, db)

answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
)

answer_query = answer_prompt | llm | StrOutputParser()

chain = (
    RunnablePassthrough.assign(query=write_query).assign(
        result=itemgetter("query") | execute_query
    )
    | answer_query
)

# Get the question from the command line
question = input("Dame una pregunta: ")

response = chain.invoke({"question": question})
print(response)
