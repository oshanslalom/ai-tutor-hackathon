from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS


class ChatTutor:
    condense_prompt = PromptTemplate.from_template(
    ("Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.\n"
      "Chat History:\n"
      "{chat_history}\n"
      "Follow Up Input: {question}\n"
      "Standalone question:"))

    question_prompt = PromptTemplate.from_template(
    ("You are a 3rd grade teching assistant. Be simple and fun in your explanation. You are a 3rd grade teching assistant. Be simple and fun in your explanation. Always answer question based on following context only."
    "If you don't know the answer, just say you don't know. DO NOT try to make up an answer."
    "If the question is not related to the context, say its not related to the context. Please ask me about context related questions"

    "{context}"

    "Question: {question}"
    "Helpful answer in markdown:"))

    quiz_condense_prompt = PromptTemplate.from_template(
    ("Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.\n"
      "Chat History:\n"
      "{chat_history}\n"
      "Follow Up Input: {question}\n"
      "Standalone question:")
)

    quiz_question_prompt = PromptTemplate.from_template(
    ("You are a 3rd grade teacher's assistant."
    "Just ask one question and give them three options." 
    "Question should be based on the last interaction in {chat_history} and it should be within the context {context}. Ask in the following format as precisely as possible:"
    "Question: YOUR QUESTION"
    "Options: YOUR CHOICES"
)
)

    quiz_check_prompt = PromptTemplate.from_template(
    ("You are a 3rd grade teacher's assistant.\n"
    "Congratulate them when they get the right answer to your question in chat history {chat_history} otherwise give them explanation on what they did wrong as a result within the context {context}. In the following format:"
    "\nResult:"
    ))

    def __init__(self):
        pass

    def process_message(self, message, memory):
        chain = self.get_chain(message, memory)
        result = chain({"question": message})
        return result["answer"]

    def get_chain(self, message, memory):
        model = ChatOpenAI(temperature=0, model='gpt-4', client=None)
        vector = self.get_vector()
        if message=="quiz":
            return ConversationalRetrievalChain.from_llm(model, vector.as_retriever(), memory=memory, condense_question_prompt=self.quiz_condense_prompt,combine_docs_chain_kwargs={'prompt': self.quiz_question_prompt})
        if message.startswith("QuizAnswer:"):
             return ConversationalRetrievalChain.from_llm(model, vector.as_retriever(), memory=memory, combine_docs_chain_kwargs={'prompt': self.quiz_check_prompt})
        return ConversationalRetrievalChain.from_llm(model, vector.as_retriever(), condense_question_prompt=self.condense_prompt, memory=memory, combine_docs_chain_kwargs={'prompt': self.question_prompt})

    def get_vector(self):

        embeddings = OpenAIEmbeddings(model="text-embedding-ada-002", chunk_size=1, client=None)
        vector_store = FAISS.load_local("db_index", embeddings)
        return vector_store
    
    def process_quiz(self, response):
        split_string = response.split("Options:")
        question = split_string[0].strip().replace("Question:", "")
        options = [option.strip() for option in split_string[1].strip().split("\n")]

        return {
            'question': question,
            'options': options
        }
