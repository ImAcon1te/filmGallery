from django.contrib import admin

# Register your models here.
#from filmGalleryProj import gallery
from .models import Film, Comment, Category

admin.site.register(Film)
admin.site.register(Comment)
admin.site.register(Category)