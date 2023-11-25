from django.contrib.auth.models import User
from django.db import models

class Film(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_loaded = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    time_filmed = models.DateTimeField()
    film_rating = models.FloatField()
    poster_url = models.URLField()
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class Comment(models.Model):
    movie = models.ForeignKey('Film', on_delete=models.CASCADE)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    comment_rating = models.FloatField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Автор коментария: {self.user}, на фильм {self.movie.title}\n' \
               f'Комментарий:{self.text}\n' \
               f'Оценка:{self.comment_rating}\n' \
               f'Временая метка:{self.created_at}'

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name