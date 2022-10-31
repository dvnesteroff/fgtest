import csv
import os

from django.core.management.base import BaseCommand

from api.models import Ingredient, Tag

INGREDIENS_FILE = 'ingredients.csv'
TAGS_FILE = 'tags.csv'
RECIPES_FILE = 'recipes.csv'


class Command(BaseCommand):
    """
    Команда 'load_data' импортирует данные об
    ингредиентах и/или тэгах из файлов
    ingredients.csv и tags.csv в БД.
    Файлы должен находиться в директории /fixtures/
    """

    def handle(self, *args, **options):
        cou = 0
        if options['ingredients']:
            self.import_data(file=INGREDIENS_FILE)
            cou += 1
        if options['tags']:
            self.import_data(file=TAGS_FILE)
            cou += 1
        if options['recipes']:
            self.import_data(file=RECIPES_FILE)
            cou += 1
        if cou == 0:
            print('Для импорта данных используйте ключи -i и/или -t\n')
        else:
            print('Импорт завершен.\n')

    def add_arguments(self, parser):
        parser.add_argument(
            '-i',
            '--ingredients',
            action='store_true',
            default=False,
            help='Импортировать ингридиенты.'
        )
        parser.add_argument(
            '-t',
            '--tags',
            action='store_true',
            default=False,
            help='Импортировать теги.'
        )
        parser.add_argument(
            '-r',
            '--recipes',
            action='store_true',
            default=False,
            help='Импортировать рецепты.'
        )

    def ingredient_update_or_create(self, row):
        num_err = 0
        try:
            obj, created = Ingredient.objects.update_or_create(
                name=row[0],
                measurement_unit=row[1],
            )
        except Exception as error:
            print(error)
            num_err += 1
        return num_err

    def tag_update_or_create(self, row):
        num_err = 0
        try:
            obj, created = Tag.objects.update_or_create(
                name=row[0],
                color=row[1],
                slug=row[2],
            )
        except Exception as error:
            print(error)
            num_err += 1
        return num_err

    def import_data(self, file=INGREDIENS_FILE):
        num_err = 0
        print(f'Загрузка {file} ...')
        file_path = f'./fixtures/{file}'
        if not os.path.exists(file_path):
            print(f'{file} не найден!')
            return

        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                print(row)
                if file == INGREDIENS_FILE:
                    num_err += self.ingredient_update_or_create(row=row)
                elif file == TAGS_FILE:
                    num_err += self.tag_update_or_create(row=row)
                else:
                    print('\nИспользован неизвестный аргумент.')

        print(f'\nЗагрузка {file} завершена.')
        if num_err > 0:
            print(f'[!] Ошибок при загрузке: {num_err} . Проверьте данные.')
        print('\n')
