from datetime import timedelta

from django.core.management import BaseCommand

from workingtime.models import CustomUser, Employee, Timesheet


# from users.models import CustomUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        l = [1, 2, 3]
        for ii in ['Георгий', 'Вася']:
            for i in l:
                timesheet = Timesheet.objects.create(
                    employee=Employee.objects.get(name=ii),
                    date=Employee.objects.get(name=ii).engaged + timedelta(days=i),
                    entry=('9:0'),
                    lunch=('12:0'),
                    # lunch_end=('13:0'),
                    out=('18:0'),
                    # timesheet_emloyee_name=Employee.objects.get(name=ii).name,

                )
                timesheet.save()

