from django.shortcuts import render, redirect
from django.http import HttpResponse
from database.models import Zajecia, Przedmiot, Uczen, Ogloszenie, Ocena
from django.contrib.auth.decorators import login_required

####
from .forms import UserLoginForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from django.contrib import messages

# def student_required(function):
#     def wrapper(request, *args, **kwargs):
#         decorated_view_func = login_required(request)
#         if not decorated_view_func.user.is_authenticated:
#             return redirect('student-login')
#         try:
#             uczen = request.user.uczen
#             return function(request, *args, **kwargs)
#         except:
#             logout_user(request)
#             messages.add_message(request, messages.SUCCESS, 'Nie masz dostępu do tej części serwisu')
#             return redirect('student-login')

#     wrapper.__doc__ = function.__doc__
#     wrapper.__name__ = function.__name__
#     return wrapper

def check_if_student(request):
    try:
        request.user.uczen
        return True
    except:
        return False

def login(request):
    if request.user.is_authenticated and check_if_student(request):
        return redirect('student-plan')

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
            response = redirect('student-plan')
        return response

    context = {
        'title': 'Zaloguj się',
        'form': form,
    }
    return render(request, "students/login.html", context)

def logout(request):
    logout_user(request)
    # response = redirect('student-login')
    messages.add_message(request, messages.SUCCESS, 'Wylogowano!')
    # return response
    return redirect('student-login')

@login_required(login_url="/students/login")
def plan(request):
    uczen = request.user.uczen
    klasa = uczen.klasa

    zajecia = Zajecia.objects.filter(id_klasy=klasa).order_by('godzina')

    context = {
        "title": "Plan zajęć",
        "zajecia": zajecia
    }
    return render(request, 'students/plan.html', context)

@login_required(login_url="/students/login")
def ogloszenia(request):
    uczen = request.user.uczen
    klasa = uczen.klasa

    zajecia = Zajecia.objects.filter(id_klasy=klasa).order_by('godzina')
    przedmioty = []
    for z in zajecia:
        przedmioty.append(z.id_przedmiotu)
        
    ogloszenia = Ogloszenie.objects.filter(id_przedmiotu__in=przedmioty).order_by('id')

    context = {
        "title": "Plan zajęć",
        "ogloszenia": ogloszenia[::-1]
    }
    return render(request, 'students/ann.html', context)

@login_required(login_url="/students/login")
def oceny(request):
    uczen = request.user.uczen
    oceny = Ocena.objects.filter(id_ucznia=uczen)

    context = {
        "title": "Plan zajęć",
        "oceny": oceny[::-1]
    }
    return render(request, 'students/grades.html', context)

@login_required(login_url="/students/login")
def przedmioty(request):
    uczen = request.user.uczen

    zajecia = Zajecia.objects.filter(id_klasy=uczen.klasa).order_by('godzina')
    przedmioty = []
    for z in zajecia:
        przedmioty.append(z.id_przedmiotu)

    context = {
        "title": "Plan zajęć",
        "przedmioty":przedmioty
    }
    return render(request, 'students/subjects.html', context)

@login_required(login_url="/students/login")
def przedmiot(request, id):
    uczen = request.user.uczen

    przedmiot = Przedmiot.objects.filter(id=id).first()
    oceny = Ocena.objects.filter(id_ucznia=uczen, id_przedmiotu=przedmiot)

    context = {
        "title": "Plan zajęć",
        "przedmiot": przedmiot,
        "oceny": oceny[::-1]
    }
    return render(request, 'students/subject.html', context)