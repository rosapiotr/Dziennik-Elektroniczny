from django.shortcuts import render, redirect
from django.http import HttpResponse
from database.models import Zajecia, Przedmiot, Uczen

####
from .forms import UserLoginForm
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user
from django.contrib import messages

def login(request):
    if request.user.is_authenticated:
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
            response.set_cookie('user-data', 1, 60*20) # 20 minutes expiry
            return response

        response = redirect('student-plan')
        response.set_cookie('user-data', 1, 60*20) # 20 minutes expiry
        return response
    context = {
        'title': 'Zaloguj się',
        'form': form,
    }
    return render(request, "students/login.html", context)
        # if next:
        #     return redirect(next)
        # return redirect('/')

def logout(request):
    logout_user(request)
    response = redirect('student-login')
    response.delete_cookie('user-data')
    messages.add_message(request, messages.SUCCESS, 'Wylogowano!')
    return response
    # context = {}
    # request.delete_cookie('sessionid')
    # request.delete_cookie('user-data')
    return render(request, 'students/login.html', context)

####
# from django.contrib.auth import views as auth_views

# def login(request):
#     context = {
#         "title": "Zaloguj się"
#     }
#     if request.method == 'POST' and request.user.is_authenticated:
#         response = render(request, 'students/plan.html', context)
#         response.set_cookie('wp_user_logged_in', 1, 60*20) # 20 minutes expiry
#         return response

#     defaults = {
#             'redirect_field_name': 'students/oceny.html',
#             'template_name': 'students/login.html',
#         }
#     response = auth_views.LoginView.as_view(**defaults)(request)  #login(request, **kwargs)
#     return response 
    # return render(request, 'students/login.html', context)

####
from django.contrib.auth.decorators import login_required
####

@login_required(login_url="/students/login")
def plan(request):
    if request.user.is_authenticated:
        id = request.user.id
    uczen = Uczen.objects.filter(user_id=id).values()
    klasa = uczen[0]['klasa_id']
    # klasa = uczen[0].keys()
    # print(klasa)

    zajecia = Zajecia.objects.filter(id_klasy=klasa).order_by('godzina')

    context = {
        "title": "Plan zajęć",
        "zajecia": zajecia
    }
    return render(request, 'students/plan.html', context)
