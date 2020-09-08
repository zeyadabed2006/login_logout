from django.shortcuts import render

# Create your views here.
from basic_app.forms import UserForm,UserProfileInfoForm
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

def index(request):
    return render(request,'basic_app/index.html')

def register(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user =user_form.save()
            user.set_password(user.password) #set_ to hash password
            user.save()
            profile =profile_form.save(commit=False) #without commit to db 
            profile.user =user

            if 'profile_pic' in request.FILES:
                profile.profile_pic =request.FILES['profile_pic']
            profile.save()
            registered =True
        else:
            print(user_form.errors,profile_form.errors) 
    else:
        user_form =UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'basic_app/registration.html',
              {'user_form':user_form,
               'profile_form':profile_form,
               'registered':registered,
              }
            )  #form parameter at html

def user_login(request): #take care from overload import names
    print('request.method ',request.method)
    if request.method =='POST': #user fill info
        username = request.Post.get('username') #as the name at html
        password = request.Post.get('password') #as the name at html
        user=authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Account not Active")
        else:
            print("Someone tried to login and failed!")#print to console
            print("username:",username,"and password:",password)
            return HttpResponse("invalid login details supplied!")
    else:        
        return render(request,'basic_app/login.html',{})

@login_required   #decorate to insure user login
def user_logout(request): 
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required   #decorate to insure user login
def special(request): 
    return HttpResponse("You are logged in, Nice!")
