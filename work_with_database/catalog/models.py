from django.db import models

# Create your models here.

class Phone(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True, verbose_name="URL") # <--- Added
    image = models.URLField(blank=True, null=True, verbose_name="Изображение")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    release_date = models.DateField(verbose_name="Дата выпуска")

    class Meta:
        db_table = 'phones'
        verbose_name = "Телефон"
        verbose_name_plural = "Телефоны"

    def __str__(self):
        return self.name
