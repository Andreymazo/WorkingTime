from django.db import transaction
from django.forms import inlineformset_factory
from django.urls import reverse_lazy
from django.views.generic import CreateView

from workingtime.forms import EmployeeForm, CustomUserForm, EmployeeFormSet
from workingtime.models import CustomUser, Employee


class CustomuserCreateWithEmployee(CreateView):
    model = CustomUser
    form_class = CustomUserForm
    template_name = 'workingtime/customuser_with_employee.html'
    success_url = reverse_lazy('workingtime:customuser_lst')

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
    def get(self, request, *args, **kwargs):

        self.object = None
        print('ffffffffffffffff', self.object)
        FormSet = inlineformset_factory(self.model, Employee, form=EmployeeForm, extra=1)
        if self.request.method == 'POST':
            formset = FormSet(self.request.POST, instance=self.request.user)
        else:
            formset = FormSet(instance=self.object)
        # print('formset', formset)
        # context_data['formset'] = formset
        context = {
            'formset': formset
        }
        return self.render_to_response(context)
        # return super(EmployeeDetail, self).get(request, *args, **kwargs)
        # return self.render_to_response(context)
        # return super().get(request, *args, **kwargs)

    # def get(self, request, *args, **kwargs):
    #     self.object = None
    #     return super().get(request, *args, **kwargs)

    # def get_context_data(self, **kwargs):
    #     print('super().get_context_data(**kwargs)', super().get_context_data(**kwargs))
    #     context_data = super().get_context_data(**kwargs)
    #     FormSet = inlineformset_factory(self.model, Employee, form=EmployeeForm, extra=1)
    #
    #     if self.request.method == 'POST':
    #         formset = FormSet(self.request.POST, instance=self.object)
    #     else:
    #         formset = FormSet(instance=self.object)
    #
    #     context_data['formset'] = formset
    #     return context_data

    # def form_valid(self, form):
    #     context_data = self.get_context_data()
    #     formset = context_data['formset']
    #     print(self.request.method)
    #     print('=+++++++++++++', formset.instance)
    #     with transaction.atomic():
    #         self.object = form.save()
    #         if formset.is_valid():
    #             formset.instance = self.object
    #             formset.save()
    #         else:
    #             return super(CustomuserCreateWithSubject, self).form_invalid(form)
    #     return super(CustomuserCreateWithSubject, self).form_valid(form)

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
