from django.urls import path
from . import views

# from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('login/', auth_views.LoginView.as_view(template_name='students/login.html'), name='student-login'),
    path('login/', views.login, name='student-login'),
    path('logout/', views.logout, name='student-logout'),
    path('plan/', views.plan, name='student-plan'),
]
