from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, FormView, UpdateView
from requests import Response

from app.utils import send_sms
from users.forms import RegistrationForm, LoginForm, ProfileForm, SMSCodeForm


class UserRegisterView(CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy('users:verify')
    template_name = 'users/register.html'

    def form_valid(self, form):
        form.save(commit=False)
        phone_number = form.cleaned_data['phone_number']
        password = form.cleaned_data['password1']
        sent_code = send_sms(phone_number)
        self.request.session['sms_code'] = sent_code
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        self.request.session['pk'] = user.pk
        return redirect(self.success_url)


class UserVerifyView(FormView):
    form_class = SMSCodeForm
    template_name = 'users/verify.html'
    success_url = reverse_lazy('app:index')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            user = get_user_model().objects.get(pk=self.request.session['pk'])
            if code == self.request.session['sms_code']:
                user.is_active = True
                user.save()
                login(request, user)
                return redirect(self.success_url)

        return HttpResponse('Неправильный код', status=400)


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'
    fields = ('phone_number', 'password')

    def get_success_url(self):
        return reverse_lazy('app:index')


class UserProfileView(UpdateView):
    model = get_user_model()
    form_class = ProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('app:index')

    def get_object(self, queryset=None):
        return self.request.user


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('app:index')
