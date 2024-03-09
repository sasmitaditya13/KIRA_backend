from langchain_community.callbacks import get_openai_callback
from langchain_openai import OpenAI
from langchain_community.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.chains import ConversationalRetrievalChain
import warnings
import sys
warnings.filterwarnings("ignore")

load_dotenv()

embeddings = OpenAIEmbeddings()

loaded_faiss=FAISS.load_local("vectorstore",embeddings=embeddings,allow_dangerous_deserialization=True)

llm = OpenAI()
memory= ConversationBufferMemory()

conversation=ConversationChain(llm=llm,verbose=True,memory=memory)

chain = ConversationalRetrievalChain.from_llm(llm=llm, 
                                                retriever=loaded_faiss.as_retriever(search_kwargs={"k": 2}))
chat_history = []

query = str(sys.argv)
print(query)
result = chain({"question": query, 'chat_history': chat_history}, return_only_outputs=True)
chat_history += [(query, result["answer"])]

response = chain.run(question=query, chat_history=chat_history)
with open("/home/kirito/R-bot/backend/results.txt" , 'w') as f:
            f.write(response)