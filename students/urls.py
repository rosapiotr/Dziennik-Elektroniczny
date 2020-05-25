from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='student-login'),
    path('logout/', views.logout, name='student-logout'),
    path('plan/', views.plan, name='student-plan'),
    path('ogloszenia/', views.ogloszenia, name='student-ann'),
    path('oceny/', views.oceny, name='student-grades'),
    path('przedmioty/', views.przedmioty, name='student-subjects'),
    path('przedmiot/<int:id>', views.przedmiot, name='student-subject-details'),
    path('profil', views.profile, name='student-profile'),
    path('zmien_haslo/', views.change_password, name='student-change-pass'),
    path('nauczyciele/', views.nauczyciele, name='student-teachers'),
    path('nauczyciel/<int:id>', views.nauczyciel, name='student-teacher-details'),
]
