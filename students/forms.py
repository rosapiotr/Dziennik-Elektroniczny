from django import forms
from django.contrib.auth import authenticate
from database.models import CustomUser

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

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email']