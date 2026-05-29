from django.contrib import admin

# Register your models here.
from .models import Phone

@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'release_date') # Колонки, которые будут видны в списке
