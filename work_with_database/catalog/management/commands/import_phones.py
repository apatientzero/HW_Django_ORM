import csv
from django.core.management.base import BaseCommand
from catalog.models import Phone


class Command(BaseCommand):
    help = 'Импортирует телефоны из файла phones.csv'

    def handle(self, *args, **options):
        file_path = 'phones.csv'

        try:
            # Открываем файл. Если utf-8 не работает, попробуй encoding='cp1251'
            with open(file_path, 'r', encoding='utf-8') as f:
                # dialect='excel' часто помогает с разными разделителями,
                # но лучше явно указать delimiter, если знаешь его.
                # Попробуем сначала стандартный reader, а потом DictReader с проверкой
                sample = f.read(1024)
                f.seek(0)  # Возвращаем курсор в начало

                # Определяем разделитель автоматически (часто бывает ; в русских Excel)
                sniffer = csv.Sniffer()
                dialect = sniffer.sniff(sample)

                reader = csv.DictReader(f, dialect=dialect)

                phones_to_create = []

                for row in reader:
                    # Выведем ключи для отладки, если что-то пойдет не так
                    # print(row.keys())

                    # Очищаем ключи от лишних пробелов, если они есть
                    clean_row = {k.strip(): v.strip() for k, v in row.items()}

                    phone_id = clean_row.get('id')
                    name = clean_row.get('name')
                    image = clean_row.get('image')
                    price = clean_row.get('price')
                    release_date = clean_row.get('release_date')

                    if not all([phone_id, name, price, release_date]):
                        continue  # Пропускаем строки с пустыми обязательными полями

                    phone = Phone(
                        id=phone_id,
                        name=name,
                        image=image,
                        price=price,
                        release_date=release_date
                    )
                    phones_to_create.append(phone)

                if phones_to_create:
                    Phone.objects.bulk_create(phones_to_create)
                    self.stdout.write(
                        self.style.SUCCESS(f'Успешно импортировано {len(phones_to_create)} телефонов')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING('Не найдено данных для импорта. Проверьте файл.')
                    )

        except FileNotFoundError:
            self.stdout.write(
                self.style.ERROR(f'Файл {file_path} не найден.')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка при импорте: {e}')
            )