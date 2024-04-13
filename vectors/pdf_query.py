# Para poder cargar mi API Key de OpenAI
import os
import getpass

os.environ['OPENAI_API_KEY'] = getpass.getpass('OpenAI API Key:')

# Modulo para cargar documentos 
# Para PDFs: (https://python.langchain.com/docs/modules/data_connection/document_loaders/pdf)
from langchain_community.document_loaders import PyPDFLoader

# Modulo para generar Embeddings
from langchain_openai import OpenAIEmbeddings

# Modulo para dividir el documento en partes
from langchain_text_splitters import CharacterTextSplitter

# Modulo para la Base de Datos de Vectores
from langchain_community.vectorstores import Chroma

dir = './resources'
documents = []

# Esto se puede resumir utilizando el File Directory module: 
# https://python.langchain.com/docs/modules/data_connection/document_loaders/file_directory
for file in os.listdir(dir):
    if file.endswith('.pdf'):
        document_path = f'{dir}/{file}'
        document_information = PyPDFLoader(document_path).load_and_split()

        documents.extend(document_information)

# Cargar el documento en formato PDF

# # Dividir el documento en chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
documents = text_splitter.split_documents(documents)

# Embedir y cargar cada chunk en la base de datos
db = Chroma.from_documents(documents, OpenAIEmbeddings())

# Realizaremos una consulta
query = "Menciona las propiedades de ACID"
docs = db.similarity_search(query)
print(docs[0].page_content)
