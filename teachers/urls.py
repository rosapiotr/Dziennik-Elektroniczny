from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='teacher-login'),
    path('logout/', views.logout, name='teacher-logout'),
    # path('dodaj_ogloszenie', views.AnnotationCreateView.as_view(), name='teacher-add-ann'),
    # path('ogloszenie/<int:id>', views.DetailView.as_view(), name='teacher-ann-detail'),
    path('dodaj_ogloszenie/', views.add_ann, name='teacher-add-ann'),
    path('zapisz_ogloszenie/', views.post_ann, name='teacher-post-ann'),
    path('dodaj_ocene/', views.add_grade, name='teacher-add-grade'),
    path('zapisz_ocene/', views.post_grade, name='teacher-post-grade'),
    path('plan/', views.plan, name='teacher-plan'),
    path('ogloszenia/', views.ogloszenia, name='teacher-ann'),
    path('profil/', views.profile, name='teacher-profile'),
    path('zmien_haslo/', views.change_password, name='teacher-change-pass'),
]
