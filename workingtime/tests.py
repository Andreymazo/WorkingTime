from http import HTTPStatus

from django.http import response
from django.test import TestCase
from django.urls import reverse

from workingtime.models import CustomUser, Employer, Employee

from django.test import Client


class MyTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email='andreymazo@try.ru', password='qwert123asd')
        # self.user.set_pasword('qwert123asd')
        # self.user.save()
        self.client = Client()
        # self.user = User.objects.create_user(username='user_1', password='1X<ISRUkw+tuK')
        self.client.force_login(user=self.user)

        # self.author = Author.objects.create(first_name='Christian', last_name='Author')

        self.path = reverse('workingtime:customuser_create')

    def test_post(self):
        print(self.client.__dict__)
        employer = Employer.objects.create(name='Vasia', customuser=self.user)

        data = {'email': 'something@may.ru', 'password': 'qwert123asd', }
        employee = Employee.objects.create(customuser=self.user, employer=employer)
        employee.save()
        assert_count = CustomUser.objects.count()
        print(assert_count, CustomUser.objects.all().values_list())
        response = self.client.post(self.path, data=data, content_type="application/json")
        print(assert_count)
        # self.assertFormError(response, 'form', 'something', 'This field is required.')status.HTTP_201_CREATED
        self.assertEqual(response.status_code, HTTPStatus.OK)  #
        self.assertEqual(assert_count, CustomUser.objects.count() - 1)

# def test_post(self):
#        data = {"name": "New Document Flow"}
#
#        response = self.unsigned_user.post(reverse(self.path), data=data)
#        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#        response = self.api_user.post(reverse(self.path), data=data)
#        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
