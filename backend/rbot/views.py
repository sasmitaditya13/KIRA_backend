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

# Create your views here.
def index(self):
    return HttpResponse("K")

class UserLoginView(APIView):
    
    def post(self,request):
        email = request.GET.get("email","")
        user = User.objects.all().filter(email = email).first()
        if (user == None):
            user = User.objects.create_user(email = email)
                
        # user = User.objects.all().filter(email = email).first()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

class UserViewSet(viewsets.ModelViewSet):
  authentication_classes = [TokenAuthentication]
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = [permissions.IsAuthenticated]
  