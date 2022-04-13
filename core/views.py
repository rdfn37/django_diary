from turtle import title
from django.shortcuts import redirect, render, HttpResponse
from core.models import Event
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.


# Exercise
# def event(req, event_title):
#     event = Event.objects.get(title=event_title)
#     return HttpResponse('<h1>{}</h1>'.format(event))

# Demonstrative only
# def index(req):
#     return redirect('/diary/')

def login_user(req):
    return render(req, 'login.html')

def logout_user(req):
    logout(req)
    return redirect('/')

def submit_login(req):
    if req.POST:
        username = req.POST.get('username')
        password = req.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(req, user)
            return redirect('/')
        else:
            messages.error(req, 'Username or password are invalid')

    return redirect('/')

@login_required(login_url='/login/')
def list_events(req):
    user = req.user #Gets de authenticated user
    event = Event.objects.filter(user=user)
    res = {'events': event}
    return render(req, 'diary.html', res)