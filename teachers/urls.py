from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='teacher-login'),
    path('logout/', views.logout, name='teacher-logout'),
    path('dodaj_ogloszenie', views.AnnotationCreateView.as_view(), name='teacher-add-ann'),
    # path('ogloszenie/<int:id>', views.DetailView.as_view(), name='teacher-ann-detail'),
    # path('dodaj_ogloszenie/', views.add_ann, name='teacher-add-ann'),
]
