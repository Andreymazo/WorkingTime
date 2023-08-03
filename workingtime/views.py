from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, DeleteView
from django_tables2 import SingleTableView
from workingtime.forms import EmployeeForm, MyAuthForm
from workingtime.models import CustomUser, Employee, EmployeeTable, Timesheet, Employer, TimesheetTable


class CustomLoginView(LoginView):
    authentication_form = MyAuthForm
    # model = CustomUser
    # form_class = UserCustomCreationForm
    # success_url = reverse_lazy('catalog:Product_list')


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('workingtime:home')


class EmploeeTableView(SingleTableView):
    table_class = EmployeeTable
    queryset = Employee.objects.all()
    template_name = "Employee_list.html"


from django.db.models import DurationField, ExpressionWrapper, F, IntegerField, Sum, QuerySet


class Timesheets(SingleTableView):
    table_class = TimesheetTable
    queryset = Timesheet.objects.all()
    template_name = "workingtime/timesheet.html"

    def get_queryset(self):
        queryset = Timesheet.objects.all()
        lst_emloyees_id = [i for i in Employee.objects.all().values_list('id', flat=True)]
        if self.request.user.id in lst_emloyees_id:
            print('+++++++++++++++++++++', self.request.user.id)
            queryset = Timesheet.objects.filter(employee_id=self.request.user.id)
            return queryset

        return queryset

    # def get(self, request, *args, **kwargs):
    #     # self.object = self.get_object()
    #     total_time = Timesheet.objects.annotate(
    #         total_time=ExpressionWrapper(
    #             ExpressionWrapper(F('out') - F('entry'), output_field=IntegerField()) -
    #             ExpressionWrapper(F('lunch_end') - F('lunch'), output_field=IntegerField()),
    #             output_field=DurationField()
    #         )
    #     )
    #
    #     general_total_time = Timesheet.objects.aggregate(
    #         general_total_time=Sum(
    #             ExpressionWrapper(F('out') - F('entry'), output_field=IntegerField()) -
    #             ExpressionWrapper(F('lunch_end') - F('lunch'), output_field=IntegerField()),
    #             output_field=DurationField()
    #         )
    #     )
    #     c = Timesheet.objects.all()
    #     context = {'c': c,
    #                'total_time': total_time,
    #                'general_total_time': general_total_time['general_total_time']}
    #     return render(request, "workingtime/timesheet.html", context)

    # def timesheet(self, request):
    #     total_time = self.model.annotate(
    #         total_time=ExpressionWrapper(
    #             ExpressionWrapper(F('out') - F('entry'), output_field=IntegerField()) -
    #             ExpressionWrapper(F('lunch_end') - F('lunch'), output_field=IntegerField()),
    #             output_field=DurationField()
    #         )
    #     )
    #
    #     general_total_time = self.model.aggregate(
    #         general_total_time=Sum(
    #             ExpressionWrapper(F('out') - F('entry'), output_field=IntegerField()) -
    #             ExpressionWrapper(F('lunch_end') - F('lunch'), output_field=IntegerField()),
    #             output_field=DurationField()
    #         )
    #     )
    #
    #     c = Timesheet.objects.all()
    #     context = {'c': c,
    #                'total_time': total_time,
    #                'general_total_time': general_total_time['general_total_time']}
    #
    #     return render(request, "workingtime/timesheet.html", context)


class EmployeeDetail(DetailView):
    model = Employee
    template_name = 'workingtime/employee_detail.html'
    form_class = EmployeeForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        total_time = Timesheet.objects.annotate(
            total_time=ExpressionWrapper(
                ExpressionWrapper(F('out') - F('entry'), output_field=IntegerField()) -
                ExpressionWrapper(F('lunch_end') - F('lunch'), output_field=IntegerField()),
                output_field=DurationField()
            )
        )

        general_total_time = Timesheet.objects.aggregate(
            general_total_time=Sum(
                ExpressionWrapper(F('out') - F('entry'), output_field=IntegerField()) -
                ExpressionWrapper(F('lunch_end') - F('lunch'), output_field=IntegerField()),
                output_field=DurationField()
            )
        )
        c = Employee.objects.all().get(employer=Employer.objects.get(name='Вася'))
        context = {'c': c,
                   'total_time': total_time,
                   'general_total_time': general_total_time['general_total_time']}
        return render(request, "workingtime/employee_detail.html", context)
    # form_class = EmployeeForm
    # queryset = Employee.objects.all()


class EmployeeDelete(DeleteView):
    model = Employee
    template_name = 'workingtime/employee_delete.html'
    form_class = EmployeeForm
    queryset = Employee.objects.all()

# class TableListView(SingleTableView):
#     model = Values_table
#     table_class = Values_tableTable
#     # generate_values()
#     template_name = "spa_table/Values_table_list.html"
#     ordering = ('distance',)  # quantity, name
#     table_pagination = {"per_page": 5}
#
    # def get_queryset(self, **kwargs):
    #     """
    #     Return the list of items for this view.
    #
    #     The return value must be an iterable and may be an instance of
    #     `QuerySet` in which case `QuerySet` specific behavior will be enabled.
    #     """
    #     if self.request.method == "GET":
    #
    #         if self.queryset is not None:
    #             queryset = self.queryset
    #             if isinstance(queryset, QuerySet):
    #                 queryset = queryset.all()
    #         if self.model is not None:
    #             queryset = self.model._default_manager.all()
    #         else:
    #             raise ImproperlyConfigured(
    #                 "%(cls)s is missing a QuerySet. Define "
    #                 "%(cls)s.model, %(cls)s.queryset, or override "
    #                 "%(cls)s.get_queryset()." % {"cls": self.__class__.__name__}
    #             )
    #         ordering = self.get_ordering()
    #         if ordering:
    #             if isinstance(ordering, str):
    #                 ordering = (ordering,)
    #             queryset = queryset.order_by(*ordering)
#         Values_table.objects.all().delete()
#
#         for i in range(1, 10):
#             generate_values()
#
#         return queryset
