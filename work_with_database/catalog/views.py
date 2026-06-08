from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Phone


def index(request):
    # Получаем все телефоны из базы данных
    phones = Phone.objects.all()

    # Передаем их в контекст шаблона
    context = {
        'phones': phones
    }

    return render(request, 'catalog/index.html', context)