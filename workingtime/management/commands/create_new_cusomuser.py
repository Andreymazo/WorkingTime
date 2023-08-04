from django.core.management import BaseCommand

from workingtime.models import CustomUser


class Command(BaseCommand):

    def handle(self, *args, **options):
        # names_emails = {'Георгий':'george@mom.ru', 'Максим':'maxim@mom.ru', 'Вася':'vasia@mom.ru'}
        # for i, ii in names_emails.items():
            customuser = CustomUser.objects.create(
                email = 'george122@mom.ru'

            )
            customuser.set_password('qwert123asd')
            customuser.save()
