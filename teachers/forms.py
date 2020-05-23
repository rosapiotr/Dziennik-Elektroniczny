#####
from django import forms
from django.contrib.auth import authenticate

from database.models import Nauczyciel, CustomUser

class UserLoginForm(forms.Form):
    username = forms.CharField(label='Nazwa użytkownika')
    password = forms.CharField(widget=forms.PasswordInput, label='Hasło')

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user or not user.check_password(password):
                raise forms.ValidationError('Błędna nazwa użytkownika lub hasło')
            if not user.is_active:
                raise forms.ValidationError('Użytkownik nie jest aktywny')
        return super(UserLoginForm, self).clean(*args, **kwargs)

#####

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Nauczyciel
        fields = ['numer_telefonu']

# class ChangePasswordForm(forms.ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = ['password']

# class ChangePasswordForm(forms.Form):
#     old_password = forms.CharField(widget=forms.PasswordInput, label='Stare hasło')
#     new_password = forms.CharField(widget=forms.PasswordInput, label='Nowe hasło')
#     reenter_password = forms.CharField(widget=forms.PasswordInput, label='Powtórz hasło')
#     def clean(self):
#         new_password=self.cleaned_data.get('new_password')
#         reenter_password=self.cleaned_data.get('reenter_password')
        
#         if new_password and new_password!=reenter_password:
#             raise forms.ValidationError('Hasła nie są takie same')
            
#         return self.cleaned_data