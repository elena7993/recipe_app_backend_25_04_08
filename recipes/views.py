import math
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework import status
from .models import Recipe
from .serializer import SeeRecipeSerializer, DetailRecipeSerializer


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
            raise exceptions.otFound("레시피가 없습니다!")

    def get(self, req, pk):
        recipe = self.get_object(pk)

        serializer = DetailRecipeSerializer(recipe)

        return Response(serializer.data)
