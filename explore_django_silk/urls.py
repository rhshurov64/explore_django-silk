from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from silk_practice import views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

router.register("test-data-viewset", views.TestDataViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("test-data/", views.TestDataAPIView.as_view()),
    path("author-book/", views.BookListView.as_view()),
    path("", include(router.urls)),
]

# Conditionally include Silk URLs if DEBUG is True
if settings.DEBUG:
    urlpatterns += [
        path("silk/", include("silk.urls", namespace="silk")),
    ]
