import os
import logging
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.chains import create_history_aware_retriever
from langchain_openai import ChatOpenAI

load_dotenv()
API_KEY = os.getenv('OPEN_API_KEY')

logging.basicConfig(level=logging.DEBUG, force='%(asctime)s - %(levelname)s - %(message)s')

# Global store to hold session data
session_store = {}

def load_embedding():
    logging.debug("1. Retriever haven't loaded --> Started to load embeddings")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory="./vector_database_2", embedding_function=embeddings)
    retriever = db.as_retriever()
    print("Load embedding sucessfully!")
    logging.debug("2. Load embedding successfully!")
    return retriever


# Session history handler
def get_session_history(session_id: str):
    if session_id not in session_store:
        session_store[session_id] = ChatMessageHistory()
    return session_store[session_id]


# Call this function only one time
def initialize_rag_chain(retriever):

    llm = ChatOpenAI(api_key=API_KEY, model='gpt-4o-mini')

    # System prompt
    contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
    )

    contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
    
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    system_prompt = (
            """
            You are a friendly Troy University Advisor assistant, please answer the question based only on the following context.
            Context: {context}
            Please answer the question with at least 5 sentences and provide more information from the context.
            Always provide an answer, and never say you are not an expert and not able to answer.
            """
        )
    
    prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder('chat_history'),
                ("human", "{input}"),
            ]
        )

    question_answer_chain = create_stuff_documents_chain(llm, prompt)

    logging.debug("3. Creating RAG chain...")

    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    conversational_rag_chain = RunnableWithMessageHistory(
                                    rag_chain,
                                    get_session_history,
                                    input_messages_key="input",
                                    history_messages_key="chat_history",
                                    output_messages_key="answer",
                                )
    
    session_store['conversational_rag_chain'] = conversational_rag_chain

    logging.debug("4. Created RAG chain")


# Main chatbot process
def process_chat(user_input: str, session_id: str):
    # Load embedding only one time
    if "retriever" not in session_store:
        session_store["retriever"] = load_embedding()

    # Ensure RAG chain is initialized
    if 'conversational_rag_chain' not in session_store:
        initialize_rag_chain(retriever=session_store["retriever"])
    
    rag_chain = session_store['conversational_rag_chain']

    response = rag_chain.invoke({"input": user_input}, config={"configurable": {"session_id": session_id}})
    
    print(response)
    answer = response['answer']

    return answer
