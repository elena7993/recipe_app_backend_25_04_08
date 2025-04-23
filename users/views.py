from django.contrib.auth.password_validation import validate_password
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework import status
from .serializer import PublicUserSerializer, PrivateUserSerializer


class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, req):
        user = req.user
        serializer = PublicUserSerializer(user)
        return Response(serializer.data)


class Signup(APIView):
    def post(self, req):
        password = req.data.get("password")
        serializer = PublicUserSerializer(data=req.data)

        try:
            validate_password(password)
        except Exception as e:
            raise exceptions.ParseError(e)

        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()

            serializer = PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
