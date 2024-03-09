from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from .models import User
from .serializers import UserSerializer
import requests
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from langchain_community.callbacks import get_openai_callback
from langchain_openai import OpenAI
from langchain_community.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.chains import ConversationalRetrievalChain
import warnings
from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import ElasticVectorSearch, Pinecone, Weaviate, FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
warnings.filterwarnings("ignore")

load_dotenv()
chat_history = []


class AiViewSet(APIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        print(request.user)
        print(request.user.chats)
        query = request.GET.get("query","")
        
        os.system('python test2.py ' + query)

        with open("/home/kirito/R-bot/backend/results.txt" , 'r') as f:
            response=f.read()
            print(response)
    
        return Response(response)

class TrainViewSet(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        reader=PdfReader("static/datafresh.pdf")

        text = ""
        for page in reader.pages:
            text += page.extract_text()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
            )
        chunks = text_splitter.split_text(text=text)


        embeddings = OpenAIEmbeddings()

        VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
        VectorStore.save_local("static/vectorstore","index") # Save the vectorstore to disk

        llm = OpenAI()
        chain = load_qa_chain(llm=llm, chain_type="stuff")

    
    
    
        return Response({'SUCCESS'})
