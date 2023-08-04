from django.core.files.storage import FileSystemStorage
from django.forms import inlineformset_factory
from django.http import request
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy, reverse

from catalog.forms import SubjectForm, ProductForm
from catalog.models import Category, Product, Record, Subject
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.http import HttpResponseBadRequest
from django.core.cache import cache
from config import settings

# def hello(request):
#     if request.method == 'POST':
#         # print(request.method)
#         print(request.POST.get('name'))
#         print(request.POST.get('e-mail'))
#         print(request.POST.get('message'))
# return render(request, 'catalog/index.html')
# return render(request, 'catalog/index.html')

# def category(request):
#     context = {
#         'object_list': Category.objects.all()
#     }
#     return render(request, 'catalog/products.html', context)


Record.views_controller = 0

@login_required
def products(request):
    g = Record.views_controller
    g += 1
    context = {
        'object_list': Product.objects.all(),
        'g': g

    }
    return render(request, 'catalog/products.html', context)


# def vivod_postatusu(request):
#     context = {'object_list': Record.objects.all()}
#     return render(request, 'catalog/record_detail.html', context)

@login_required()
def contact_us(request):


    if request.method == 'POST':
        # print(request.method)
        # print(request.POST.get('name'))
        print(request.POST.get('e-mail'))
        print(request.POST.get('message'))
    return render(request, 'catalog/contact_us.html')


# def crab1(request):
#     context = {
#         'object_list': Record.objects.all()
#
#     }
#     return render(request, 'catalog/crab1.html', context)
# def contacts(request):
#     return render(request, 'catalog/contact_us.html')
# def vivod_postatusu(request):
#     if Record.id_public != True:
#         context = {'object_list': Record.objects.all()}
#         return render(request, 'catalog/record_detail.html', context)
######################################
def get_counter(requests):
    if requests.method == "GET":
        g = Record.views_controller
        g += 1
        print(f'CounteEEEEr  {g}')
        context = {"g": g}
        return render(requests, context)

class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    # form_class = CategoryForm
    success_url = reverse_lazy('catalog:Category_List')

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:Product_list')
    template_name = 'catalog/Product_list.html'


class ProductCreateView(PermissionRequiredMixin, CreateView):#Zapretili sozdanie producta
    model = Product
    permission_required = 'catalog.create_Product'
    #form_class = SubjectForm
    form_class = ProductForm
    # fields = ('product_name', 'product_description', 'preview', 'price_per_unit', 'category')
    success_url = reverse_lazy('catalog:Product_list')
    template_name = 'catalog/product_withsubject.html'
# def select_from_cache_or_get_from_db():######Keshiruem
#     queryset = Product.objects.all()
#     if settings.CACHE_ENABLED:
#         cache_key = 'all_products'


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:Product_list')
    template_name = 'catalog/product_form.html'

    # def clean(self):
    #     t = ['казинo', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
    #     if request.method == 'POST':
    #         form = ProductForm(request.POST, request.FILES)
    #         for i in t:
    #             if Product.product_name == i:
    #                 raise ValueError('Nedopustimie slova')
    #         if not form.is_valid():
    #
    #         else:
    #             return Product.product_name


class ProductDeleteView(UserPassesTestMixin, DeleteView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:Product_list')
    template_name = 'catalog/product_confirm_delete.html'

    def test_func(self):
        return self.request.user.is_superuser


class ProductDetailView(LoginRequiredMixin, DeleteView):
    model = Product
    # form_class = ProductForm
    success_url = reverse_lazy('catalog:Product_list')
    template_name = 'catalog/Product_detail.html'
    def _cache_subjects(self):#####Keshirovanie na nizkom urovne
        queryset = Subject.objects.filter(product_name_again=self.object)
        if settings.CACHE_ENABLED:
            key = f'product_name_again_subjects_{self.object.pk}'
            cache_data = cache.get(key)
            if cache_data is None:
                cache_data=queryset
                cache.set(key, cache_data)
            return cache_data
        return queryset
    def get_context_data(self, **kwargs):

        context_data = super().get_context_data(**kwargs)
        context_data['subjects']=Subject.objects.filter(product_name_again=self.object)#product_content
        return context_data

@login_required
def change_status(request, pk):
    if request.user.has_perm('catalog.set_published_status'):

    # product_item = Product.objects.filter(pk=pk).first()
    # if product_item:
    #     if ... is None:
        product_item = get_object_or_404(Product, pk=pk)
        if product_item.published_status == Product.STATUS_ACTIV:
            product_item.published_status = Product.STATUS_INACTIV
        else:
            product_item.published_status = Product.STATUS_ACTIV
        product_item.save()
        return redirect(reverse('catalog:Product_list'))

    raise HttpResponseBadRequest

# class ProductCreateFormMore():
#     def context_data(self, **kwargs):
#         context_data = super().get_context_data(**kwargs)
#         FormSet = inlineformset_factory(self.model, Product, form=ProductForm, extra=1)
#         if self.request.method == 'POST':
#             formset = FormSet(self.request.POST, instance=self.object)
#         else:
#             formset = FormSet(instance=self.object)
#         context_data['formset']=formset
#         return context_data


class RecordListView(LoginRequiredMixin, ListView):
    model = Record


class RecordCreateView(LoginRequiredMixin, CreateView):
    # Sozdaem zapis "Record form"
    model = Record
    fields = '__all__'
    # fields = ('title', 'content', 'id_public')
    success_url = reverse_lazy('catalog:Rec_list')


# def rec_lst_img(request):
#     if request.method=='POST' and request.FILES:
#         file=request.FILES['myfile1']
#         fs=FileSystemStorage()
#         filename=fs.save(file.name, file)
#         file_url = fs.url(filename)
#         return render(request, 'Rec_list.html', {
#             'file_url':file_url
#         })
class RecordUpdateView(LoginRequiredMixin, UpdateView):
    # Sozdaem zapis
    model = Record
    # fields = '__all__'
    fields = ('title', 'content', 'image', 'id_public')
    success_url = reverse_lazy('catalog:Rec_list')



class RecordDeleteView(LoginRequiredMixin, DeleteView):
    model = Record
    success_url = reverse_lazy('catalog:Rec_list')


class RecordDetailView(LoginRequiredMixin, DetailView):
    model = Record
    template_name = 'catalog/record_detail.html'

    # def get_object(self, queryset=None):
    #     object=super().get_object(queryset)
    #     object.view_controller += 1
    #     object.save()
    #     return object
# class SubjectCreateView(CreateView):#Zapretili sozdanie producta
#     model = Subject
#     # permission_required = 'catalog.create_Product'
#     #form_class = SubjectForm
#     # form_class = ProductForm
#     # fields = ('product_name', 'product_description', 'preview', 'price_per_unit', 'category')
#     success_url = reverse_lazy('catalog:Product_list')
#     template_name = 'catalog/product_withsubject.html'