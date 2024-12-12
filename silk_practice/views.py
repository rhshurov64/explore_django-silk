from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from . import models, serializers
from silk.profiling.profiler import silk_profile


class TestDataAPIView(APIView):
    @silk_profile(name="TestDataAPIView - GET")
    def get(self, request, format=None):
        data = models.TestModel.objects.all()
        serializer = serializers.TestModelSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @silk_profile(name="TestDataAPIView - POST")
    def post(self, request, format=None):
        serializer = serializers.TestModelSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestDataViewSet(ModelViewSet):
    serializer_class = serializers.TestModelSerializer
    queryset = models.TestModel.objects.all()


class BookListView(APIView):
    def get(self, request, *args, **kwargs):
        authors = models.Author.objects.all().prefetch_related("books")

        # Create an N+1 problem: for each author, fetch their books
        author_books = []
        for author in authors:
            # books = (
            #     author.books.all()
            # )  # This generates an additional query for each author
            author_books.append(
                {
                    "author": author.name,
                    "books": [book.title for book in author.books.all()],
                }
            )

        return Response(author_books)
