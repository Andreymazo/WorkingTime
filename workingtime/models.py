from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models
from django.shortcuts import render
from django.utils import timezone
from django_tables2 import tables, TemplateColumn
from pip._internal.utils._jaraco_text import _

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
    employee = models.ForeignKey('workingtime.Employee', on_delete=models.CASCADE, related_name='timesheet')
    date = models.DateField(auto_now=False, auto_now_add=False, verbose_name="Data")
    entry = models.TimeField(auto_now=False, auto_now_add=False, verbose_name="Начало рабочего дня", default='09:00:00')
    lunch = models.TimeField(auto_now=True, auto_now_add=False, null=True, blank=True, verbose_name="Начало перерыва")
    out = models.TimeField(auto_now=False, auto_now_add=False, verbose_name="Конец рабочего дня", default='18:00:00')

    class Meta:
        ordering = ["id"]
        verbose_name_plural = "Таймшиты"
###Эта функция не дает нормально жить, надо разобраться, но без нее тоже не очень. не сохранятеся в базе ворктайм
    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        j = WorkTime.objects.create(work_safe_sheets=self.lunch, timesheet_id=self.id, status_work_wt=self.status_work)
        j.save()
        timesheet_employee_name = self.employee.name
        super().save(force_insert, force_update, using, update_fields)
        return j

    # print(employee.customuser.email)
    def __str__(self):
        return f" Таймшит относится к сотруднику: {self.employee.name}  id:{self.employee.id} id таймшита: {self.id}"


class TimesheetTable(tables.Table):
    class Meta:
        model = Timesheet


class WorkTime(models.Model):
    timesheet = models.ForeignKey('workingtime.Timesheet', related_name='worktime', on_delete=models.CASCADE, **NULLABLE)
    work_safe_sheets = models.TimeField(auto_now_add=False, auto_now=True, **NULLABLE)
    status_work_wt = models.BooleanField(**NULLABLE)


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
