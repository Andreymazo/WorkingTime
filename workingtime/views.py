from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.datetime_safe import datetime
from django.views.generic import DetailView, DeleteView, ListView, UpdateView, CreateView
from django_filters.views import FilterView
from django_tables2 import SingleTableView, tables, SingleTableMixin
from pip._internal.utils._jaraco_text import _

from config import settings
from workingtime.filters import CustomUserFilter, TimesheetFilter
from workingtime.forms import EmployeeForm, MyAuthForm, TimesheetForm, CustomUserForm, WorkTimeForm
from workingtime.models import CustomUser, Employee, EmployeeTable, Timesheet, Employer, TimesheetTable, \
    CustomUserTable, WorkTime, WorkTimeTable


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

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(
                    self.object_list, "exists"
            ):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(
                    _("Empty list and “%(class_name)s.allow_empty” is False.")
                    % {
                        "class_name": self.__class__.__name__,
                    }
                )
        context = self.get_context_data()
        return self.render_to_response(context)

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


class EmployeeTableView(ListView):
    model = Employee
    table_class = EmployeeTable
    template_name = "workingtime/Employee_list2.html"

    # https: // glasshost.tech / django - tables2 - add - button - per - row /
    # queryset = Employee.objects.all()

    # acciones = TemplateColumn(
    #     template_code='<a href="{% url "workingtime:home2" record.id %}" class="btn btn-success">Ver</a>')

    class Meta:
        model = Employee
        exclude = (
            'engaged',
        )


from django.db.models import DurationField, ExpressionWrapper, F, IntegerField, Sum, QuerySet, Value, Func, When, Case


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
    template_name = 'workingtime/employee_detail.html'
    # form_class = EmployeeForm

    #Сейчас другеи поля считают в таймшите и в worktime
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        # total_time = Timesheet.objects.annotate(
        #     total_time=ExpressionWrapper(
        #         ExpressionWrapper(F('out') - F('entry'), output_field=IntegerField()) -
        #         ExpressionWrapper(F('lunch_end') - F('lunch'), output_field=IntegerField()),
        #         output_field=DurationField()
        #     )
        # )

        # general_total_time = Timesheet.objects.aggregate(
        #     general_total_time=Sum(
        #         ExpressionWrapper(F('out') - F('entry'), output_field=IntegerField()) -
        #         ExpressionWrapper(F('lunch_end') - F('lunch'), output_field=IntegerField()),
        #         output_field=DurationField()
        #     )
        # )
        
        # c = Employee.objects.all().get(employer=Employer.objects.get(name='Вася'))
        self_req_employee_id = CustomUser.objects.get(email=self.request.user.email)
        print('===================+++++++++++++++++++++++get_object().id', self.get_object().id)
        #Если заходит админ, то у него нет сущности employee, либо коммент оставить, либо обработать
        # print(self_req_employee_id.employee.id)
        # c = Timesheet.objects.all().filter(employee_id=self_req_employee_id.employee.id)
        c = Employee.objects.all().get(id=self.get_object().id)
        data =  Employee.objects.all()
        total_time = Timesheet.objects.aggregate(Sum('worktime__time_worked_per_day'))
        context = {'c': c,
                   'cc':data,
                   'total_time': total_time['worktime__time_worked_per_day__sum'],}
                #    'general_total_time': general_total_time['general_total_time']}
        # context = self.get_context_data()
        # return self.render_to_response(context)

        context['table'] = data
        return self.render_to_response(context)
        # return super(EmployeeDetail, self).get(request, *args, **kwargs)
        # return self.render_to_response(context)#"workingtime/employee_detail.html",


class EmployeeDelete(DeleteView):
    model = Employee
    template_name = 'workingtime/employee_confirm_delete.html'
    success_url = reverse_lazy('workingtime:employee_lst')


