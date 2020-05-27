from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from django.contrib import messages
from django.db.models import Q

from .forms import UserLoginForm, UserUpdateForm
from database.models import Zajecia, Przedmiot, Uczen, Ogloszenie, Ocena, Nauczyciel

def student_required(function):
    def wrapper(request, *args, **kwargs):
        decorated_view_func = login_required(request)
        if not decorated_view_func.user.is_authenticated:
            return redirect('student-login')
        try:
            uczen = request.user.uczen
            return function(request, *args, **kwargs)
        except:
            logout_user(request)
            messages.add_message(request, messages.SUCCESS, 'Nie masz dostępu do tej części serwisu')
            return redirect('student-login')

    wrapper.__doc__ = function.__doc__
    wrapper.__name__ = function.__name__
    return wrapper

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

# @login_required(login_url="/students/login")
@student_required
def plan(request):
    uczen = request.user.uczen
    klasa = uczen.klasa

    zajecia = Zajecia.objects.filter(id_klasy=klasa).order_by('godzina')

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
    return render(request, 'students/plan.html', context)

@student_required
def ogloszenia(request):
    uczen = request.user.uczen
    klasa = uczen.klasa

    zajecia = Zajecia.objects.filter(id_klasy=klasa).order_by('godzina')
    przedmioty = []
    for z in zajecia:
        przedmioty.append(z.id_przedmiotu)
        
    ogloszenia = Ogloszenie.objects.filter(id_przedmiotu__in=przedmioty).order_by('id')

    context = {
        "title": "Ogłoszenia",
        "ogloszenia": ogloszenia[::-1]
    }
    return render(request, 'students/ann.html', context)

@student_required
def oceny(request):
    uczen = request.user.uczen
    oceny = Ocena.objects.filter(id_ucznia=uczen)

    context = {
        "title": "Oceny",
        "oceny": oceny[::-1]
    }
    return render(request, 'students/grades.html', context)

@student_required
def przedmioty(request):
    uczen = request.user.uczen

    zajecia = Zajecia.objects.filter(id_klasy=uczen.klasa).order_by('godzina')
    przedmioty = []
    for z in zajecia:
        if z.id_przedmiotu not in przedmioty:
            przedmioty.append(z.id_przedmiotu)

    context = {
        "title": "Lista przedmiotów",
        "przedmioty":przedmioty
    }
    return render(request, 'students/subjects.html', context)

@student_required
def przedmiot(request, id):
    uczen = request.user.uczen

    przedmiot = Przedmiot.objects.filter(id=id).first()
    oceny = Ocena.objects.filter(id_ucznia=uczen, id_przedmiotu=przedmiot)

    srednia = 0
    wagi = 0
    for ocena in oceny:
        srednia += float(ocena.ocena) * ocena.waga
        wagi += ocena.waga
    try:
        srednia /= wagi
    except ZeroDivisionError:
        srednia = 0.00

    context = {
        "title": przedmiot.nazwa,
        "przedmiot": przedmiot,
        "oceny": oceny[::-1],
        "srednia": round(srednia, 2)
    }
    return render(request, 'students/subject.html', context)

@student_required
def profile(request):
    user = request.user
    uczen = request.user.uczen

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user)
        
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Pomyślnie zaktualizowano profil!')
            return redirect('student-profile')

    u_form = UserUpdateForm(instance=user)
    
    context = {
        'title': "Profil",
        'u_form': u_form
    }

    return render(request, "students/profile.html", context)

@student_required
def change_password(request):
    user = request.user

    if request.method == 'POST':
        password_form = PasswordChangeForm(data=request.POST, user=user)
        
        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            messages.success(request, f'Pomyślnie zmieniono hasło!')
            return redirect('student-profile')
        else:
            messages.success(request, f'Podano złe hasło, lub hasła nie są identyczne')
    
    password_form = PasswordChangeForm(user=user)

    context = {
        'title': "Zmień hasło",
        'password_form': password_form,
    }

    return render(request, "students/change_password.html", context)

@student_required
def nauczyciele(request):
    nauczyciele = []
    if request.method == 'POST':
        naucz = request.POST.get("nauczyciel").split()
        if len(naucz) < 1:
            naucz = [1, 1]
        elif len(naucz) < 2:
            naucz.append(1)

        nauczyciele = Nauczyciel.objects.filter(Q(imie__contains=naucz[0]) | Q(imie__contains=naucz[1]) | 
            Q(nazwisko__contains=naucz[0]) | Q(nazwisko__contains=naucz[1]))

    context = {
        "title": "Szukaj nauczyciela",
        "nauczyciele": nauczyciele
    }
    return render(request, 'students/teachers.html', context)

@student_required
def nauczyciel(request, id):
    nauczyciel = Nauczyciel.objects.get(id=id)
    # przedmiot = Przedmiot.objects.filter(id=id).first()
    przedmioty = Przedmiot.objects.filter(id_nauczyciela=nauczyciel)

    context = {
        "title": nauczyciel.imie + " " + nauczyciel.nazwisko,
        "przedmioty": przedmioty,
        "nauczyciel": nauczyciel
        }
    return render(request, 'students/teacher.html', context)