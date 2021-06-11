from django.core.management.base import BaseCommand, CommandError
import csv
from django.conf import settings
from company.models import Person, Company


class Command(BaseCommand):
    help = "Запустить парсинг csv файла"
    DIRECTORY_PATH = settings.BASE_DIR / 'import'
    DEFAULT_FILE_NAME = 'new 6.csv'

    def add_arguments(self, parser):
        parser.add_argument('--filename', default=self.DEFAULT_FILE_NAME)

    def handle(self, *args, **options):
        file_name = options.get('filename')
        file_path = self.DIRECTORY_PATH / file_name
        with open(file_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file, delimiter=';', skipinitialspace=True, quoting=csv.QUOTE_ALL)
            for row in reader:
                self.create_users(row)

    def create_users(self, csv_row):
        inn = csv_row[0]
        title = csv_row[1]
        uid = csv_row[2]
        company = Company.get_company(inn)
        person = Person.get_person(uid)
        person.fio = title
        person.company = company
        person.save()
        print(person)
