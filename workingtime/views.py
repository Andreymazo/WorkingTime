from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, DeleteView, ListView, UpdateView, CreateView
from django_tables2 import SingleTableView, tables

from config import settings
from workingtime.forms import EmployeeForm, MyAuthForm, TimesheetForm, CustomUserForm
from workingtime.models import CustomUser, Employee, EmployeeTable, Timesheet, Employer, TimesheetTable


class CustomLoginView(LoginView):
    authentication_form = MyAuthForm
    # model = CustomUser
    # form_class = UserCustomCreationForm
    # success_url = reverse_lazy('workingtime:Product_list')


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('workingtime:home')


from django_tables2.utils import A  # alias for Accessor

from django_tables2 import TemplateColumn, LinkColumn


class EmploeeTableView(SingleTableView):
    table_class = EmployeeTable
    queryset = Employee.objects.all()
    template_name = "workingtime/employee_list.html"

    def get_queryset(self):
        queryset = Employee.objects.all()
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

#     delete = LinkColumn('workingtime:home', args=[A('pk')], attrs={
#         'a': {'class': 'btn'}
#     })


class EmploeeTable(ListView):
    model = Employee
    table_class = EmployeeTable
    template_name = "Employee_list2.html"

    # https: // glasshost.tech / django - tables2 - add - button - per - row /
    # queryset = Employee.objects.all()

    # acciones = TemplateColumn(
    #     template_code='<a href="{% url "workingtime:home2" record.id %}" class="btn btn-success">Ver</a>')

    class Meta:
        model = Employee
        exclude = (
            'engaged',
        )


from django.db.models import DurationField, ExpressionWrapper, F, IntegerField, Sum, QuerySet


class Timesheets(SingleTableView):
    table_class = TimesheetTable
    queryset = Timesheet.objects.all()
    template_name = "workingtime/timesheet.html"

    # def get_queryset(self):
    #     queryset = Timesheet.objects.all()
    #     lst_employees_emails = [i.customuser.email for i in Employee.objects.all()]
    #     if not self.request.user.is_authenticated:
    #         login_url = reverse_lazy('workingtime:login')
    #         return redirect(login_url)
    #         # return redirect(f"{settings.LOGIN_URL}?next={self.request.path}")
    #     if self.request.user.email in lst_employees_emails:
    #         self_req_employee_id = CustomUser.objects.get(email=self.request.user.email)
    #         queryset = Timesheet.objects.filter(employee_id=self_req_employee_id.employee.id)
    #         return queryset
    #     else:
    #         return queryset
    #
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


# class EmployeeList(ListView):
#     model = Employee
#     template_name = 'workingtime/employee_lst.html'
#     form_class = EmployeeForm
class EmployeeCreate(CreateView):
    model = Employee
    form_class = EmployeeForm
    success_url = reverse_lazy('workingtime:employee_lst')


class EmployeeUpdate(UpdateView):
    model = Employee
    form_class = EmployeeForm
    template_name = 'workingtime/employee_form.html'
    success_url = reverse_lazy('workingtime:employee_lst')


class EmployeeDetail(DetailView):
    model = Employee
    # template_name = 'workingtime/employee_detail.html'
    template_name = 'workingtime/employee_form.html'
    form_class = EmployeeForm

    def get(self, request, *args, **kwargs):
        print('==================', self.get_object())
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
        # c = Employee.objects.all().get(employer=Employer.objects.get(name='Вася'))
        self_req_employee_id = CustomUser.objects.get(email=self.request.user.email)
        print('===================+++++++++++++++++++++++get_object().id', self.get_object().id)
        print(self_req_employee_id.employee.id)
        # c = Timesheet.objects.all().filter(employee_id=self_req_employee_id.employee.id)
        c = Employee.objects.all().get(id=self.get_object().id)

        context = {'c': c,
                   'total_time': total_time,
                   'general_total_time': general_total_time['general_total_time']}
        return super(EmployeeDetail, self).get(request, *args, **kwargs)
        # return self.render_to_response(context)#"workingtime/employee_detail.html",


class EmployeeDelete(DeleteView):
    model = Employee
    template_name = 'workingtime/employee_confirm_delete.html'
    print('IF we was here [[[[[[[[[[[]]]]]]]]]]')
    success_url = reverse_lazy('workingtime:employee_lst')

    # form_class = EmployeeForm


# class BlogListView(ListView):
#     model = Post
#     template_name = 'home.html'
#
#
# class BlogDetailView(DetailView):
#     model = Post
#     template_name = 'post_detail.html'
#
#
# class BlogCreateView(CreateView):
#     model = Post
#     template_name = 'post_new.html'
#     fields = ['title', 'author', 'body']
#
#
# class BlogUpdateView(UpdateView):  # Новый класс
#     model = Post
#     template_name = 'post_edit.html'
#     fields = ['title', 'body']

# class BlogDeleteView(DeleteView): # Создание нового класса
#     model = Post
#     template_name = 'post_delete.html'
#     success_url = reverse_lazy('home')

class TimesheetLst(ListView):
    form_class = TimesheetForm
    template_name = 'workingtime/timesheets_without_tables2.html'

    def get_queryset(self):
        queryset = Timesheet.objects.all()
        lst_employees_emails = [i.customuser.email for i in Employee.objects.all()]
        if not self.request.user.is_authenticated:
            login_url = reverse_lazy('workingtime:login')
            return redirect(login_url)
            # return redirect(f"{settings.LOGIN_URL}?next={self.request.path}")
        if self.request.user.email in lst_employees_emails:
            self_req_employee_id = CustomUser.objects.get(email=self.request.user.email)
            queryset = Timesheet.objects.filter(employee_id=self_req_employee_id.employee.id)
            return queryset
        else:
            return queryset

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            login_url = reverse_lazy('workingtime:login')
            return redirect(login_url)
        tt = Timesheet.objects.annotate(
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

        self_req_employee_id = CustomUser.objects.get(email=request.user.email)
        print(self_req_employee_id.employee.name)
        c = Timesheet.objects.all().filter(employee_id=self_req_employee_id.employee.id)
        employee_name = self_req_employee_id.employee.name
        context = {'c': c,
                   'tt': tt,
                   'general_total_time': general_total_time['general_total_time'],
                   'employee_name': employee_name}
        # print(tt[0].entry)
        # print(general_total_time['general_total_time'])

        return render(request, "workingtime/timesheets_without_tables2.html", context)


class CustomUserLst(ListView):
    queryset = CustomUser.objects.all()
    form_class = CustomUserForm

    class Meta:
        model = CustomUser
        fields = '__all__'


# class CustomUserCreate(CreateView):
#     form_class = CustomUserForm
#     template_name = 'workingtime/customuser_with_employee.html'

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
