from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Uczen, Nauczyciel, CustomUser, Przedmiot, Klasa, Zajecia, Ogloszenie

# from django.forms import ModelForm

from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm



class UczenAdmin(admin.ModelAdmin):
    model = Uczen
    # fielsets = (None, {'fields': ('user', 'nazwa')},)
    list_display = ['imie', 'nazwisko', 'klasa_id']


class KlasaAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.id = "-".join([str(obj.rocznik), obj.nazwa])
        super().save_model(request, obj, form, change)

    fieldsets = (
        (None, {'fields': ('nazwa', 'rocznik', 'opis', 'id_wychowawcy')}),

    )
    model = Klasa
    list_display = ['nazwa', 'rocznik', 'id']
    list_filter = ['rocznik', 'nazwa']
    search_fields = ('nazwa',)
    ordering = ('nazwa',)

class PrzedmiotAdmin(admin.ModelAdmin):
    model = Przedmiot
    list_display = ['nazwa', 'id_nauczyciela', 'id']
    list_filter = ['nazwa', 'id_nauczyciela', 'id']
    # fieldsets = (
    #     (None, {'fields': ('nazwa', 'id_nauczyciela')}),
    # )
    search_fields = ('nazwa',)
    ordering = ('nazwa',)

    # add_form = PrzedmiotCreationForm
    # list_display = ['nazwa', 'id_nauczyciela']


######################
# class UserProfileForm(ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(UserProfileForm, self).__init__(*args, **kwargs)
#         # if self.instance.pk is None:
#         #     self.empty_permitted = False # Here

#     class Meta:
#         model = Nauczyciel


# class UserProfileInline(admin.TabularInline):         
#     model = UserProfile                               
#     form = UserProfileForm
########################
class CustomUserAdmin(UserAdmin):
    # add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'is_staff', 'is_active', 'is_teacher', 'is_student',)
    list_filter = ('username', 'is_staff', 'is_active', 'is_teacher', 'is_student',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active', 'is_student', 'is_teacher')}
        ),
    )
    search_fields = ('username',)
    ordering = ('username',)


admin.site.register(CustomUser, CustomUserAdmin)


# Register your models here.
admin.site.register(Zajecia)
admin.site.register(Przedmiot, PrzedmiotAdmin)
admin.site.register(Klasa, KlasaAdmin)

admin.site.unregister(Group)
admin.site.unregister(CustomUser)
admin.site.register(Uczen, UczenAdmin)
# admin.site.register(Uczen)
admin.site.register(Nauczyciel)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Ogloszenie)