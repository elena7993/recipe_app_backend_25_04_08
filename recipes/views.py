from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Recipe
from .serializer import SeeRecipeSerializer


class SeeRecipes(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    # 읽기전용

    def get(self, req):
        recipes = Recipe.objects.all()
        # all()전부가져옴

        serializer = SeeRecipeSerializer(
            recipes,
            many=True,
        )

        return Response(serializer.data)
