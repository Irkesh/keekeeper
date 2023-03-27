from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password, check_password
from cryptography.fernet import Fernet
from passkeeper.models import AppUser
from django.http import JsonResponse
from bootstrap_modal_forms.forms import *
# Create your views here.
from .models import *
from .forms import *






def index(request):
    if request.user.is_authenticated:
        # User is authenticated, so do something for authenticated users
        user = request.user.id
        categories_list = Category.objects.filter(user_id__exact=user).reverse()
        category = categories_list[0]
        passitems = PasItem.objects.all().filter(pass_category__exact=category.id).reverse()
        return render(request, 'passkeeper/index.html',  {'categories_list': categories_list, 'category': category, 'passitems': passitems})
    else:
        # User is not authenticated, so do something for anonymous users
        context = {}
        return render(request, 'passkeeper/login.html', context)

def getuserpassword(request):
    content = {"content": "This is user's password."}
    return render(request, 'passkeeper/passwords_table.html', content)


#pk - primary key for category
def category(request, pk):
    user = request.user.id       
    categories_list = Category.objects.filter(user_id__exact=user).reverse()
    category = Category.objects.get(pk=pk)
    passitems = PasItem.objects.all().filter(pass_category__exact=category.id).reverse()
    return render(request, 'passkeeper/passwords_table.html',  {'categories_list': categories_list, 'category': category, 'passitems': passitems})

#pk - primary key for password
#id - primary key for category
def delete_password(request, pk, id):
    user = request.user.id       
    categories_list = Category.objects.filter(user_id__exact=user).reverse()
    PasItem.objects.filter(pk=pk).delete()    
    passitems = PasItem.objects.filter(pass_category__exact=id).reverse()
    return render(request, 'passkeeper/passwords_table.html',  {'categories_list': categories_list, 'category': category, 'passitems': passitems})

#pk - primary key for password
#id - primary key for category
def edit_password(request, pk, id):
    user = request.user.id       
    categories_list = Category.objects.filter(user_id__exact=user).reverse()
    #we do nothing with edit for now
    category = Category.objects.get(pk=id)
    passitems = PasItem.objects.filter(pass_category__exact=id)
    return render(request, 'passkeeper/passwords_table.html',  {'categories_list': categories_list, 'category': category, 'passitems': passitems})

#pk - primary key for password
#id - primary key for category
def edit_password_item(request, pk, id):
    user = request.user.id       
    categories_list = Category.objects.filter(user_id__exact=user).reverse()
    category = Category.objects.get(pk=id)    
    if request.method == 'POST':
        form = PasswordForm(request.POST)        
        passitems = PasItem.objects.filter(pass_category__exact=id)

        form = PasswordForm()    
    return render(request, 'passkeeper/create_password.html', {'form': form, 'categories_list': categories_list, 'category': category})



#here id - is a Category pk
def create_password(request, id, user):
    user = request.user.id       
    categories_list = Category.objects.filter(user_id__exact=user).reverse()
    category = Category.objects.get(pk=id)    
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        passitems = PasItem.objects.filter(pass_category__exact=id)
        # Retrieve a User object by username or other identifier
        user = AppUser.objects.get(user_id=user)
        user_key = user.salt
        #key = Fernet.generate_key()
        print("Key: ")
        print(user_key)
        # Create a Fernet instance with the secret key
        #cipher_suite = Fernet(key)
        cipher_suite = Fernet(user_key)
        print("Cipher_suite: ")
        print(cipher_suite)
        
        #validate the data
        if form.is_valid():
            password = PasItem()                        
            password.password_id = form.cleaned_data['password_id']    #title - how user decide to call it
            password.username = form.cleaned_data['username']          #username to store

            tmppass=form.cleaned_data['password']                      #password to store
            encoded_password = cipher_suite.encrypt(tmppass.encode()).decode()
            print("Encoded password: "+ encoded_password)
            password.password = encoded_password
            password.url = form.cleaned_data['url'] 
            #own = models.CharField(max_length=2, default="Me")
            password.comment = form.cleaned_data['comment'] 
            password.pass_category = category
            password.save()
            decoded_password = cipher_suite.decrypt(encoded_password.encode()).decode()
            print("Decoded password: "+ decoded_password)
                     
            return HttpResponseRedirect('/')
            #return render(request, 'passkeeper/passwords_table.html',  {'categories_list': categories_list, 'category': category, 'passitems': passitems})
    else:    
        form = PasswordForm()    
        return render(request, 'passkeeper/create_password.html', {'form': form, 'categories_list': categories_list, 'category': category})

