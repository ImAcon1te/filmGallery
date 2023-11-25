"""
URL configuration for filmGalleryProj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from gallery.views import *
from gallery import views

#router = routers.SimpleRouter()

#router.register(r'gallery', GalleryViewSet, basename='gallery')

"""
127.0.0.1:8000/api/gallery/ - выводит 5 фильмов Доступные методы GET/POST
127.0.0.1:8000/api/gallery/<int:pk> - выводит конкретный фильм. Доступные методы GET/POST/PUT/DELETE
127.0.0.1:8000/api/gallery/<int:pk>/category/ - выводит конкретную категорию. Если выбраной категории нет - выводит все.
127.0.0.1:8000/api/gallery/<int:pk>/category/ - выводит конкретный комментарий. Если выбраной комментария нет - выводит все.
"""


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),

    path('api/gencat/', views.cat_gen),
    path('api/gencat/<int:pk>/', views.cat_gen),
    path('api/genfilm/', views.film_gen),
    path('api/genfilm/<int:pk>/', views.film_gen),

    path('api/v1/cat/', CatAPIList.as_view()),

    path('api/v1/gallery/', GalleryAPIList.as_view()),
    path('api/v1/gallery/<int:pk>/', GalleryAPIUpdate.as_view(), name='gallery-update'),
    path('api/v1/gallerydelete/<int:pk>/', GalleryAPIDestroy.as_view(), name='gallery-destroy'),
    path('api/v1/gallerybycat/<int:pk>/', GalleryCatAPIList.as_view()),
    path('api/v1/сommentstotilm/<int:pk>/', CommentsToFilmAPIList.as_view()),
    path('api/v1/gallery/sortbycat/', GallerySortByCatAPIList.as_view()),
    path('api/v1/gallery/sortbycat/<int:pk>/', GalleryGetByCatAPIList.as_view()),

    path('api/v1/comment/', CommentAPIList.as_view(), name='comment-list'),
    path('api/v1/comment/<int:pk>/', CommentAPIUpdate.as_view(), name='comment-update'),
    path('api/v1/commentdelete/<int:pk>/', CommentAPIDestroy.as_view(), name='comment-destroy'),

    path('api/v1/gallery-auth/', include('rest_framework.urls')),
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
