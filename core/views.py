from turtle import title
from django.http import JsonResponse
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

@login_required(login_url='/login/')
def json_event_list(req):
    user = req.user #Gets de authenticated user
    event = Event.objects.filter(user=user).values('id', 'title')
    return JsonResponse(list(event), safe=False)

@login_required(login_url='/login/')
def event(req):
    event_id = req.GET.get('id')
    data = {}
    if event_id:
        data['event'] = Event.objects.get(id=event_id)
    return render(req, 'event.html', data)

@login_required(login_url='/login/')
def submit_event(req):
    if req.POST:
        title = req.POST.get('title')
        event_date = req.POST.get('event_date')
        description = req.POST.get('description')
        user = req.user
        event_id = req.POST.get('event_id')
        if event_id:
            event = Event.objects.get(id=event_id)
            if event.user == user:
                event.title = title
                event.event_date = event_date
                event.description = description
                event.save()
            # Event.objects.filter(id=event_id).update(
            #     title=title,
            #     event_date=event_date,
            #     description = description
            # )
        else:
            Event.objects.create(
                title=title,
                event_date=event_date,
                description=description,
                user=user
            )
    return redirect('/')

@login_required(login_url='/login/')
def event_delete(req, event_id):
    user = req.user
    event = Event.objects.get(id=event_id)
    if user == event.user:
        event.delete()
    return redirect('/')


