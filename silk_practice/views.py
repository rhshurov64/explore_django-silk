from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from . import models, serializers


class TestDataAPIView(APIView):
    def get(self, request, format=None):
        data = models.TestModel.objects.all()
        serializer = serializers.TestModelSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = serializers.TestModelSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestDataViewSet(ModelViewSet):
    serializer_class = serializers.TestModelSerializer
    queryset = models.TestModel.objects.all()
