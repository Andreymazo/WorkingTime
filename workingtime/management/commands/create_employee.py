from datetime import timedelta

from django.core.management import BaseCommand

from workingtime.models import CustomUser, Employee, Employer, Timesheet


# from users.models import CustomUser


class Command(BaseCommand):

    def handle(self, *args, **options):
        names_emails = {'Георгий':'george@mom.ru', 'Максим':'maxim@mom.ru', 'Вася':'vasia@mom.ru'}
        for i, ii in names_emails.items():
            customuser = CustomUser.objects.create(
                email = ii

            )
            customuser.set_password('qwert123asd')
            customuser.save()
        for i,ii in names_emails.items():
            employee = Employee.objects.create(
                customuser=CustomUser.objects.get(email=ii), #'andreymazo@mail.ru'),
                employer=Employer.objects.get(name='Вася'),
                name=i
            )
            employee.save()
        # l = [1, 2, 3]
        # for i in l:
        #     timesheet = Timesheet.objects.create(
        #         employee=Employee.objects.get(name='Георгий'),
        #         date=Employee.objects.get(name='Георгий').engaged + timedelta(days=i),
        #         entry=('9:0'),
        #         lunch=('12:0'),
        #         lunch_end=('13:0'),
        #         out=('18:0'),
        #     )
        #     timesheet.save()
