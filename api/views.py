from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import generics,status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer,LoginSerializer
# Create your views here.

class UserRegisterView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes=[AllowAny]
    def post(self, request:Request, *args, **kwargs):
        serialzer = self.serializer_class(data=request.data)
        if serialzer.is_valid(raise_exception=True):
            serialzer.save()
            response = {
                "message":'Register Successfully',
                'data':serialzer.data
            }
            return Response(data=response, status=status.HTTP_200_OK)
        return Response(data= serialzer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    def post(self, request:Request, format=None):
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return Response(data={'message':"Login successfully"}, status=status.HTTP_200_OK)
        return Response(data={'message':"Invalid username or password."})
    def get(self, request:Request, *args, **kwargs):
        response = {
            "user":str(request.user),
            'auth':str(request.auth)
        }
        return Response(data=response, status=status.HTTP_200_OK)
        