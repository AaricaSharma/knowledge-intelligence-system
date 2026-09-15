from langchain.chat_models import ChatOpenAI
from langchain.chains import conversational_retrieval
from langchain.memory import ConversationBufferMemory
from config import Config
class llm_service:
    def __init__(self,vector_store):
        self.llm=ChatOpenAI(
            temperature=0.7,
            model_name="gpt-3.5-turbo",
            openai_api_key=Config.OPENAI_API_KEY
        )
        self.memory=ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.chain=ConversationalRetrievalChain(
            llm=self.llm,
            retriever=vector_store.vectorstore.as_retriever(),
            memory=self.memory
        )
    def get_response(self,query):
        try:
            response=self.chain({"question":query})
            return response['answer']
        except Exception as e:
            print(f"Error getting in llm response: {e}")
            return "I encountered an error proccessing your request"