#create new category
def create_category(request, user):
    user = request.user.id       
    categories_list = Category.objects.filter(user_id__exact=user).reverse()
    #creating a form
    form = CategoryForm()
    cat_user = User.objects.get(pk=user)
    if request.method == 'POST':
        #extracting hidden value
        user = request.POST.get('user')
        form = CategoryForm(request.POST)
        if form.is_valid():
            new_category = Category()                        
            new_category.itemcategory = form.cleaned_data['itemcategory']    #title - how user decide to call it
            new_category.user = cat_user  
            new_category.save()
            return HttpResponseRedirect('/')
    return render(request, 'passkeeper/create_category.html', {'form': form})

def get_user_password(request, enc_password_id, userID):
    enc_password = PasItem.objects.get(pk=enc_password_id).password
    user = AppUser.objects.get(user_id=userID)
    user_key = user.salt
    cipher_suite = Fernet(user_key)
    decoded_password = cipher_suite.decrypt(enc_password.encode()).decode()
    #print("Decoded password: "+ decoded_password)
    data = {'password': decoded_password}
    return JsonResponse(data)


def create_new_password(request, id, user):
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


#/create_new_password/{{category.id}}



#if used loggin in - he will have a possiblity to log out
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('../')

#handling form that receives username and password
def user_login(request):
   
    #if getting HTTP POST - handle form, if not - return login form
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        #check that username and passwosrd are matching
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            return HttpResponse("Invalid login details supplied.")
    else:
        #categories_list = Category.objects.all()
        #category = Category.objects.get(pk=5)
        #passitems = PasItem.objects.all().filter(pass_category__exact=5)
        #return render(request, 'passkeeper/login.html',  {'categories_list': categories_list, 'category': category, 'passitems': passitems})
        return render(request, 'passkeeper/login.html') 
        #return render(request, 'passkeeper/login.html', {'master_genes': master_genes})


def register(request):
    
    registered = False
    #user has sent us done registr data
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            # Save the user to the database
            user.save()
            # Get the user's primary key (pk)
            user_pk = user.pk
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'organisation' in user_form.cleaned_data:
                profile.organisation = request.DATA['organisation']      
            ##generating account encryption key         
            user_key = Fernet.generate_key()
            profile.salt = user_key
            ###here is the process on coping default example passwords from template tables 
            profile.save()      
            cipher_suite = Fernet(user_key)      
            passItemTemp_list = PasItemTemplate.objects.all()
            catTemp_list = CategoryTemplate.objects.all()
            #iterating through categories
            for i in range(len(catTemp_list)):
                category_item =Category()
                category_item.itemcategory = catTemp_list[i].itemcategory_temp
                category_item.user = user     
                category_item.save()   
            
            #extracting new category list
            catNew_list = Category.objects.filter(user_id__exact=user_pk)

            #user = AppUser.objects.get(user_id=user)
            #user_key = user.salt
            #iterating trough new password items
            for i in range(len(passItemTemp_list)):
                password_item = PasItem()
                password_item.password_id = passItemTemp_list[i].password_id_temp
                password_item.username = passItemTemp_list[i].username_temp
                #encoded_password = cipher_suite.encrypt(tmppass.encode()).decode()
                #print("Encoded password: "+ encoded_password)
                passkey = passItemTemp_list[i].password_temp
                password_item.password = cipher_suite.encrypt(passkey.encode()).decode()
                #password_item.password = passItemTemp_list[i].password_temp
                password_item.url = passItemTemp_list[i].url_temp
                password_item.comment = passItemTemp_list[i].comment_temp
                password_item.pass_category = catNew_list[i]     
                password_item.save()        
            

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    
    #if it is not POST - blank form for registration
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'passkeeper/register.html', { 'user_form': user_form, 'profile_form': profile_form, 'registered': registered})