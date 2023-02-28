from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from .models import *


def index(request):
    categories = Category.objects.all()
    passitems = PasItem.objects.all()
    return render(request, 'passkeeper/index.html',  {'categories': categories, 'passitems': passitems})


def category(request, pk):
    category = Category.objects.get(pk=pk)
    passitems = PasItem.objects.filter(pass_category__exact=category.id)
    return render(request, 'passkeeper/passwords_table.html',  {'category': category, 'passitems': passitems})


def delete(request, pk, id):
    PasItem.objects.filter(pk=pk).delete()    
    passitems = PasItem.objects.filter(pass_category__exact=id)
    return render(request, 'passkeeper/passwords_table.html',  {'category': category, 'passitems': passitems})

def edit(request):
    category = Category.objects.get(pk=pk)
    passitems = PasItem.objects.filter(pass_category__exact=category.id)
    return render(request, 'passkeeper/passwords_table.html',  {'category': category, 'passitems': passitems})