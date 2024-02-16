import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient, Tag

CSV = {
    Ingredient: 'ingredients.csv',
    Tag: 'tags.csv'
}


class Command(BaseCommand):
    """Импорт csv-файлов."""
    help = 'Command for import csv files'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_path', type=str, nargs='?', default='../data'
        )

    def handle(self, *args, **options):
        count = 0
        csv_path = options['csv_path']
        with open(f'{csv_path}/{CSV[Ingredient]}', encoding='utf-8'
                  ) as csv_file:
            reader = csv.DictReader(csv_file)
            if Ingredient.objects.exists():
                self.stdout.write(self.style.WARNING(
                    f'Для модели "{Ingredient._meta.verbose_name}" '
                    f'данные уже добавлены!')
                )
            else:
                ing_dict = {}
                for row in reader:
                    ing_dict[row['name']] = row['measurement_unit']
                created_objects = Ingredient.objects.bulk_create(
                    Ingredient(
                        name=name, measurement_unit=measurement_unit
                    ) for name, measurement_unit in ing_dict.items()
                )
                count += len(created_objects)
        with open(f'{csv_path}/{CSV[Tag]}', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Tag.objects.get_or_create(
                    name=row['name'], color=row['color'], slug=row['slug'])
                count += 1

        self.stdout.write(self.style.SUCCESS(f'Добавлено записей - {count}'))
