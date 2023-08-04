import datetime

from django.core.management import BaseCommand
from django.db.models import DurationField, ExpressionWrapper, F, IntegerField, Sum

from django.utils import timezone

from config.settings import BASE_DIR, STATIC_FILES_DIRS
from workingtime.models import CustomUser, Employee, Employer, Timesheet


# from users.models import CustomUser


class Command(BaseCommand):
    def handle(self, *args, **options):
        # now = timezone.now()
        # print(now)
        # employee_engaged = Employee.objects.get(employer=Employer.objects.get(name='Вася')).engaged
        # print(employee_engaged)
        # print((now-employee_engaged))
        # print(employee_engaged.weekday())#2 wednesday
        # week = [0, 1, 2, 3, 4, 5, 6]
        # daily_start_work =
        # print((Employee.objects.get(name='Петя').engaged + datetime.timedelta(days=1)))
        # c = Timesheet.objects.all().get(employee=Employee.objects.get(name='Петя'))
        # print(c.date)
        # print(STATIC_FILES_DIRS)

    ##############################################################
        # general_total_time = Timesheet.objects.aggregate(
        #     general_total_time=Sum(
        #         ExpressionWrapper(F('out') - F('entry'), output_field=IntegerField()) -
        #         ExpressionWrapper(F('lunch_end') - F('lunch'), output_field=IntegerField()),
        #         output_field=DurationField()
        #     )
        # )
        # print(general_total_time['general_total_time'])
        # print(type(timezone.timedelta(1)))
###############################################
        # total_time = Timesheet.objects.annotate(
        #     total_time=ExpressionWrapper(
        #         ExpressionWrapper(F('out') - F('entry'), output_field=IntegerField()) -
        #         ExpressionWrapper(F('lunch_end') - F('lunch'), output_field=IntegerField()),
        #         output_field=DurationField()
        #     )
        # )
        # for i in total_time:
        #     print(i.date, i.out, i.total_time)
            ############################################
        # p = [p[0] for p in ClientSignedDocument._meta.permissions]
        # my_group = Group.objects.get(name='clients')
        # self.client_user.groups.set([my_group])
        # [my_group.permissions.add(Permission.objects.get(codename=i).id) for i in p]
        # print(Timesheet.objects.all().values_list('id', flat=True)[1])

        # lst_emloyees_id = [i for i in Timesheet.objects.all().values_list('id', flat=True)]
        # lst_emloyees_id = [i for i in Employee.objects.all().values_list('id', flat=True)]
        #############################################
        # employee = Employee.objects.get(name='Георгий')
        # print(employee.customuser.email)
        # customuser = CustomUser.objects.get(email='george@mom.ru')
        # print(customuser.employee.name)
        ###############################################
        # p=Employee.objects.all()
        # j=[]
        # for i in p:
        #     j.append(i.customuser.email)
        # print(j)
        # print([i.customuser.email for i in Employee.objects.all()])
        #############################################

        self_req_employee_id = CustomUser.objects.get(email=self.request.user.email)
        print(self_req_employee_id.employee.id)
        c = Timesheet.objects.all().get(employee_id=self_req_employee_id.employee.id)
        #############################################
        print(BASE_DIR)
        # lst_emloyees_emails = [i for i in Employee.objects.all().employee.values_list('email', flat=True)]

        # print(lst_emloyees_emails)
        # print(Timesheet.objects.filter(employee_id=8))
        # print(CustomUser.objects.select_related("employee")[0])
        # print(Employee.employee.all().name)