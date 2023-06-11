from django.shortcuts import render, redirect
from .forms import UserInfoForm, UserForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserInfo

# Create your views here.
def index(request):    
    context = {}

    if request.user.is_authenticated:
        current_user_id = request.user.id
        user_basic_info = User.objects.get(id = current_user_id)
        user_more_info = UserInfo.objects.get(user__id = current_user_id)

        context = {
            'user_basic_info': user_basic_info,
            'user_more_info': user_more_info
        }

    return render(request, 'login_app/index.html', context)

def register(request):
    registered = False
    user_form = UserForm()
    user_info_form = UserInfoForm()

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        user_info_form = UserInfoForm(request.POST, request.FILES)

        if user_form.is_valid() and user_info_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            user_info = user_info_form.save(commit=False)
            user_info.user = user
            user_info.save()
            registered = True

    context = {
        'user_form' : user_form,
        'user_info_form' : user_info_form,
        'registered' : registered
    }

    return render(request, 'login_app/register.html', context)

def login_page(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:

            if user.is_active:
                login(request,user)
                return redirect('index')
            
            else:
                return HttpResponse('Account is not active')
            
        else:
            return HttpResponse('Login Details are wrong')
        
    else:
        return render(request, 'login_app/login.html')

@login_required

def user_logout(request):
    logout(request)
    return redirect('index')