from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')



# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.forms import UserCreationForm
# from .models import CustomUser

# class UserCreateForm(UserCreationForm):

#     class Meta:
#         model = User
#         fields = ('username', 'first_name' , 'last_name', )


# class UserAdmin(UserAdmin):
#     add_form = UserCreateForm
#     prepopulated_fields = {'username': ('first_name' , 'last_name', )}

#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('first_name', 'last_name', 'username', 'password1', 'password2', ),
#         }),
#     )


# # Re-register UserAdmin
# # admin.site.unregister(User)
# admin.site.register(CustomUser, UserAdmin)
