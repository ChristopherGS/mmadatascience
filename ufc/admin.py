from django.contrib import admin

# Register your models here.
from .models import Fighter, Opponent

admin.site.register(Fighter)
admin.site.register(Opponent)
