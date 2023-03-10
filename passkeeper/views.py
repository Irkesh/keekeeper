from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.hashers import make_password, check_password
from cryptography.fernet import Fernet
from passkeeper.models import AppUser
# Create your views here.
from .models import *
from .forms import *



def index(request):
    categories_list = Category.objects.all()
    category = Category.objects.get(pk=5)
    passitems = PasItem.objects.all().filter(pass_category__exact=1).reverse()
    return render(request, 'passkeeper/index.html',  {'categories_list': categories_list, 'category': category, 'passitems': passitems})



#pk - primary key for category
def category(request, pk):
    categories_list = Category.objects.all()
    category = Category.objects.get(pk=pk)
    passitems = PasItem.objects.filter(pass_category__exact=category.id).reverse()
    return render(request, 'passkeeper/passwords_table.html',  {'categories_list': categories_list, 'category': category, 'passitems': passitems})

#pk - primary key for password
#id - primary key for category
def delete(request, pk, id):
    categories_list = Category.objects.all()
    PasItem.objects.filter(pk=pk).delete()    
    passitems = PasItem.objects.filter(pass_category__exact=id).reverse()
    return render(request, 'passkeeper/passwords_table.html',  {'categories_list': categories_list, 'category': category, 'passitems': passitems})

#pk - primary key for password
#id - primary key for category
def edit(request, pk, id):
    categories_list = Category.objects.all()
    #we do nothing with edit for now
    category = Category.objects.get(pk=id)
    passitems = PasItem.objects.filter(pass_category__exact=id)
    return render(request, 'passkeeper/passwords_table.html',  {'categories_list': categories_list, 'category': category, 'passitems': passitems})


def create_password(request, id, user):
    categories_list = Category.objects.all()
    category = Category.objects.get(pk=id)
    
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        passitems = PasItem.objects.filter(pass_category__exact=id)
        # Retrieve a User object by username or other identifier
        user = AppUser.objects.get(user_id=user)
        # Access the email address of the user
        #user_email = user.email
        user_key = user.salt
        # Generate a salt for the password hash using the user's email address
        #salt = bytes(user_email, 'utf-8')
        #print(user_salt)
        #salt = '\xfb|\xe8\xe0\xe5\x9d\x11\xf5\xbc 8o\xbe<\xd9\x92'

        # Generate a secret key for encryption/decryption
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
            # Hash the password using PBKDF2 with 10000 iterations and a 256-bit key            
            #password.password = make_password(tmppass.encode('utf-8'), salt=salt, hasher='pbkdf2_sha256')
            #password.password = make_password(tmppass, salt=salt, hasher='pbkdf2_sha256')

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
                     
            
            return render(request, 'passkeeper/passwords_table.html',  {'categories_list': categories_list, 'category': category, 'passitems': passitems})
    else:    
        form = PasswordForm()    
        return render(request, 'passkeeper/create_password.html', {'form': form, 'categories_list': categories_list, 'category': category})



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
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'organisation' in user_form.cleaned_data:
                profile.organisation = request.DATA['organisation']
            
            profile.salt = Fernet.generate_key()
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    
    #if it is not POST - blank form for registration
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'passkeeper/register.html', { 'user_form': user_form, 'profile_form': profile_form, 'registered': registered})