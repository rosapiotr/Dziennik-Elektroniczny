from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "Administracja"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('database.urls')),
    path('students/', include('students.urls')),
    path('teachers/', include('teachers.urls')),
]
