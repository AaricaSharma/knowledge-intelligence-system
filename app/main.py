from models.vector_store import VectorStore
from sevices.storage_service import s3Storage
from sevices.llm_srvice import llm_service
from config import Config
import os
from langchain.document_loaders import TextLoader,PyPDFLoader 
from langchain.text_splitter import RecursiveCharacterTextSplitter
import tempfile
import logging
vectore_store=VectorStore(Config.VECTOR_DB_PATH)
storage_services=s3Storage()
LLM_service=llm_service(vectore_store)



#CONFIGURE LOGGING
logging.basicConfig(level=logging.DEBUG)
logger=logging.getLogger(__name__)

def process_document(file):
    temp_dir=tempfile.mkdtemp()
    temp_path=os.path.join(temp_dir,file.filename)

    try:
        #save file temporarily
        file.save(temp_path)

        #process based on file type
        if file.filename.endswith('.pdf'):
            loader=PyPDFLoader(temp_path)
            documents=loader.load()
        elif file.filename.endswith('.txt'):
            loader=TextLoader(temp_path)
            documents=loader.load()
        else:
            raise ValueError("unsupported file type")
        
        #split text into chunks
        text_splitter=RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        text_chunks=text_splitter.split_documents(documents)
        return text_chunks
    finally:
        #clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)
        os.rmdir(temp_dir)
              

