from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from workingtime.forms import EmployeeForm, CustomUserForm, EmployeeFormSet
from workingtime.models import CustomUser, Employee


# CompanyFormSet = inlineformset_factory(Company, CompanyImage, fields='__all__')
# def get(self, request, *args, **kwargs):
#     """
# #     Handles GET requests and instantiates blank versions of the form
# #     and its inline formsets.
# #     """
#
#     self.object = None
#     form_class = self.get_form_class()
#     form = self.get_form(form_class)
#     item_form = EmployeeFormSet()
#
#     return self.render_to_response(self.get_context_data(form=form,
#                                                          item_form=item_form, ))
###########################################################################################

#     self.object = None
#     form_class = self.get_form_class()
#     # form = self.get_form(form_class)
#     FormSet = inlineformset_factory(self.model, Employee, form=EmployeeForm, extra=1)
#
#     # company_form = CompanyFormSet()
#     # return self.render_to_response(
#     #     self.get_context_data(form=form,
#     #                           Form_Set=FormSet))
#     context = {
#         # 'form': form,
#         'Form_Set': FormSet
#     }
#     return self.render_to_response(context)

# def post(self, request, *args, **kwargs):
#     """
#     Handles POST requests, instantiating a form instance and its inline
#     formsets with the passed POST variables and then checking them for
#     validity.
#     """
#     FormSet = inlineformset_factory(self.model, Employee, form=EmployeeForm, extra=1)
#     self.object = None
#     form_class = self.get_form_class()
#     form = self.get_form(form_class)
#     company_form = FormSet(self.request.POST)
#     if (form.is_valid() and company_form.is_valid()):
#         return super(CustomuserCreateWithSubject, self).form_valid(form)
#     else:
#         return self.form_invalid(form, company_form)
#


# def view_name(request):
#     form = LessonForm()
#     formset = MaterialsFormset(instance=Lesson())
#     if request.method == 'POST':
#         form = LessonForm(request.POST)
#         if form.is_valid():
#             lesson = form.save()
#             formset = MaterialsFormset(request.POST, request.FILES,
#                                        instance=lesson)
#             if formset.is_valid():
#                 formset.save()
#                 return render(request, 'index.html', )
#     return render(request, "page.html", {
#         'form': form, 'formset': formset
#     })

# return super(EmployeeDetail, self).get(request, *args, **kwargs)
# return self.render_to_response(context)
# return super().get(request, *args, **kwargs)

# def get(self, request, *args, **kwargs):
#     self.object = None
#     return super().get(request, *args, **kwargs)
class CustomuserCreateWithEmployee(PermissionRequiredMixin, CreateView):  #
    model = CustomUser
    form_class = CustomUserForm
    template_name = 'workingtime/customuser_with_employee.html'
    success_url = reverse_lazy('workingtime:customuser_lst')
    permission_required = ["workingtime.add_customuser", "workingtime.view_customuser"]

    # def get_queryset(self, *args, **kwargs):
    #     lst_employees_emails = [i.customuser.email for i in Employee.objects.all()]
    #     # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', lst_employees_emails)
    #     self_req_employee_id = CustomUser.objects.get(email=self.request.user.email)
    #     print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', self_req_employee_id.email)
    #     if not self.request.user.is_authenticated or self_req_employee_id.email in lst_employees_emails:
    #         login_url = reverse_lazy('workingtime:login')
    #         return redirect(login_url)

    def get_context_data(self, **kwargs):
        print('super().get_context_data(**kwargs)', super().get_context_data(**kwargs))
        context_data = super().get_context_data(**kwargs)
        FormSet = inlineformset_factory(self.model, Employee, form=EmployeeForm, extra=1)

        if self.request.method == 'POST':
            formset = FormSet(self.request.POST, instance=self.object)
        else:
            formset = FormSet(instance=self.object)

        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        lst_employees_emails = [i.customuser.email for i in Employee.objects.all()]
        # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', lst_employees_emails)
        self_req_employee_id = CustomUser.objects.get(email=self.request.user.email)
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', self_req_employee_id.email)
        if not self.request.user.is_authenticated or self_req_employee_id.email in lst_employees_emails:
            login_url = reverse_lazy('workingtime:login')
            return redirect(login_url)
        context_data = self.get_context_data()
        formset = context_data['formset']
        print(self.request.method)
        # print('form', form)
        with transaction.atomic():
            self.object = form.save()
            if formset.is_valid():
                print('=+++++++++++++', formset.instance)
                formset.instance = self.object
                formset.save()
            else:
                # return super(CustomuserCreateWithEmployee, self).form_invalid(form)
                return HttpResponse("Failure")
        return super(CustomuserCreateWithEmployee, self).form_valid(form)
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

    # def form_valid(self, form, company_form):
    #     """
    #     Called if all forms are valid. Creates a Recipe instance along with
    #     associated Ingredients and Instructions and then redirects to a
    #     success page.
    #     """
    #     self.object = form.save()
    #     company_form.instance = self.object
    #     company_form.instance.user = self.request.user
    #     company_form.save()
    #     return HttpResponseRedirect(self.get_success_url())
    #
    # def form_invalid(self, form, company_form):
    #     """
    #     Called if a form is invalid. Re-renders the context data with the
    #     data-filled forms and errors.
    #     """
    #     return self.render_to_response(
    #         self.get_context_data(form=form,
    #                               company_form=company_form))


class CustomuserUpdateWithEmployee(PermissionRequiredMixin, UpdateView):  #
    model = CustomUser
    form_class = CustomUserForm
    template_name = 'workingtime/customuser_with_employee.html'
    success_url = reverse_lazy('workingtime:customuser_lst')
    permission_required = ["workingtime.add_customuser", "workingtime.view_customuser"]

    # def get_queryset(self, *args, **kwargs):
    #     lst_employees_emails = [i.customuser.email for i in Employee.objects.all()]
    #     # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', lst_employees_emails)
    #     self_req_employee_id = CustomUser.objects.get(email=self.request.user.email)
    #     print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', self_req_employee_id.email)
    #     if not self.request.user.is_authenticated or self_req_employee_id.email in lst_employees_emails:
    #         login_url = reverse_lazy('workingtime:login')
    #         return redirect(login_url)

    def get_context_data(self, **kwargs):
        print('super().get_context_data(**kwargs)', super().get_context_data(**kwargs))
        context_data = super().get_context_data(**kwargs)
        FormSet = inlineformset_factory(self.model, Employee, form=EmployeeForm, extra=1)

        if self.request.method == 'POST':
            formset = FormSet(self.request.POST, instance=self.object)
        else:
            formset = FormSet(instance=self.object)

        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        lst_employees_emails = [i.customuser.email for i in Employee.objects.all()]
        # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', lst_employees_emails)
        self_req_employee_id = CustomUser.objects.get(email=self.request.user.email)
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', self_req_employee_id.email)
        if not self.request.user.is_authenticated or self_req_employee_id.email in lst_employees_emails:
            login_url = reverse_lazy('workingtime:login')
            return redirect(login_url)
        context_data = self.get_context_data()
        formset = context_data['formset']
        print(self.request.method)
        # print('form', form)
        with transaction.atomic():
            self.object = form.save()
            if formset.is_valid():
                print('=+++++++++++++', formset.instance)
                formset.instance = self.object
                formset.save()
            else:
                # return super(CustomuserCreateWithEmployee, self).form_invalid(form)
                return HttpResponse("Failure")
        return super(CustomuserUpdateWithEmployee, self).form_valid(form)
