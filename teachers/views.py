from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import UserLoginForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from django.contrib import messages

###
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView
from database.models import Ogloszenie

class AnnotationCreateView(LoginRequiredMixin, CreateView):
    model = Ogloszenie
    template_name = 'teachers/add_ann.html'
    fields = ['id_przedmiotu', 'tresc']

# class AnnotationDetailView(LoginRequiredMixin, DetailView):
#     model = Ogloszenie

###

def login(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login_user(request, user)

        if next:
            response = redirect(next)
        else:
            response = redirect('teacher-add-ann')
        # response.set_cookie('user-data', 1, 60*20) # 20 minutes expiry
        return response

    context = {
        'title': 'Zaloguj się',
        'form': form,
    }
    return render(request, "teachers/login.html", context)

def logout(request):
    logout_user(request)
    response = redirect('teacher-login')
    # response.delete_cookie('user-data')
    messages.add_message(request, messages.SUCCESS, 'Wylogowano!')
    return response

@login_required(login_url="/teachers/login")
def add_ann(request):
    context = {
        'title': "Dodaj ogłoszenie"
    }
    return render(request, 'teachers/add_ann.html', context)
