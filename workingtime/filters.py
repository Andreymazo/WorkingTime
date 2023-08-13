from datetime import timedelta

import django_filters
from django.db.models import Sum, ExpressionWrapper, F, fields, Func
from django.forms import inlineformset_factory
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView

from workingtime.forms import CustomUserForm, EmployeeForm
from workingtime.models import CustomUser, CustomUserTable, Employee, EmployeeTable, Timesheet
# class CustomUserFilter(django_filters.FilterSet):
#     email = django_filters.CharFilter(lookup_expr='iexact')
#     date_joined__gt = django_filters.NumberFilter(field_name='date_joined', lookup_expr='gt')
#
#     class Meta:
#         model = CustomUser
#         ordering = ('email',)
#         fields = ['email']

from django_filters import FilterSet
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin


class CustomUserFilter(FilterSet):
    class Meta:
        model = CustomUser
        # fields = {"email": ["exact", "contains"], "full_name": ["exact"]}
        fields = {
            # "nombre_estudio": ["icontains"],
            # "nombre_centro": ["icontains"],
            "id": ["gt"],
            # "nombre_asignatura": ["icontains"],
            # "cod_grupo_asignatura": ["exact"],
        }
        order_by = ["id"]


class FilteredCustomUserListView(SingleTableMixin, FilterView):
    table_class = CustomUserTable
    model = CustomUser
    template_name = "workingtime/customuser_list.html"
    filterset_class = CustomUserFilter

    # Сотрутник может видеть только свои данные, если попадет на этот ендпоинт

    def get_queryset(self):
        queryset = CustomUser.objects.all()
        lst_employees_emails = [i.customuser.email for i in Employee.objects.all()]
        if not self.request.user.is_authenticated:
            login_url = reverse_lazy('workingtime:login')
            return redirect(login_url)
        if self.request.user.email in lst_employees_emails:
            self_req_employee_id = CustomUser.objects.get(email=self.request.user.email)
            queryset = Employee.objects.filter(id=self_req_employee_id.employee.id)
            return queryset
        else:
            return queryset


class EmployeeFilter(FilterSet):
    class Meta:
        model = Employee
        # fields = {"email": ["exact", "contains"], "full_name": ["exact"]}
        fields = {
            # "nombre_estudio": ["icontains"],
            # "nombre_centro": ["icontains"],
            "id": ["exact"],
            # "nombre_asignatura": ["icontains"],
            # "cod_grupo_asignatura": ["exact"],
        }
        order_by = ["name"]


class FilteredEmployeeListView(SingleTableMixin, FilterView):
    table_class = EmployeeTable
    model = Employee
    template_name = "workingtime/employee_lst_filtered.html"  # lst django-tables2 + ListView
    filterset_class = EmployeeFilter
    queryset = Employee.objects.all()


# class TimesheetFilter(FilterSet):
    
    # class Meta:
        # model = Timesheet
        # fields = {"email": ["exact", "contains"], "full_name": ["exact"]}
        # fields = {
            # "datetime_complete": ["icontains"],
            # "datetime_start": ["icontains"],
            # "id": ["exact"],
            # "employee": ["icontains"],
            # "cod_grupo_asignatura": ["exact"],
        # }
        # order_by = ["name"]
        ########################################################################
    # employee = django_filters.CharFilter(lookup_expr='icontains')
    # @property
    # def sum(self):
    #     return Timesheet.objects.filter(worktime__status_work_wt=True)#.annotate(
    # duration=(F('worktime__time_break_safe_sheets') - F('datetime_start')))

    # duration = ExpressionWrapper(F('closed_at') - F('opened_at'), output_field=fields.DurationField())
    # objects = Timesheet.objects.closed().annotate(duration=duration).filter(duration__gt=timedelta(seconds=2))
    # qs = super(TimesheetFilter, self).qs
    # return qs.aggregate(Sum('worktime__time_break_safe_sheets'))#['worktime__work_safe_sheets__avg']#['id__avg']

    # @property
    # def get_sum_values(self):
    #     sum_values = self.objects.all().aggregate(Sum('value'))['value__sum']
    #     return sum_values
    # @property
    # def sum(self):
    #     qs = super(TimesheetFilter, self).qs
    #     return qs.aggregate(Sum(F('worktime__start_break_safe_sheets') - F('worktime__start_break_safe_sheets')))

    class Meta:
        model = Timesheet
        # fields = {"email": ["exact", "contains"], "full_name": ["exact"]}
        fields = {
            #     # "nombre_estudio": ["icontains"],
            #     # "nombre_centro": ["icontains"],
            "id": ["gt"],
            # "worktime__status_work_wt":["exact"], "employee":["exact"]#, "worktime__time_break_safe_sheets":["range"]
            #
            #     "employee":["exact"], "date":["contains"], "worktime__status_work_wt":
            #
            #     # "nombre_asignatura": ["icontains"],
            #     # "cod_grupo_asignatura": ["exact"],
        }
        order_by = ["id"]

        # fields = ['employee', 'date', 'worktime__status_work_wt', 'id'] #, "worktime__work_safe_sheets":["lt"]
