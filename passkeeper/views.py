from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from .models import *
from .forms import *



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


def create_password(request, id):
    categories_list = Category.objects.all()
    category = Category.objects.get(pk=id)
    
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        passitems = PasItem.objects.filter(pass_category__exact=id)
        #validate the data
        if form.is_valid():
            password = PasItem()                        
            password.password_id = form.cleaned_data['password_id']    #title - how user decide to call it
            password.username = form.cleaned_data['username']          #username to store
            password.password = form.cleaned_data['password']          #password to store
            password.url = form.cleaned_data['url'] 
            #own = models.CharField(max_length=2, default="Me")
            password.comment = form.cleaned_data['comment'] 
            password.pass_category = category
            password.save()
                     
            
            return render(request, 'passkeeper/passwords_table.html',  {'categories_list': categories_list, 'category': category, 'passitems': passitems})
    else:    
        form = PasswordForm()    
        return render(request, 'passkeeper/create_password.html', {'form': form, 'categories_list': categories_list, 'category': category})
