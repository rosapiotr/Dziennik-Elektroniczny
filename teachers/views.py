from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

from database.models import Ogloszenie, Nauczyciel, Przedmiot, Zajecia, Uczen, Ocena
from .forms import UserLoginForm, ProfileUpdateForm, UserUpdateForm
from datetime import date

def teacher_required(function):
    def wrapper(request, *args, **kwargs):
        decorated_view_func = login_required(request)
        if not decorated_view_func.user.is_authenticated:
            return redirect('teacher-login')
        try:
            teacher = request.user.nauczyciel
            return function(request, *args, **kwargs)
        except:
            logout_user(request)
            messages.add_message(request, messages.SUCCESS, 'Nie masz dostępu do tej części serwisu')
            return redirect('teacher-login')

    wrapper.__doc__ = function.__doc__
    wrapper.__name__ = function.__name__
    return wrapper

def check_if_teacher(request):
    try:
        request.user.nauczyciel
        return True
    except:
        return False

def login(request):
    if request.user.is_authenticated and check_if_teacher(request):
        return redirect('teacher-plan')

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
            response = redirect('teacher-plan')
        return response

    context = {
        'title': 'Zaloguj się',
        'form': form,
    }
    return render(request, "teachers/login.html", context)

def logout(request):
    logout_user(request)
    response = redirect('teacher-login')
    messages.add_message(request, messages.SUCCESS, 'Wylogowano!')
    return response

# @login_required(login_url="/teachers/login")
@teacher_required
def add_ann(request):
    nauczyciel = request.user.nauczyciel
    id_n = nauczyciel.id
    przedmioty = Przedmiot.objects.filter(id_nauczyciela=id_n)

    context = {
        'title': "Dodaj ogłoszenie",
        'przedmioty': przedmioty
    }
    return render(request, 'teachers/add_ann.html', context)

@teacher_required
def post_ann(request):
    nauczyciel = request.user.nauczyciel
    id_nauczyciela = nauczyciel.id
    id_przedmiotu = request.POST.get("subject", "").split()[-1][1:-1]
    przedmiot = Przedmiot.objects.filter(id=id_przedmiotu)
    tresc = "(" + str(date.today()) + ") " + request.POST.get("content", "")
    o = Ogloszenie(id_nauczyciela=nauczyciel, id_przedmiotu=przedmiot[0], tresc=tresc)
    o.save()
    
    response = redirect('teacher-add-ann')
    messages.add_message(request, messages.SUCCESS, 'Dodano ogłoszenie')
    return response

@teacher_required
def add_grade(request):
    nauczyciel = request.user.nauczyciel
    id_nauczyciela = nauczyciel.id

    przedmioty = Przedmiot.objects.filter(id_nauczyciela=nauczyciel)
    zajecia = Zajecia.objects.filter(id_przedmiotu__in=przedmioty)
    klasy = []
    for z in zajecia:
        klasy.append(z.id_klasy)
    uczniowie = Uczen.objects.filter(klasa__in=klasy)

    context = {
        'title': "Dodaj ocenę",
        'przedmioty': przedmioty,
        'uczniowie': uczniowie
    }

    return render(request, "teachers/add_grade.html", context)

@teacher_required
def post_grade(request):
    response = redirect('teacher-add-grade')
    if request.method == 'POST':
        nauczyciel = request.user.nauczyciel
        id_nauczyciela = nauczyciel.id
        id_przedmiotu = request.POST.get("subject", "").split()[-1][1:-1]
        przedmiot = Przedmiot.objects.filter(id=id_przedmiotu)[0]
        uczen = request.POST.get("student", "").split()
        id_ucznia = Uczen.objects.filter(imie=uczen[0], nazwisko=uczen[1])[0]
        ocena = int(request.POST.get("grade", ""))
        waga = int(request.POST.get("weight", ""))
        wynik = request.POST.get("description", "")

        if Zajecia.objects.filter(id_klasy=id_ucznia.klasa, id_przedmiotu=przedmiot).exists():
            o = Ocena(id_ucznia=id_ucznia, id_przedmiotu=przedmiot, ocena=ocena, waga=waga, wynik=wynik)
            o.save()
            messages.add_message(request, messages.SUCCESS, 'Dodano ocenę')
        else:
            messages.add_message(request, messages.SUCCESS, 'BŁĄD. Uczeń {0} nie uczęszcza na ten przedmiot ({1})'.format(id_ucznia, przedmiot))    

        return response
    return response

@teacher_required
def plan(request):
    nauczyciel = request.user.nauczyciel
    przedmioty = Przedmiot.objects.filter(id_nauczyciela=nauczyciel)
    zajecia = Zajecia.objects.filter(id_przedmiotu__in=przedmioty)
    # print(zajecia)

    plan = {"poniedziałek": zajecia.filter(dzien__contains="Pon"),
            "wtorek": zajecia.filter(dzien__contains="Wt"),
            "środa": zajecia.filter(dzien__contains="Śr"),
            "czwartek": zajecia.filter(dzien__contains="Cz"),
            "piątek": zajecia.filter(dzien__contains="Pi"),
            }
    
    plan2 = {"poniedziałek": [],
            "wtorek": [],
            "środa": [],
            "czwartek": [],
            "piątek": [],
            }

    for dzien in plan:
        godzina = 8
        for zajecia in plan[dzien]:
            while zajecia.godzina.hour > godzina:
                plan2[dzien].append("")
                godzina += 2
            plan2[dzien].append(zajecia)
            godzina += 2

    context = {
        "title": "Plan zajęć",
        "zajecia": plan2
    }
    
    return render(request, "teachers/plan.html", context)

@teacher_required
def ogloszenia(request):
    nauczyciel = request.user.nauczyciel
    # id = request.user.id
    # nauczyciel = Nauczyciel.objects.filter(user_id=id)[0]
    ogloszenia = Ogloszenie.objects.filter(id_nauczyciela=nauczyciel)
    print(ogloszenia)
    
    context = {
        'title': "Moje ogłoszenia",
        'ogloszenia': ogloszenia[::-1]
    }

    return render(request, "teachers/ann.html", context)

@teacher_required
def profile(request):
    # id = request.user.id
    # nauczyciel = Nauczyciel.objects.filter(user_id=id)[0]
    user = request.user
    nauczyciel = request.user.nauczyciel

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = ProfileUpdateForm(request.POST, instance=nauczyciel)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Pomyślnie zaktualizowano profil!')
            return redirect('teacher-profile')

    u_form = UserUpdateForm(instance=user)
    p_form = ProfileUpdateForm(instance=nauczyciel)
    
    context = {
        'title': "Profil",
        'p_form': p_form,
        'u_form': u_form
    }

    return render(request, "teachers/profile.html", context)

@teacher_required
def change_password(request):
    user = request.user
    nauczyciel = request.user.nauczyciel

    if request.method == 'POST':
        password_form = PasswordChangeForm(data=request.POST, user=user)
        
        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            messages.success(request, f'Pomyślnie zmieniono hasło!')
            return redirect('teacher-profile')
        else:
            messages.success(request, f'Podano złe hasło, lub hasła nie są identyczne')
    
    password_form = PasswordChangeForm(user=user)

    context = {
        'title': "Zmień hasło",
        'password_form': password_form,
    }

    return render(request, "teachers/change_password.html", context)
