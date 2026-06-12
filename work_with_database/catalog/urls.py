from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_catalog, name='catalog'),       # Адрес /catalog/
    path('<slug>/', views.show_product, name='product'), # Адрес /catalog/<slug>/
]
