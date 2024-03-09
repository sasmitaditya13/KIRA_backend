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
from dotenv import load_dotenv
from authlib.integrations.django_client import OAuth
import os
load_dotenv()

oauth = OAuth()

AUTHLIB_OAUTH_CLIENTS = {
'KIRA': {
    'client_id': os.getenv('CLIENT_ID'),
    'client_secret': os.getenv('CLIENT_SECRET'),
    'redirect_uri': 'http://localhost:8000/callback',
}
}

KIRA=oauth.register("KIRA",
               client_id=os.getenv('CLIENT_ID'),
               client_secret=os.getenv('CLIENT_SECRET'),
               server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
               client_kwargs={"scope": "email profile"}
               )

AUTHLIB_INSECURE_TRANSPORT=True

# Create your views here.
def index(self):
    return HttpResponse("K")

def login(request):
        redirect_uri = 'http://localhost:8000/callback'
        return oauth.KIRA.authorize_redirect(request, redirect_uri)
    
def callback(request):
    token = KIRA.authorize_access_token()
    user_info = KIRA.get('https://www.googleapis.com/oauth2/v2/userinfo')
    user_email = user_info.json().get('email')
    return HttpResponse(user_email)
class UserLoginView(APIView):
    
    def post(self,request):
        email = request.GET.get("email","")
        user = User.objects.all().filter(email = email).first()
        if (user == None):
            user = User.objects.create_user(email = email)
                
        # user = User.objects.all().filter(email = email).first()
        chats = user.chats
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key , 'chat history' : chats})

class UserViewSet(viewsets.ModelViewSet):
  authentication_classes = [TokenAuthentication]
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = [permissions.IsAuthenticated]
  