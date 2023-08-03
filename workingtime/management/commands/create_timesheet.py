from datetime import timedelta

from django.core.management import BaseCommand

from workingtime.models import CustomUser, Employee, Timesheet


# from users.models import CustomUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        l = [1, 2, 3]
        for i in l:
            timesheet = Timesheet.objects.create(
                employee=Employee.objects.get(name='Георгий'),
                date=Employee.objects.get(name='Георгий').engaged + timedelta(days=i),
                entry=('9:0'),
                lunch=('12:0'),
                lunch_end=('13:0'),
                out=('18:0'),
            )
            timesheet.save()