from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class RegistrationForm(UserCreationForm):
    phone_number = forms.CharField(label="Номер телефона", widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ('phone_number', 'password1', 'password2')
        labels = {'phone_number': 'Номер телефона', 'password1': 'Пароль', 'password2': 'Повторите пароль'}
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-input'}),
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if get_user_model().objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError('Такой пользователь уже существует')
        if not phone_number.startswith('+7'):
            raise forms.ValidationError('Номер должен начинаться с +7')
        if len(phone_number) != 12:
            raise forms.ValidationError('Номер должен содержать 11 цифр')
        return phone_number


class LoginForm(AuthenticationForm):
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ('phone_number', 'password')


class ProfileForm(forms.ModelForm):
    phone_number = forms.CharField(label="Номер телефона", widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model()
        fields = ('phone_number',)
        labels = {'phone_number': 'Номер телефона'}
        widgets = {'phone_number': forms.TextInput(attrs={'class': 'form-input'})}


class SMSCodeForm(forms.Form):
    code = forms.CharField(label="Код подтверждения", widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        verbose_name = "Код подтверждения"

    def clean_code(self):
        code = self.cleaned_data['code']
        if len(str(code)) != 6:
            raise forms.ValidationError('Код должен содержать 6 цифр')
        return code
