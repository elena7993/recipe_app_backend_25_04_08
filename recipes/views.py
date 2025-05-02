import math
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework import status
from .models import Recipe
from .serializer import SeeRecipeSerializer, DetailRecipeSerializer
from comments.serializer import CommentSerializers


class SeeRecipes(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    # 읽기전용

    def get(self, req):
        page = req.query_params.get("page")
        # =>url 매개변수 가져옴

        try:
            page = int(page)
        except Exception:
            page = 1

        page_count = settings.PAGE_COUNT
        start = (page - 1) * page_count
        end = start + page_count

        all_recipe = Recipe.objects.all()
        recipes = all_recipe.order_by("-created_at")[start:end]
        # all()전부가져옴

        total = all_recipe.count()
        total_page = math.ceil(total / settings.PAGE_COUNT)
        print(total_page)

        serializer = SeeRecipeSerializer(
            recipes,
            many=True,
        )

        return Response(
            {
                "data": serializer.data,
                "page": page,
                "total_page": total_page,
            }
        )

    def post(self, req):
        serializer = DetailRecipeSerializer(data=req.data)

        if serializer.is_valid():
            recipe = serializer.save(user=req.user)
            serializer = DetailRecipeSerializer(recipe)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipeDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            raise exceptions.NotFound("레시피가 없습니다!")

    def get(self, req, pk):
        recipe = self.get_object(pk)

        serializer = DetailRecipeSerializer(
            recipe,
            context={"req": req},
        )

        return Response(serializer.data)

    def put(self, req, pk):
        recipe = self.get_object(pk)
        user = req.user

        if user != recipe.user:
            raise exceptions.PermissionDenied

        srializer = DetailRecipeSerializer(
            recipe,
            data=req.data,
            partial=True,
        )

        if serializer.is_valid():
            recipe = serializer.save()
            serializer = DetailRecipeSerializer(recipe)
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, req, pk):
        recipe = self.get_object(pk)
        user = req.user
        if user != recipe.user:
            raise exceptions.PermissionDenied

        recipe.delete()
        return Response(
            {
                "ok": True,
            },
            status=status.HTTP_204_NO_CONTENT,
        )


class RecipeLike(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            raise exceptions.NotFound

    def put(self, req, pk):
        recipe = self.get_object(pk)

        if recipe.like.filter(pk=req.user.pk).exists():
            recipe.like.remove(req.user)
        else:
            recipe.like.add(req.user)

        return Response(
            {"ok": True},
        )

        # 좋아요를 누른 유저를 찾고,
        # 그 유저중에서 나를 찾아야함(내가 좋아요한)


class SeeComment(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            raise exceptions.NotFound("레시피가 없습니다!")

    def get(self, req, pk):
        recipe = self.get_object(pk)
        comment = recipe.comments.all()

        serializer = CommentSerializers(
            comment,
            many=True,
            context={"req": req},
        )

        return Response(serializer.data)
