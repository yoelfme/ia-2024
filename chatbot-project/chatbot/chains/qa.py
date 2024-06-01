import getpass
import os
# import bs4

# Importando todas los modulos necesarios de Langchain 
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.vectorstores import utils as chromautils

# Para cargar documentos de Excel
from langchain_community.document_loaders import UnstructuredExcelLoader

# Para cargar PDFs
from langchain_community.document_loaders import PyPDFLoader

# Obtener el API Key de OpenAI
os.environ["OPENAI_API_KEY"] = getpass.getpass('OPEN_AI_API_KEY:')

# Crear un objeto LLM de OpenAI
llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

# **** CARGAR INFORMACION DE UN EXCEL ****
# Leer nuestra informacion, en este caso nuestros archivos de Excel
loader = UnstructuredExcelLoader("resources/transportation/info.xlsx", mode="elements")
docs = loader.load()

# Filtrar los metadatos complejos como ['spa'] que obtenemos de Excel
docs = chromautils.filter_complex_metadata(docs)
# **** CARGAR INFORMACION DE UN EXCEL ****

# # **** CARGAR INFORMACION DE UN PDF ****
# loader = PyPDFLoader("resources/jewelry/info.pdf")
# docs = loader.load_and_split()
# # **** CARGAR INFORMACION DE UN PDF ****

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

text = format_docs(docs)

# Partir los documentos en multiles partes para que el chatbot pueda procesarlos
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

# Obtener y generar usando los fragmentos relevantes del Excel
retriever = vectorstore.as_retriever()
prompt = hub.pull("rlm/rag-prompt")


chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
