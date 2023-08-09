from http import HTTPStatus

from django.forms import inlineformset_factory
from django.http import response, HttpResponse
from django.test import TestCase
from django.urls import reverse

from workingtime.forms import EmployeeForm, CustomUserForm
from workingtime.models import CustomUser, Employer, Employee

from django.test import Client


class MyTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(email='andreymazo@try.ru', password='qwert123asd')
        # self.user.set_pasword('qwert123asd')
        # self.user.save()
        self.client = Client()
        # self.user = User.objects.create_user(username='user_1', password='1X<ISRUkw+tuK')
        self.client.force_login(user=self.user)

        # self.author = Author.objects.create(first_name='Christian', last_name='Author')

        self.path = reverse('workingtime:customuser_create')

    def test_post_inlineformset_factory(self):
        # print(self.client.__dict__)
        CustomUserFormSet = inlineformset_factory(CustomUser, Employee, form=CustomUserForm,
                                                formset=EmployeeForm,
                                                extra=1, max_num=20, can_delete=False)
        self.user2 = CustomUser.objects.create(email='eamilfortest@ugr.ru', password='qwert123asd')
        employer = Employer.objects.create(name='Vasia', customuser=self.user)
        employee = Employee.objects.create(employer=employer, customuser=self.user2)
        form_data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1',
            'customuser': self.user2.id,
            'employer': employer.id,
            'name': 'test employee',
            'password': 'qwert123asd',
            'email':'qwrrtr@wejhg.ru',
            'full_name': 'andry',
            'is_staff':True,
            'is_admin':False,
            'is_active':True
        }
        formset = CustomUserFormSet(form_data, instance=employee)
        if formset.is_valid():
            return HttpResponse('worked')
        else:
            formset = CustomUserFormSet(form_data, instance=employee)
            # formset = AlbumFormSet()
        print('formset.errors', formset.errors)
        formset.save()
        # self.assertTrue(formset.is_valid())
        # data = {'form-customuser': self.user.id,
        #         'form-employer':employer.id,
        #         'formname':'test employee'}

                # 'password':'qwert123asd',
                # 'email':'qwrrtr@wejhg.ru',
                # 'full_name': 'andry',
                # 'is_staff':True,
                # 'is_admin':False,
                # 'is_active':True}
        # employee = Employee.objects.create(customuser=self.user, employer=employer)
        # employee.save()
        # assert_count = Employee.objects.count()
        # # print(assert_count)
        assert_count = CustomUser.objects.count()
        response = self.client.post(self.path, data=form_data, content_type="application/json", follow=True)
        # print(assert_count, '------------', response.context_data)
        print(response.context['form'].errors)
        # #fields=(password;last_login;email;full_name;is_staff;is_admin;is_active)
        # # self.assertFormError(response, 'form', 'something', 'This field is required.')status.HTTP_201_CREATED
        print(response.context['errors'].__dict__)

        self.assertEqual(assert_count, CustomUser.objects.count() - 1)
        self.assertEqual(response.status_code, HTTPStatus.OK)  #
        # form = CustomUserForm()
        # self.assertFormSetError(response,
        #                         formset='form',
        #                         form_index=1,
        #                         field='name',
        #                         errors='Second author name should contain consonants')
        # https: // simpleit.rocks / python / django / forms / using - formsets -
        # with-django - cbv - generic - views /

        # https: // whoisnicoleharris.com / 2015 / 01 / 06 / implementing - django - formsets.html


        # self.assertEqual(assert_count, Employee.objects.count() - 1)


# def test_post(self):
#        data = {"name": "New Document Flow"}
#
#        response = self.unsigned_user.post(reverse(self.path), data=data)
#        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#        response = self.api_user.post(reverse(self.path), data=data)
#        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
