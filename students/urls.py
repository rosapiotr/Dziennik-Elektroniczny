from django.urls import path
from . import views

# from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('login/', auth_views.LoginView.as_view(template_name='students/login.html'), name='student-login'),
    path('login/', views.login, name='student-login'),
    path('logout/', views.logout, name='student-logout'),
    path('plan/', views.plan, name='student-plan'),
    path('ogloszenia/', views.ogloszenia, name='student-ann'),
    path('oceny/', views.oceny, name='student-grades'),
    path('przedmioty/', views.przedmioty, name='student-subjects'),
    path('przedmiot/<int:id>', views.przedmiot, name='student-subject-details'),
]
