from django.shortcuts import render, get_object_or_404
from .models import Phone

def show_catalog(request):
    """
    Отображает список всех телефонов.
    Доступен по адресу /catalog/
    """
    template = 'catalog/catalog.html'
    phones = Phone.objects.all()
    
    # Если нужна сортировка, можно раскомментировать одну из строк ниже:
    # sort = request.GET.get('sort')
    # if sort == 'min_price':
    #     phones = phones.order_by('price')
    # elif sort == 'max_price':
    #     phones = phones.order_by('-price')
    
    context = {'phones': phones}
    return render(request, template, context)


def show_product(request, slug):
    """
    Отображает детальную информацию об одном телефоне.
    Доступен по адресу /catalog/<slug>/
    """
    template = 'catalog/product.html'
    # Получаем объект по slug или возвращаем 404, если не найден
    phone = get_object_or_404(Phone, slug=slug)
    
    context = {'phone': phone}
    return render(request, template, context)
