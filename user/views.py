from django.shortcuts import render
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken


from .serializers import UserCreateSrz, UserLoginSrz

class CreateUserView(views.APIView):
    permission_classes = [AllowAny]
    def post(self ,request):
        serializer = UserCreateSrz(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"maessage": "user created succesfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class UserLoginView(views.APIView):
    def post(self, request):
        serializer = UserLoginSrz(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                response = Response({"message": "ورود موفقیت‌آمیز بود"})
                csrftoken = get_token(request)
                response.set_cookie(key='refresh_token', value=str(refresh), httponly=False, secure=True, samesite='None', max_age=360000)
                response.set_cookie(key='access_token', value=str(refresh.access_token), httponly=False, secure=True, samesite='None', max_age=360000)
                response.set_cookie(key="csrftoken", value=csrftoken, httponly=False, secure=True, samesite='None', max_age=360000)
                return response
            return Response({"error": "ایمیل یا رمز عبور اشتباه است."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    




class UserLogout(views.APIView):
    permission_classes = [AllowAny]
    authentication_classes = []


    def post(self, request):
        response = Response({"message": "loged out succesfully"})
        response.delete_cookie("access_token", path="/", samesite="None")
        response.delete_cookie("refresh_token", path="/", samesite="None")
        return response

