from django.shortcuts import render
from django.contrib.auth import login, logout

from rest_framework.views import APIView

#from .authentication import QuietBasicAuthentication

class APILogin(APIView):
	pass