from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.shortcuts import render
from django.utils import timezone
from django_tables2 import tables, TemplateColumn
from pip._internal.utils._jaraco_text import _
from django.urls import reverse_lazy
from workingtime.managers import CustomUserManager

phone_validator = RegexValidator(r"^(\+?\d{0,4})?\s?-?\s?(\(?\d{3}\)?)\s?-?\s?(\(?\d{3}\)?)\s?-?\s?(\(?\d{4}\)?)?$",
                                 "The phone number provided is invalid")
NULLABLE = {'blank': True, 'null': True}


class CustomUser(AbstractBaseUser, PermissionsMixin):  # , PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True)
    # VERIFICATION_TYPE = [
    #     ('sms', 'SMS'),
    # ]
    # phone_number = PhoneNumberField(unique = True)
    # verification_method = models.CharField(max_length=10,choices= VERIFICATION_TYPE)
    # phone_number = models.CharField(max_length=16, validators=[phone_validator], unique=True)
    full_name = models.CharField(max_length=30)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    # is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return f"{self.id}: {self.email}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        permissions = [("workingtime.add_customuser", "Can add customuser"),
                       ("workingtime.change_customuser", "Can change customuser"),
                       ("workingtime.delete_customuser", "Can delete customuser"),
                       ("workingtime.view_customuser", "Can view customuser")]

    @staticmethod
    def has_perm(perm, obj=None, **kwargs):
        return True

    @staticmethod
    def has_module_perms(app_label, **kwargs):
        return True


class CustomUserTable(tables.Table):
    class Meta:
        model = CustomUser
        empty_text = _(
            "No hay ninguna asignatura que satisfaga los criterios de búsqueda."
        )
        template_name = "django_tables2/bootstrap3.html"
        per_page = 20
        # template_name = 'django_tables2/bootstrap.html'


class Employer(models.Model):
    customuser = models.OneToOneField('workingtime.CustomUser', on_delete=models.CASCADE)
    name = models.CharField(max_length=150, verbose_name='Работодатель')
    joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id} {self.name}'


class EmployerTable(tables.Table):
    class Meta:
        model = Employer


class Employee(models.Model):
    customuser = models.OneToOneField('workingtime.CustomUser', on_delete=models.CASCADE, related_name='employee')
    employer = models.ForeignKey('workingtime.Employer', on_delete=models.CASCADE)
    name = models.CharField(max_length=150, verbose_name='Работник')
    engaged = models.DateTimeField(default=timezone.now)

    # edit = TemplateColumn('<a href="{% url "workingtime:home2" record.id %}">Edit</a>')
    # acciones = TemplateColumn(
    #     template_code='<a href="{% url "workingtime:home2" record.id %}" class="btn btn-success">Ver</a>')
    class Meta:
        unique_together = ("name", "customuser")
        # permissions = [("workingtime.add_employee", "Can add employee"),
        #                ("workingtime.change_employee", "Can change employee"),
        #                ("workingtime.delete_employee", "Can delete employee"),
        #                ("workingtime.view_employee", "Can view employee")]

    def __str__(self):
        return f" {self.name} id: {self.id}"


class EmployeeTable(tables.Table):
    class Meta:
        model = Employee


class Timesheet(models.Model):
    STATUS_WORK = True
    STATUS_NOWORK = False
    STATUSES = (
        (STATUS_WORK, 'WORK'),
        (STATUS_NOWORK, 'NOWORK')
    )
    status_work = models.BooleanField(choices=STATUSES, verbose_name='Статус работы',
                                      default=STATUS_NOWORK)
    employee = models.ForeignKey('workingtime.Employee', on_delete=models.CASCADE, related_name='timesheet', **NULLABLE)
    datetime_start = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name="Начало рабочего дня", **NULLABLE)
    datetime_complete = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name="Конец рабочего дня", **NULLABLE)
    time_break = models.DateTimeField(auto_now=True, auto_now_add=False, null=True, blank=True, verbose_name="Начало перерыва")
    # out = models.TimeField(auto_now=False, auto_now_add=False, verbose_name="Конец рабочего дня", default='18:00:00')

    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Таймшиты"

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        
        if not self.status_work and self.datetime_start:
            print('here-----------------')
            w = WorkTime.objects.all()
            ww = w.exclude(start_break_safe_sheets=None)
            www = w.exclude(end_break_safe_sheets=None)


##Если статус нерабочий, в ворктайме уже сть end_break_safe_sheets, to nevazhno, mozhno udalit
            # if www:
            #     j = WorkTime.objects.create(start_break_safe_sheets=self.time_break, timesheet_id=self.id,
            #                                 time_worked_per_day=str(self.time_break-ww.latest('start_break_safe_sheets').start_break_safe_sheets))
            #     j.save()
## Если статус нерабочий, в ворктайме есть start_break_safe_sheets          
            if ww:
                print('sssssssssssssssssssssssss')
                j = WorkTime.objects.create(start_break_safe_sheets=self.time_break, timesheet_id=self.id,
                                            time_worked_per_day=str(self.time_break-ww.latest('start_break_safe_sheets').start_break_safe_sheets))
                j.save()
