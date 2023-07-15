from flask import Flask, app, request, jsonify
from dotenv import load_dotenv
from langchain.vectorstores import FAISS
from chat import ChatTutor
from flask_cors import CORS, cross_origin
from langchain.memory import ConversationBufferMemory
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader

app = Flask(__name__)
CORS(app, support_credentials=True)
load_dotenv()

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

def init_faiss_db():

    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", chunk_size=1, client=None)
    loader = PyPDFLoader("/Users/oshanoshu/AI tutor hackathon/app/backend/docs/science3rd.pdf")
    pages = loader.load_and_split() 
    vector_store = FAISS.from_documents(pages, embeddings)
    vector_store.save_local("db_index")

@app.route('/api/chatbot', methods=['POST'])
def chatbot():
    chat_tutor=ChatTutor()
    message = request.json['message']
    response = chat_tutor.process_message(message, memory)
    response_headers = {
        'Access-Control-Allow-Origin': '*',  # Allow requests from all origins
        'Access-Control-Allow-Headers': 'Content-Type',  # Allow the Content-Type header
    }

    if message == "quiz":
        quiz_response = chat_tutor.process_quiz(response)
        return jsonify(quiz_response), 200, response_headers
    return jsonify(response), 200, response_headers

if __name__ == '__main__':
    init_faiss_db()
    app.run()