from django.contrib import admin
from .models import Category,Book,Rating,Favourite
# Register your models here.
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Rating)
admin.site.register(Favourite)