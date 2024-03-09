from langchain_community.callbacks import get_openai_callback
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import OpenAI
from langchain_community.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from dotenv import load_dotenv
import sys
load_dotenv()

embeddings = OpenAIEmbeddings()

loaded_faiss=FAISS.load_local("vectorstore",embeddings=embeddings,allow_dangerous_deserialization=True)

llm = OpenAI()
chain = load_qa_chain(llm=llm, chain_type="stuff")


# query=str(input("How can I help you today?: "))
query = sys.argv[1]

docs = loaded_faiss.similarity_search(query=query, k=2)
with get_openai_callback() as cb:
        response = chain.run(input_documents=docs, question=query)
        with open("/home/kirito/R-bot/backend/results.txt" , 'w') as f:
            f.write(response)