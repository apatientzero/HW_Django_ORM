import csv
from django.core.management.base import BaseCommand
from django.utils.text import slugify # <--- Импортируем функцию
from catalog.models import Phone

class Command(BaseCommand):
    help = 'Импортирует телефоны из файла phones.csv'

    def handle(self, *args, **options):
        file_path = 'phones.csv'
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                # Определяем разделитель автоматически
                sample = f.read(1024)
                f.seek(0)
                sniffer = csv.Sniffer()
                dialect = sniffer.sniff(sample)
                
                reader = csv.DictReader(f, dialect=dialect)
                
                phones_to_create = []
                
                for row in reader:
                    clean_row = {k.strip(): v.strip() for k, v in row.items()}
                    
                    phone_id = clean_row.get('id')
                    name = clean_row.get('name')
                    image = clean_row.get('image')
                    price = clean_row.get('price')
                    release_date = clean_row.get('release_date')
                    
                    if not all([phone_id, name, price, release_date]):
                        continue

                    # Генерируем slug из названия (например, "Iphone X" -> "iphone-x")
                    phone_slug = slugify(name)

                    phone = Phone(
                        id=phone_id,
                        name=name,
                        slug=phone_slug, # <--- Заполняем поле slug
                        image=image,
                        price=price,
                        release_date=release_date
                    )
                    phones_to_create.append(phone)
                    
                if phones_to_create:
                    # Удаляем старые записи, чтобы не было конфликтов ID и Slug при повторном запуске
                    Phone.objects.all().delete() 
                    Phone.objects.bulk_create(phones_to_create)
                    self.stdout.write(
                        self.style.SUCCESS(f'Успешно импортировано {len(phones_to_create)} телефонов')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING('Не найдено данных для импорта.')
                    )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка при импорте: {e}')
            )
