from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework import status
from .serializer import PublicUserSerializer, PrivateUserSerializer
from users.models import User


class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, req):
        user = req.user
        serializer = PublicUserSerializer(user)
        return Response(serializer.data)

    def put(self, req):
        user = req.user
        serializer = PrivateUserSerializer(
            user,
            data=req.data,
            partial=True,
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, req):
        user = req.user
        user.delete()
        return Response(
            status=status.HTTP_200_OK,
        )


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


class Login(APIView):
    def post(self, req):
        username = req.data.get("username")
        password = req.data.get("password")
        print(username)
        print(password)

        if not username or not password:
            raise exceptions.ParseError("아이디 및 비밀번호는 필수입니다!")

        try:
            validate_password(password)
        except Exception as e:
            raise exceptions.ParseError(e)

        user = authenticate(
            req,
            username=username,
            password=password,
        )

        if user:
            login(req, user)
            return Response({"ok": "로그인되었습니다"}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "아이디 및 패스워드를 다시 확인해주세요!"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, req):
        logout(req)
        return Response(
            {"ok": "로그아웃되었습니다"},
            status=status.HTTP_200_OK,
        )


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, req):
        user = req.user

        old_password = req.data.get("old_password")
        new_password = req.data.get("new_password")

        if not old_password or not new_password:
            raise exceptions.ParseError("패스워드 입력은 필수입니다!")

        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(
                {"ok": "패스워드를 변경했습니다."}, status=status.HTTP_200_OK
            )
        else:
            raise exceptions.ParseError("패스워드를 다시 확인해보세요!")


class SeeUser(APIView):
    def get(self, req, username):
        try:
            user = User.objects.get(username=username)
            serializer = PublicUserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            raise exceptions.NotFound("찾으시는 유저가 없습니다.")
