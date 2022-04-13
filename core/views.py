from turtle import title
from django.shortcuts import redirect, render, HttpResponse
from core.models import Event

# Create your views here.


# Exercise
# def event(req, event_title):
#     event = Event.objects.get(title=event_title)
#     return HttpResponse('<h1>{}</h1>'.format(event))

# Demonstrative only
# def index(req):
#     return redirect('/diary/')

def list_events(req):
    user = req.user #Gets de authenticated user
    event = Event.objects.filter(user=user)
    res = {'events': event}
    return render(req, 'diary.html', res)