from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    context = {
        "title": "Dziennik Elektroniczny"
    }
    return render(request, 'database/home.html', context)
