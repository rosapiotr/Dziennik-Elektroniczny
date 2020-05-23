from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import UserLoginForm, ProfileUpdateForm, UserUpdateForm #, ChangePasswordForm
from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from django.contrib import messages

from django.forms import ValidationError
###
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView
from database.models import Ogloszenie, Nauczyciel, Przedmiot, Zajecia, Uczen, Ocena
from django.contrib.auth.forms import PasswordChangeForm

class AnnotationCreateView(LoginRequiredMixin, CreateView):
    model = Ogloszenie
    template_name = 'teachers/add_ann.html'
    fields = ['id_przedmiotu', 'tresc']

# class AnnotationDetailView(LoginRequiredMixin, DetailView):
#     model = Ogloszenie

###

def login(request):
    if request.user.is_authenticated:
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
    # id = request.user.id
    # nauczyciel = Nauczyciel.objects.filter(user_id=id).values()
    nauczyciel = request.user.nauczyciel
    id_n = nauczyciel.id
    # id_n = nauczyciel[0]['id']
    przedmioty = Przedmiot.objects.filter(id_nauczyciela=id_n)
    # przedmioty = Przedmiot.objects.filter(id_nauczyciela=id_n).values()
    # lista_przedmiotow = []
    # for p in przedmioty:
    #     # print(p['id'], p['nazwa'])
    #     lista_przedmiotow.append(str(p['nazwa']) + " " + str(p['id']))

    context = {
        'title': "Dodaj ogłoszenie",
        'przedmioty': przedmioty
    }
    return render(request, 'teachers/add_ann.html', context)

@login_required(login_url="/teachers/login")
def post_ann(request):
    # id = request.user.id
    # nauczyciel = Nauczyciel.objects.filter(user_id=id)[0]
    nauczyciel = request.user.nauczyciel
    id_nauczyciela = nauczyciel.id
    id_przedmiotu = request.POST.get("subject", "").split()[-1][1:-1]
    przedmiot = Przedmiot.objects.filter(id=id_przedmiotu)
    tresc = request.POST.get("content", "")
    o = Ogloszenie(id_nauczyciela=nauczyciel, id_przedmiotu=przedmiot[0], tresc=tresc)
    o.save()
    
    response = redirect('teacher-add-ann')
    messages.add_message(request, messages.SUCCESS, 'Dodano ogłoszenie')
    return response

@login_required(login_url="/teachers/login")
def add_grade(request):
    # id = request.user.id
    # nauczyciel = Nauczyciel.objects.filter(user_id=id)[0]
    nauczyciel = request.user.nauczyciel
    id_nauczyciela = nauczyciel.id

    przedmioty = Przedmiot.objects.filter(id_nauczyciela=nauczyciel)
    zajecia = Zajecia.objects.filter(id_przedmiotu__in=przedmioty)
    # zajecia = []
    # for p in przedmioty:
    #     zajecia.append(Zajecia.objects.filter(id_przedmiotu=p.id))
    klasy = []
    for z in zajecia:
        # for zz in z:
        klasy.append(z.id_klasy)
    uczniowie = Uczen.objects.filter(klasa__in=klasy)
    # uczniowie = []
    # for k in klasy:
    #     for kk in klasy:
    #         uczniowie.append(Uczen.objects.filter(klasa=kk.id))

    context = {
        'title': "Dodaj ocenę",
        'przedmioty': przedmioty,
        'uczniowie': uczniowie
    }

    return render(request, "teachers/add_grade.html", context)

@login_required(login_url="/teachers/login")
def post_grade(request):
    # id = request.user.id
    # nauczyciel = Nauczyciel.objects.filter(user_id=id)[0]
    nauczyciel = request.user.nauczyciel
    id_nauczyciela = nauczyciel.id
    id_przedmiotu = request.POST.get("subject", "").split()[-1][1:-1]
    przedmiot = Przedmiot.objects.filter(id=id_przedmiotu)[0]
    uczen = request.POST.get("student", "").split()
    id_ucznia = Uczen.objects.filter(imie=uczen[0], nazwisko=uczen[1])[0]
    ocena = int(request.POST.get("grade", ""))
    waga = int(request.POST.get("weight", ""))
    wynik = request.POST.get("description", "")

    response = redirect('teacher-add-grade')

    if Zajecia.objects.filter(id_klasy=id_ucznia.klasa, id_przedmiotu=przedmiot).exists():
        o = Ocena(id_ucznia=id_ucznia, id_przedmiotu=przedmiot, ocena=ocena, waga=waga, wynik=wynik)
        o.save()
        messages.add_message(request, messages.SUCCESS, 'Dodano ocenę')
    else:
        messages.add_message(request, messages.SUCCESS, 'BŁĄD. Uczeń {0} nie uczęszcza na ten przedmiot ({1})'.format(id_ucznia, przedmiot))    

    return response

@login_required(login_url="/teachers/login")
def plan(request):
    # id = request.user.id
    # nauczyciel = Nauczyciel.objects.filter(user_id=id)[0]
    nauczyciel = request.user.nauczyciel
    przedmioty = Przedmiot.objects.filter(id_nauczyciela=nauczyciel)
    zajecia = Zajecia.objects.filter(id_przedmiotu__in=przedmioty)
    print(zajecia)
    
    context = {
        'title': "Plan zajęć",
        'zajecia': zajecia
    }

    return render(request, "teachers/plan.html", context)

@login_required(login_url="/teachers/login")
def ogloszenia(request):
    nauczyciel = request.user.nauczyciel
    # id = request.user.id
    # nauczyciel = Nauczyciel.objects.filter(user_id=id)[0]
    ogloszenia = Ogloszenie.objects.filter(id_nauczyciela=nauczyciel)
    print(ogloszenia)
    
    context = {
        'title': "Moje ogłoszenia",
        'ogloszenia': ogloszenia
    }

    return render(request, "teachers/ann.html", context)

@login_required(login_url="/teachers/login")
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

@login_required(login_url="/teachers/login")
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
