from django.urls import path
from workingtime.apps import WorkingtimeConfig
from workingtime.filters import FilteredCustomUserListView, CustomUserList
from workingtime.formset import CustomuserCreateWithEmployee, CustomuserUpdateWithEmployee
from workingtime.models import CustomUser, CustomUserTable
from workingtime.views import CustomLoginView, \
    EmployeeDetail, EmployeeDelete, Timesheets, EmploeeTable, TimesheetLst, EmployeeUpdate, EmployeeCreate, \
    EmploeeTableView, CustomUserLst, TimesheetsCreateView, TimesheetsUpdateView, TimesheetsDetailView, \
    TimesheetsDeleteView, WorkTimeListView, WorkTimeCreateView, WorkTimeUpdateView, WorkTimeDetailView, \
    WorktimeDeleteView

app_name = WorkingtimeConfig.name

urlpatterns = [

    path('', CustomLoginView.as_view(template_name='registration/login.html'), name='login'),

    path('customuser_lst2/', CustomUserList.as_view(), name='customuser_lst2'),
    path('customuser_lst/', FilteredCustomUserListView.as_view(), name='customuser_lst'),
    path('customuser_create/', CustomuserCreateWithEmployee.as_view(), name='customuser_create'),
    path('customuser_update/<int:pk>', CustomuserUpdateWithEmployee.as_view(), name='customuser_update'),
    path('employee_self/', EmploeeTableView.as_view(), name='employee_self'),
    path('employee_lst/', EmploeeTable.as_view(template_name="workingtime/employee_list2.html"), name='employee_lst'),
    ##Либо кастомюзер create с Емплоии, либо просто Емплоии create. Одно комментируем.
    # path('employee_create/', EmployeeCreate.as_view(template_name="workingtime/employee_form.html"), name='employee_create'),
    path('employee_detail/<int:pk>', EmployeeDetail.as_view(template_name="workingtime/employee_detail.html"), name='employee_detail'),
    #Либо кастомюзер апдейт с Емплоии, либо просто Емплоии апдейт. Одно комментируем.
    # path('employee_update/<int:pk>', EmployeeUpdate.as_view(template_name="workingtime/employee_form.html"), name='employee_update'),
    path('employee_delete/<int:pk>', EmployeeDelete.as_view(template_name='workingtime/employee_confirm_delete.html'), name='employee_delete'),

    # path('customuser_lst/', CustomUserLst.as_view(table_class = CustomUserTable, model=CustomUser, template_name ='workingtime/customuser_list.html', table_pagination={ "per_page":5 } ) , name='filtered_customuser_lst'),
    path('timesheet_get_self_time/', TimesheetLst.as_view(), name='timesheet_lst_self_time'),
    path('timesheet/', Timesheets.as_view(template_name="workingtime/timesheet.html"), name='timesheet'),
    path('timesheet_create/', TimesheetsCreateView.as_view(template_name="workingtime/timesheet_form.html"), name='timesheet_create'),
    path('timesheet_update/<int:pk>', TimesheetsUpdateView.as_view(template_name="workingtime/timesheet_form.html"), name='timesheet_update'),
    path('timesheet_detail/<int:pk>', TimesheetsDetailView.as_view(template_name="workingtime/timesheet_form.html"), name='timesheet_detail'),
    path('timesheet_delete/<int:pk>', TimesheetsDeleteView.as_view(template_name="workingtime/timesheet_confirm_delete.html"), name='timesheet_delete'),

    path('worktime_lst/', WorkTimeListView.as_view(template_name="workingtime/worktime_lst.html"), name='worktime_lst'),
    path('worktime_create/', WorkTimeCreateView.as_view(template_name="workingtime/worktime_form.html"), name='worktime_create'),
    path('worktime_update/<int:pk>', WorkTimeUpdateView.as_view(template_name="workingtime/worktime_update.html"), name='worktime_update'),
    path('worktime_detail/<int:pk>', WorkTimeDetailView.as_view(template_name="workingtime/worktime_detail.html"), name='worktime_detail'),
    path('worktime_delete/<int:pk>', WorktimeDeleteView.as_view(template_name="workingtime/worktime_confirm_delete.html"), name='worktime_delete'),

]
