внутри есть doker-compose.yml и Dokerfile для 3х контейнеров - drf, redis, celery
Для токенов был использован djoser
из доп. библиотек есть random/datetime

1) GET сгенерировать категорию (Сelery) - http://127.0.0.1:8000/api/gencat/
2) GET сгенерировать много категорий (Сelery) - http://127.0.0.1:8000/api/gencat/<int:количество>/
3) GET сгенерировать фильм (Сelery) - http://127.0.0.1:8000/api/genfilm/
4) GET сгенерировать много фильмов (Сelery) - http://127.0.0.1:8000/api/genfilm/<int:pk>/
5) GET просмотр категорий - http://127.0.0.1:8000/api/v1/cat/
6) GET просмотр всех фильмов - http://127.0.0.1:8000/api/v1/gallery/
7) PUT просмотр/изменений конкретного фильма [аутентификация по токену или сессия] - http://127.0.0.1:8000/api/v1/gallery/<int:id_фильма>/
8) DELETE удалить конкретный фильм [только админ] - http://127.0.0.1:8000/api/v1/gallerydelete/<int:id_фильма>/
9) GET получить названия фильмов по категории [авторизован или только для чтения] - http://127.0.0.1:8000/api/v1/gallerybycat/<int:id_категории>/
10) GET посмотреть комментарий к фильму - http://127.0.0.1:8000/api/v1/сommentstotilm/<int:id_фильма>/
11) GET посмотреть фильмы отсортированные по категориям http://127.0.0.1:8000/api/v1/gallery/sortbycat/
12) GET/POST посмотреть или добавить комментарий - http://127.0.0.1:8000/api/v1/comment/
13) PUT изменить комментарий - http://127.0.0.1:8000/api/v1/comment/<int:id_комментария>/
14) DELETE удалить комментарий - http://127.0.0.1:8000/api/v1/commentdelete/<int:pk>/
15) POST регистрация - http://127.0.0.1:8000/api/v1/auth/users/
-> username, password, email
<- данные о зарегистрированном пользователе или сообщение о неправильно введеных данных
16) POST запрос токена - http://127.0.0.1:8000/auth/token/login/
-> username, password, email
<- auth_token
17) GET logout - http://127.0.0.1:8000/auth/token/logout/
