from django.core.management import BaseCommand

from workingtime.models import CustomUser, Employer


# from users.models import CustomUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        employee = Employer.objects.create(
            customuser=CustomUser.objects.get(email='andreymazo@mail.ru'),
            name='Вася'
        )
        employee.save()