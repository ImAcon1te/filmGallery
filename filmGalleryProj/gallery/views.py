from django.http import HttpResponse
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .serializers import *
from .permissions import *
from . import tasks

def home(request):
    return HttpResponse(f"<h1>API запросы для создания задач Celery/Redis</h1>"
                        f"<p><a href='http://127.0.0.1:8000/genfilms/</a>'>генерация 1 фильма</a></p>"
                        f"<p><a href='http://127.0.0.1:8000/genfilms/10/'>генерация n фильмов (на ссылке 10)</a></p>")
def cat_gen(request, pk=None):
    if pk:
        tasks.generate_Category(pk)
        return HttpResponse(f"<h1>запущена генерация {pk} категорий</h1>")
    tasks.generate_Category.delay()
    return HttpResponse(f"<h1>запущена генерация 1 категории (по умолчанию)</h1>")

def film_gen(request, pk=None):
    if pk:
        tasks.generate_Film(pk)
        return HttpResponse(f"<h1>запущена генерация {pk} фильмов</h1>")
    tasks.generate_Film.delay()
    return HttpResponse(f"<h1>запущена генерация 1 фильмa (по умолчанию)</h1>")


class GalleryAPIListPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10000

#get/post
class CatAPIList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = GalleryAPIListPagination

class GalleryAPIList(generics.ListCreateAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = GalleryAPIListPagination

class GallerySortByCatAPIList(generics.ListAPIView):
    serializer_class = FilmSerializer
    queryset = Film.objects.all().order_by('cat_id')
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = GalleryAPIListPagination

class GalleryGetByCatAPIList(generics.ListAPIView):
    serializer_class = FilmSerializer
    queryset = Film.objects.all().order_by('cat_id')
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = GalleryAPIListPagination
    @action(methods=['get'], detail=False)
    def get(self, request,  pk=None):
        queryset = Film.objects.filter(cat_id=pk)
        if queryset:
            return Response({f'фильмы отобранные по категории': [c.title for c in queryset]})
        return Response({'detail': f'По категории id={pk} нет фильмов'})

class GalleryCatAPIList(generics.ListAPIView):
    serializer_class = FilmSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = GalleryAPIListPagination
    @action(methods=['get'], detail=False)
    def get(self, request,  pk=None):
        try:
            cat = Category.objects.get(pk=pk)
            films = Film.objects.filter(cat=pk)
            return Response({f'{cat}': [c.title for c in films]})
        except:
            cats = Category.objects.all()
            films = Film.objects.all()
            return Response({'detail':f"категории под id={pk} не существует",'все категории': [c.name for c in cats],'все фильмы':[f.title for f in films]})

class CommentsToFilmAPIList(generics.ListAPIView):
    serializer_class = FilmSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = GalleryAPIListPagination
    @action(methods=['get'], detail=False)
    def get(self, request,  pk=None):
        try:
            coms = Comment.objects.filter(movie_id=pk)
            film = Film.objects.get(pk=pk)
            if coms:
                data = []
                for comment in coms:
                    data.append({'id':comment.id,
                                 'user_id':comment.user_id,
                                 'comment_rating':comment.comment_rating,
                                 'text':comment.text,})
                return Response({f'{film}': data})# [com.text for com in coms]})
            return Response({'detail':f"комментариев к фильму '{film}' не существует"})
        except:
            return Response({'detail':f"Фильма id={pk} не существует"})


class GalleryAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    permission_classes = (IsAuthenticated, )#(IsOwnerOrReadOnly, )
    authentication_classes = (TokenAuthentication, SessionAuthentication )


class GalleryAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
    permission_classes = (IsAdminOrReadOnly, )


class CommentAPIList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = GalleryAPIListPagination


class CommentAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly, )

class CommentAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAdminOrReadOnly, )

