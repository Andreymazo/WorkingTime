import django_filters
from django.forms import inlineformset_factory
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView

from workingtime.forms import CustomUserForm, EmployeeForm
from workingtime.models import CustomUser, CustomUserTable, Employee
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


class CustomUserList(ListView):
    model = CustomUser
    queryset = CustomUser.objects.all()

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