## Если статус нерабочий, в ворктайме нет start_break_safe_sheets, то вычитаем из time_break datetime_start Сюда можно попасть , если 
# нажать на создать новый день, но статус сделать не рабочим, вроде так не должно быть впринципе и попасть сюда не должны
            if not ww:
                print('ffffffffffffffffffffffffffffff[[[[[]]]]]')
                j = WorkTime.objects.create(start_break_safe_sheets=self.time_break, timesheet_id=self.id,
                                            time_worked_per_day=str(self.time_break-self.datetime_start))#ww.latest('start_break_safe_sheets').start_break_safe_sheets))
                j.save()  
        if self.status_work and self.datetime_start:
            print('77777777777777777777777')
            w = WorkTime.objects.all()
            ww = w.exclude(start_break_safe_sheets=None)
            www = w.exclude(end_break_safe_sheets=None)
##Если статус рабочий, но в ворктайме уже есть end_break_safe_sheets
            if www:
                print('66666666666666666666666666')
                j = WorkTime.objects.create(end_break_safe_sheets=self.time_break, timesheet_id=self.id)
                                            #time_worked_per_day=str(self.time_break-ww.latest('start_break_safe_sheets').start_break_safe_sheets))# Второй раз чситать не надо
                j.save()
##Если статус рабочий, но в ворктайме еще нет start_break_safe_sheets, то вместо него self.datetime_start

            if not ww:
                print(f'Создали тамшит {self.id} timesheet.datetime_start {self.datetime_start}')
                # j = WorkTime.objects.create(start_break_safe_sheets=self.time_break, timesheet_id=self.id,
                                            #time_worked_per_day=str(self.time_break-self.datetime_start))
                # j.save()
##Если статус рабочий, но еще нет end_break_safe_sheets
            if not www:
                print('hhhhhhhhhhhhhhhhhhhhjjj')
                j = WorkTime.objects.create(end_break_safe_sheets=self.time_break, timesheet_id=self.id)
                j.save()
## Если статус рабочий, и есть Завершение рабочего дня end_break_safe_sheets и есть конец рабочего дня 
        if self.status_work and self.datetime_complete:
            print('{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}}')
            j = WorkTime.objects.create(end_break_safe_sheets=self.datetime_complete, timesheet_id=self.id)
            j.save()
           
## Если статус нерабочий, и есть Завершение рабочего дня, тогда ничего
        if not self.status_work and self.datetime_complete:
            print(':::::::::::;')
            j = WorkTime.objects.create(timesheet_id=self.id)
            j.save()
            print('self.id', self.id)
           
        
        # if self.status_work:
            # j = WorkTime.objects.create(end_break_safe_sheets=self.time_break, timesheet_id=self.id,)
            # j.save()
        # timesheet_employee_name = self.employee.name
        super(Timesheet, self).save(force_insert, force_update, using, update_fields)
        # return j

    # print(employee.customuser.email)
    def __str__(self):
        return f" Таймшит относится к сотруднику: {self.employee.name}  id:{self.employee.id} id таймшита: {self.id}"


class TimesheetTable(tables.Table):
    class Meta:
        model = Timesheet


class WorkTime(models.Model):
    timesheet = models.ForeignKey('workingtime.Timesheet', related_name='worktime', on_delete=models.CASCADE,
                                  **NULLABLE)
    # lunch = models.TimeField(auto_now=True, auto_now_add=False, null=True, blank=True)
    start_break_safe_sheets = models.DateTimeField(auto_now_add=False, auto_now=False, verbose_name="Запись начала перерыва", **NULLABLE)
    end_break_safe_sheets = models.DateTimeField(auto_now_add=False, auto_now=False,
                                                   verbose_name="Запись начала перерыва", **NULLABLE)
    time_worked_per_day = models.TimeField(**NULLABLE)

    # status_work_wt = models.BooleanField(**NULLABLE)
    
    def __str__(self) -> str:
        return f'Номер таймшита {self.timesheet} '


class WorkTimeTable(tables.Table):
    class Meta:
        model = WorkTime




# def safe(self, force_insert=False, force_update=False, using=None, update_fields=None):
#
#     # work_safe_sheets = self.timesheet.lunch
# #     print('self.timesheet.status_work', self.timesheet.status_work)
#     status_work_wt = self.timesheet.status_work
#     super().save(force_insert, force_update, using, update_fields)
#     status_work_wt = self.timesheet.status_work
#     return status_work_wt
#     return work_safe_sheets#, status_work_wt

# from django.db.models import DurationField, ExpressionWrapper, F, IntegerField, Sum
#
# Timesheet.objects.annotate(
#     total_time=ExpressionWrapper(
#         ExpressionWrapper(F('out') - F('entry'), output_field=IntegerField()) -
#         ExpressionWrapper(F('lunch_end') - F('lunch'), output_field=IntegerField()),
#        output_field=DurationField()
#     )
# )
#
# from django.db.models import DurationField, ExpressionWrapper, F, IntegerField
#
#
# Timesheet.objects.aggregate(
#     total_time=Sum(
#         ExpressionWrapper(F('out') - F('entry'), output_field=IntegerField()) -
#         ExpressionWrapper(F('lunch_end') - F('lunch'), output_field=IntegerField()),
#        output_field=DurationField()
#     )
# )
# ['total_time']

# in view
# def timesheet(request):
#     c = Timesheet.objects.all()
#     context = {'c': c}
#     return render(request, "workingtime/timesheet.html", context)
# in html
# {% for ci in c %}
#     {{ ci.data }}: {{ ci.entry }} - {{ ci.out }}; {{ ci.total_time }}
# {% endfor %}
