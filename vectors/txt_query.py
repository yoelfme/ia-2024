# Para poder cargar mi API Key de OpenAI
import os
import getpass

os.environ['OPENAI_API_KEY'] = getpass.getpass('OpenAI API Key:')

# Modulo para cargar documentos 
# Para PDFs: (https://python.langchain.com/docs/modules/data_connection/document_loaders/pdf)
from langchain_community.document_loaders import TextLoader

# Modulo para generar Embeddings
from langchain_openai import OpenAIEmbeddings

# Modulo para dividir el documento en partes
from langchain_text_splitters import CharacterTextSplitter

# Modulo para la Base de Datos de Vectores
from langchain_community.vectorstores import Chroma

# Cargar el documento
raw_documents = TextLoader('./resources/state_of_the_union.txt').load()

# Dividir el documento en chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
documents = text_splitter.split_documents(raw_documents)

# Embedir y cargar cada chunk en la base de datos
db = Chroma.from_documents(documents, OpenAIEmbeddings())

# Realizaremos una consulta
query = "What did the president say about Ketanji Brown Jackson"
docs = db.similarity_search(query)
print(docs[0].page_content)