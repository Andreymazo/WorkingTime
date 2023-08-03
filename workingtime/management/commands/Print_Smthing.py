from django.core.management import BaseCommand

from config.settings import BASE_DIR


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('BASE_DIR', BASE_DIR)