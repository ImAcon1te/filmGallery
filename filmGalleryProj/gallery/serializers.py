import io

from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Film, Comment, Category
import datetime
from datetime import datetime

class FilmSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Film
        fields = ("__all__")

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Comment
        fields = ("__all__")

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("__all__")
"""
Ковырял чисто в образовательных целях

POST/PUT на сериалайзере, GET/DELETE висят на GalleryApiView.
URLS -  GET/POST 'api/gallery/filmlist'
        PUT      'api/gallery/filmlist/<int:pk>/' 
        DELETE   'api/gallery/filmlist/delete/<int:pk>/'
    
class FilmSerializer(serializers.Serializer): 
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    time_loaded = serializers.DateTimeField(read_only=True)
    time_update = serializers.DateTimeField(read_only=True)
    time_filmed = serializers.DateTimeField()
    film_rating = serializers.FloatField()
    poster_url = serializers.URLField()
    cat_id = serializers.IntegerField()
    def create(self, validated_data):
        return Film.objects.create(**validated_data)
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.time_loaded = validated_data.get('time_loaded', instance.time_loaded)
        instance.time_update = validated_data.get('time_update', instance.time_update)
        instance.time_filmed = validated_data.get('time_filmed', instance.time_filmed)
        instance.film_rating = validated_data.get('film_rating', instance.film_rating)
        instance.poster_url = validated_data.get('poster_url', instance.poster_url)
        instance.cat_id = validated_data.get('cat_id', instance.cat_id)
        instance.save()
        return instance
class FilmModel:
    def __init__(self,title,description,time_filmed,film_rating,poster_url,cat_id):
        self.title = title
        self.description = description
        self.time_loaded = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        self.time_update = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        self.time_filmed = time_filmed
        self.film_rating = film_rating
        self.poster_url = poster_url
        self.cat_id = cat_id
    def __repr__(self):
        return (f"{self.title=}\n"
              f"{self.description=}\n"
              f"{self.time_loaded=}\n"
              f"{self.time_update=}\n"
              f"{self.time_filmed=}\n"
              f"{self.film_rating=}\n"
              f"{self.poster_url=}\n"
              f"{self.cat_id=}\n")
"""
"""
Использовал для тестов кодирования/декодирования в байтовый JSON. Просто проверял нет ли в джанге серьезных отличий. В целом нет.
def encode():
    model = FilmModel('название','описание',"2017-09-17T11:24:49Z",4.3,'https://upload.wikimedia.org/wikipedia/ru/a/a9/%D0%A2%D0%B5%D0%BB%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%B8%D1%82%D0%B5%D0%BB%D1%8C_%D0%BA%D0%B8%D0%BB%D0%BB%D0%B5%D1%80%D0%B0.jpg',4)
    model_sr = FilmSerializer(model)
    json = JSONRenderer().render(model_sr.data)
    print(json)
    #from gallery.serializers import encode
    
def decode():
    stream = io.BytesIO(b'{"title":"\xd0\xbd\xd0\xb0\xd0\xb7\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5","description":"\xd0\xbe\xd0\xbf\xd0\xb8\xd1\x81\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5","time_loaded":"2023-11-22T16:05:38Z","time_update":"2023-11-22T16:05:38Z","time_filmed":"2017-09-17T11:24:49Z","film_rating":4.3,"poster_url":"https://upload.wikimedia.org/wikipedia/ru/a/a9/%D0%A2%D0%B5%D0%BB%D0%BE%D1%85%D1%80%D0%B0%D0%BD%D0%B8%D1%82%D0%B5%D0%BB%D1%8C_%D0%BA%D0%B8%D0%BB%D0%BB%D0%B5%D1%80%D0%B0.jpg","cat_id":"4"}')
    data = JSONParser().parse(stream)
    serializer = FilmSerializer(data=data)
    serializer.is_valid()
    print(serializer.validated_data)
    
"""