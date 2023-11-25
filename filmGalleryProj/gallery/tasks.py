from celery import shared_task
from gallery.models import *
import random
import datetime
@shared_task
def generate_Category(count=1):
    for x in range(count):
        cat = Category(random.randint(0, 10000),f'name_{random.randint(0,10000)}')
        cat.save()

@shared_task
def generate_Film(count=1):
    category_ids = list(Category.objects.values_list('id', flat=True))
    for x in range(count):
        current_date = datetime.date.today()
        years_ago = current_date - datetime.timedelta(days=365 * 23)
        random_days = random.randint(0, (current_date - years_ago).days)
        random_date = years_ago + datetime.timedelta(days=random_days)
        random_time = datetime.time(random.randint(0, 23), random.randint(0, 59), random.randint(0, 59), random.randint(0, 999999))
        random_datetime = datetime.datetime.combine(random_date, random_time)
        formatted_datetime = random_datetime.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        number_of_gen_film = random.randint(0,10000)
        film = Film(
             title=f"Название фильма {number_of_gen_film}",
             description=f"фильм #{number_of_gen_film}",
             time_filmed=formatted_datetime,
             film_rating=round(random.uniform(0,5),1),
             poster_url="https://example.com/poster.jpg",
             cat=random.choice(Category.objects.all()),
             user=random.choice(User.objects.all()),
         )
        film.save()


