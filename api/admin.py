from django.contrib import admin
from .models import User, Stockpile, Symbol

# Register your models here.
admin.site.register(User)
admin.site.register(Stockpile)
admin.site.register(Symbol)
