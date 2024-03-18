from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

from users.models import User
from users.serializers import UserSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer=UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    def get(self,request):
        serializer = UserSerializer(User.objects.all(), many=True)
        return Response(serializer.data)

class LoginView(APIView):
    permission_classes = []
    authentication_classes = []

    @staticmethod
    def post(request):
        email = request.data.get("email")
        password = request.data.get("password")
        username= request.data.get("username")
        
        if not username:
            if not email or not password:
                return Response(
                    {"detail": "Email and password are required."},
                    status=HTTPStatus.BAD_REQUEST,
                )

            user = get_object_or_404(User, email=email)
        elif not email:
            if not username or not password:
                return Response(
                    {"detail": "Username and password are required."},
                    status=HTTPStatus.BAD_REQUEST,
                )

            user = get_object_or_404(User, username=username)
        else:
            user=get_object_or_404(User,email=email)

        if not user.check_password(password):
            return Response(
                {"detail": "Incorrect password."}, status=HTTPStatus.BAD_REQUEST
            )


        # Generate JWT refresh token for the user
        refresh_token = RefreshToken.for_user(user)

        serializer = UserSerializer(user)
        print("Serializer Data:", serializer.data)
        serializer.access_token = refresh_token.access_token
        serializer.refresh_token = str(refresh_token)
        
        response={}
        for key in serializer.data:
            response[key]=serializer.data[key]
        response["access_token"]=str(refresh_token.access_token)
        response["refresh_token"]=str(refresh_token)
        return Response(
            {
                "data":response
                
            },
            status=HTTPStatus.OK,
        )