class TimesheetsFilteredFilterView(FilterView, SingleTableView):
    model = Timesheet
    table_class = TimesheetTable
    queryset = Timesheet.objects.all()
    template_name = "workingtime/timesheet.html"
    filterset_class = TimesheetFilter

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        q = Timesheet.objects.all()
        #Tak ne rabotaet
        # ff = q.annotate(sum_difference=(ExpressionWrapper(F('worktime__start_break_safe_sheets') -
        #             F('worktime__end_break_safe_sheets'), output_field=DurationField())))

        # f = []
        # ff = []

        #     f.append(i)
        # now = timezone.now()
        # now = datetime.now()
        # f.append([((now - timedelta(ii.end_break_safe_sheets)).hour-(now-timedelta(ii.start_break_safe_sheets)).hour for i,ii in enumerate(q))])
        # print(f[0])
        # s=0
        # for i in f:
        #     s += i
        # print('========================', s)
        # ff.append([ii.start_break_safe_sheets for i,ii in enumerate(q)])

        # ff=Sum(f)

        # for i, ii in enumerate(WorkTime.objects.all()):
        #     print((i,ii)) # Timesheet.objects.all():
        #     f.append((i, type(ii)))
        #     print('______________________', (ff))



        # ded_time = Timesheet.objects.annotate(
        #     deduct_time=Sum((F('worktime__end_break_safe_sheets') - F('worktime__start_break_safe_sheets')))
        # )
        # total_time = Timesheet.objects.annotate(
        #
        #     total_time=ExpressionWrapper(
        #         ExpressionWrapper(F('datetime_complete') - F('datetime_start'), output_field=IntegerField())
        #         - ded_time,
        #         # -
        #         # ExpressionWrapper(
        #             # Sum((F('worktime__end_break_safe_sheets') - F('worktime__start_break_safe_sheets'))),
        #             # output_field=IntegerField()),
        #         output_field=DurationField()
        #     )
        # )
        general_total_time = Timesheet.objects.aggregate(Sum('worktime__time_worked_per_day'))
        # general_total_time = Timesheet.objects.aggregate(
        #     general_total_time=Sum(
        #         ExpressionWrapper(F('datetime_complete') - F('datetime_start'), output_field=IntegerField()) -
        #         ExpressionWrapper((F('worktime__start_break_safe_sheets') - F('worktime__end_break_safe_sheets')),
        #                           output_field=IntegerField()),
        #         output_field=DurationField()
        #     )
        # )
        # c = Employee.objects.all().get(employer=Employer.objects.get(name='Вася'))
        self_req_employee_id = CustomUser.objects.get(email=self.request.user.email)
        # print('===================+++++++++++++++++++++++get_object().id', self.get_object().id)
        # print(self_req_employee_id.employee.id)

        data = Timesheet.objects.all()#.filter(employee_id=self_req_employee_id.employee.id)
        context = {'object_list': data,
                #    'ff':ff,
                   #'total_time': total_time,
                   'general_total_time': general_total_time['worktime__time_worked_per_day__sum']
                #    'general_total_time': general_total_time['general_total_time']
                   }
        # context = self.get_context_data(**kwargs)
        context['table'] = data
        return self.render_to_response(context)

        # c = Employee.objects.all().get(id=self.get_object().id)

    #     # self.object = self.get_object()
    #     # if self.object.status_work and self.object.datetime_complete.exists():
    #     lst_poz_times = [Timesheet.objects.all().filter(worktime__time_break_safe_sheets=)]
    #         total_time = Timesheet.objects.annotate(
    #             total_time=ExpressionWrapper(
    #                 ExpressionWrapper(F('datetime_start') + F('time_break'), output_field=IntegerField()) -
    #                 ExpressionWrapper(F('lunch_end') - F('lunch'), output_field=IntegerField()),
    #                 output_field=DurationField()
    #             )
    #         )
    #     context = {'c': c,
    #           'total_time': total_time,
    #           'general_total_time': general_total_time['general_total_time']}
    #     context = self.get_context_data()

    # return render(request, "workingtime/timesheet.html", context)
    # def get(self, request, *args, **kwargs):
    #     self.object_list = self.get_queryset()
    ##  Соберем в один кверисет врем с Тру, в другой время с Фолс
    # queriset1 = Timesheet.objects.annotate(username_index=Func(F('username'), Value('(\d+)'), function='substring')).filter(status_work_wt__worktime=True) #'^[A-Z]{2}\d+$'
    # q = Timesheet.objects.annotate(status_work_wt__index=Func()).filter(worktime__status_work_wt=True)
    # queriset1 = WorkTime.objects.annotate(status_work_wt=Func()).filter(status_work_wt=True)
    # print('---------------------------', type(queriset1))
    # data = Timesheet.objects.all()
    # data = self.get_context_data(**kwargs)
    # data = q
    # context = self.get_context_data(**kwargs)
    # context['table'] = data
    #
    # context = {'q': q,
    #            'table':data}
    # return render(request, "workingtime/timesheet.html", context)

    # total_time = Timesheet.objects.annotate(
    #     total_time=ExpressionWrapper(
    #         ExpressionWrapper(F('out') - F('entry'), output_field=IntegerField()) -
    #         ExpressionWrapper(F('lunch_end') - F('lunch'), output_field=IntegerField()),
    #         output_field=DurationField()
    #     )
    # )
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


from django.db.models import ExpressionWrapper, F, fields


