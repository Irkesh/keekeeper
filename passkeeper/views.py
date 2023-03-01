from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from .models import *


def index(request):
    categories_list = Category.objects.all()
    category = Category.objects.get(pk=1)
    passitems = PasItem.objects.all().filter(pass_category__exact=1)
    return render(request, 'passkeeper/index.html',  {'categories_list': categories_list, 'category': category, 'passitems': passitems})


#pk - primary key for category
def category(request, pk):
    categories_list = Category.objects.all()
    category = Category.objects.get(pk=pk)
    passitems = PasItem.objects.filter(pass_category__exact=category.id)
    return render(request, 'passkeeper/passwords_table.html',  {'categories_list': categories_list, 'category': category, 'passitems': passitems})

#pk - primary key for password
#id - primary key for category
def delete(request, pk, id):
    categories_list = Category.objects.all()
    PasItem.objects.filter(pk=pk).delete()    
    passitems = PasItem.objects.filter(pass_category__exact=id)
    return render(request, 'passkeeper/passwords_table.html',  {'categories_list': categories_list, 'category': category, 'passitems': passitems})

#pk - primary key for password
#id - primary key for category
def edit(request, pk, id):
    categories_list = Category.objects.all()
    #we do nothing with edit for now
    category = Category.objects.get(pk=id)
    passitems = PasItem.objects.filter(pass_category__exact=id)
    return render(request, 'passkeeper/passwords_table.html',  {'categories_list': categories_list, 'category': category, 'passitems': passitems})