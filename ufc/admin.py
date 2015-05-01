from django.contrib import admin

# Register your models here.
from .models import Fighter
from .models import Opponent


admin.site.register(Fighter)
admin.site.register(Opponent)