class TimesheetLst(ListView):
    form_class = TimesheetForm
    template_name = 'workingtime/timesheets_without_tables2.html'

    def get_queryset(self):
        # print('?????????????????????????????????', self.request.user.email )
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
            queryset = Timesheet.objects.all()
            return queryset

    ################### Убрал lunch_end из таймшита, пока пусть закомментировано будет, считаем по-другому################
    def get(self, request, *args, **kwargs):
        #     # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', self.request.user.email)
        #     if not self.request.user.is_authenticated:
        #         login_url = reverse_lazy('workingtime:login')
        #         return redirect(login_url)
        #     lst_employees_emails = [i.customuser.email for i in Employee.objects.all()]
        #     # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', lst_employees_emails)
        #     self_req_employee_id = CustomUser.objects.get(email=request.user.email)
        #     # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', self_req_employee_id.email)
        #     if self_req_employee_id.email not in lst_employees_emails:
        #         # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        cc = Timesheet.objects.all()
        tt = WorkTime.objects.aggregate(Sum('time_worked_per_day'))
        # ItemPrice.objects.aggregate(Sum('price'))
        # total_time = cc.annotate(
        #     ttt=ExpressionWrapper(
        #         ExpressionWrapper(F('datetime_complete') - F('datetime_start'), output_field=fields.IntegerField()),

                # -
                # ExpressionWrapper((F('worktime__time_break_safe_sheets'), F('worktime__status_work_wt'==False)) - F('worktime__time_break_safe_sheets', F('worktime__status_work_wt'=True)), output_field=IntegerField()),
                # delta = When(worktime__status_work_wt=False, then=(F('worktime__time_break_safe_sheets'))))
                # output_field=DurationField()
            # )
        # )

        # total_time = cc.annotate(
        #     total_time=ExpressionWrapper(
        #         ExpressionWrapper(F('out') - F('entry'), output_field=IntegerField()) -
        #         ExpressionWrapper(F('lunch_end') - F('lunch'), output_field=IntegerField()),
        #         output_field=DurationField()
        #     )
        # )
        #
        # general_total_time = cc.aggregate(
        #     general_total_time=Sum(
        #         ExpressionWrapper(F('out') - F('entry'), output_field=IntegerField()) -
        #         ExpressionWrapper(F('lunch_end') - F('lunch'), output_field=IntegerField()),
        #         output_field=DurationField()
        #     )
        # )
        self_req_employee_id = CustomUser.objects.get(email=request.user.email)
        self_name = self_req_employee_id.email
        context = {
            'cc': cc,
            'tt':tt['time_worked_per_day__sum'],
            #'total_time': total_time,
            # 'general_total_time': general_total_time['general_total_time'],
            'employee_name': self_name

        }
        return render(request, "workingtime/timesheets_without_tables2.html", context)


#
#     lst_employees_emails = [i.customuser.email for i in Employee.objects.all()]
#     self_req_employee_id = CustomUser.objects.get(email=request.user.email)
#     # if self_req_employee_id in lst_employees_emails:
#     print(self_req_employee_id.employee.name)
#     c = Timesheet.objects.all().filter(employee_id=self_req_employee_id.employee.id)
#     employee_name = self_req_employee_id.employee.name
#     # print('c', c)
#
#     tt = c.annotate(
#         total_time=ExpressionWrapper(
#             ExpressionWrapper(F('out') - F('entry'), output_field=IntegerField()) -
#             ExpressionWrapper(F('lunch_end') - F('lunch'), output_field=IntegerField()),
#             output_field=DurationField()
#         )
#     )
#
#     general_total_time = c.aggregate(
#         general_total_time=Sum(
#             ExpressionWrapper(F('out') - F('entry'), output_field=IntegerField()) -
#             ExpressionWrapper(F('lunch_end') - F('lunch'), output_field=IntegerField()),
#             output_field=DurationField()
#         )
#     )
#
#     context = {
#         'c': c,
#         'tt': tt,
#         'general_total_time': general_total_time['general_total_time'],
#         'employee_name': employee_name
#     }
#
#     # print(tt[0].entry)
#     # print(general_total_time['general_total_time'])
#
#     return render(request, "workingtime/timesheets_without_tables2.html", context)
# context = Timesheet.objects.all()
# return context
############################################################################

class TimesheetsCreateView(CreateView):
    model = Timesheet
    form_class = TimesheetForm
    template_name = 'workingtime/timesheet_form.html'

    def get_success_url(self):
        return reverse_lazy('workingtime:timesheet_update', kwargs={'pk': self.object.pk})


class TimesheetsUpdateView(UpdateView):
    model = Timesheet
    form_class = TimesheetForm
    success_url = reverse_lazy('workingtime:timesheet_update')
    template_name = 'workingtime/timesheet_form.html'

    def get_success_url(self):
        return reverse_lazy('workingtime:timesheet_update', kwargs={'pk': self.object.pk})


class TimesheetsDetailView(SingleTableMixin, FilterView, DetailView):
    table_class = TimesheetTable
    model = Timesheet
    form_class = TimesheetForm
    success_url = reverse_lazy('workingtime:timesheet_lst_self_time')
    template_name = 'workingtime/timesheet_detail.html'
    filterset_class = TimesheetFilter

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self_req_timesheet_id = Timesheet.objects.get(id=self.object.pk)
        self_name = self_req_timesheet_id.employee.name
        context = {
            'object_list': self_req_timesheet_id,  # self.get_context_data(object=self.object),
            'self_name': self_name
        }
        return render(request, "workingtime/timesheet_detail.html", context)


class TimesheetsDeleteView(DeleteView):
    queryset = Timesheet.objects.all()
    form_class = TimesheetForm
    success_url = reverse_lazy('workingtime:timesheet_lst_self_time')
    template_name = 'workingtime/timesheet_confirm_delete.html'


class WorkTimeListView(SingleTableView):
    table_class = WorkTimeTable
    queryset = WorkTime.objects.all()
    template_name = "workingtime/worktime_lst.html"


class WorkTimeCreateView(CreateView):
    model = WorkTime
    form_class = WorkTimeForm
    template_name = 'workingtime/worktime_form.html'

    def get_success_url(self):
        return reverse_lazy('workingtime:worktime_update', kwargs={'pk': self.object.pk})


class WorkTimeUpdateView(UpdateView):
    model = WorkTime
    form_class = WorkTimeForm
    success_url = reverse_lazy('workingtime:worktime_update')
    template_name = 'workingtime/worktime_form.html'

    def get_success_url(self):
        return reverse_lazy('workingtime:worktime_update', kwargs={'pk': self.object.pk})


class WorkTimeDetailView(DetailView):
    model = WorkTime
    form_class = WorkTimeForm
    success_url = reverse_lazy('workingtime:timesheet_lst_self_time')
    template_name = 'workingtime/worktime_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = {
            'object_list': self.get_context_data(object=self.object),
        }
        return render(request, "workingtime/worktime_detail.html", context)


class WorktimeDeleteView(DeleteView):
    queryset = WorkTime.objects.all()
    form_class = WorkTimeForm
    success_url = reverse_lazy('workingtime:timesheet_lst_self_time')
    template_name = 'workingtime/worktime_confirm_delete.html'


###############################
class CustomUserList(ListView):
    model = CustomUser
    queryset = CustomUser.objects.all()


# Эта закомментрованная функция добавляет форму к формсету, сейчас откуда-то берется, но если исчезнет,
# то ее надо будет раскоментровать и добавить туда, где формсет
# def get(self, request, *args, **kwargs):
#     print('Get Get get')
#     form = CustomUserForm()
#     self.object = None
#     FormSet = inlineformset_factory(self.model, Employee, form=EmployeeForm, extra=1)
#     if self.request.method == 'POST':
#
#         formset = FormSet(self.request.POST, instance=self.request.user)
#     else:
#         formset = FormSet(instance=self.object)
#     context = {'form': form,
#                'formset': formset
#                }
#     return self.render_to_response(context)


class CustomUserLst(ListView):
    queryset = CustomUser.objects.all()
    form_class = CustomUserForm
    ordering = ('email',)

    # def get_queryset(self):
    #     print('oooooooooooooooooo')
    #     """
    #     Не нашел в django-filters ничего проще ,чем переписать кверисет ,чтобы отсортировать по имени, но вот так сортирует
    #     """
    #     queryset = CustomUser.objects.all().order_by('email')
    #     return queryset

    class Meta:
        model = CustomUser
        fields = '__all__'
################################################################
# class CustomUserLst(SingleTableView):
#     table_class = CustomUserTable
#     queryset = CustomUser.objects.all()
#     form_class = CustomUserForm
#     # ordering = ('email',)
#     template_name = 'django_tables2/bootstrap.html'
#     context_filter_name = "filter"
#
#     def get_table_data(self):
#         f = CustomUserFilter(self.request.GET, queryset=CustomUser.objects.all(), request=self.request)
#         return f
#
#     def get_context_data(self, **kwargs):
#         context = super(CustomUserLst, self).get_context_data(**kwargs)
#         f = CustomUserFilter(self.request.GET, queryset=CustomUser.objects.all(), request=self.request)
#         context['form'] = f.form
#         return context
#
#     class Meta:
#         model = CustomUser
#         fields = '__all__'
######################################################
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
