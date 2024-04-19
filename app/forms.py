from django import forms
from django.contrib.auth import get_user_model
from djmoney.models.fields import MoneyField
from app.models import Publication, Subscription


class AddPublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ['title', 'description', 'image', 'is_published', 'is_paid']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Заголовок'}),
            'description': forms.Textarea(
                attrs={'cols': 50, 'rows': 5, 'class': 'form-input', 'placeholder': 'Описание'}),
            'image': forms.FileInput(attrs={'class': 'form-input'}),
            'is_published': forms.Select(attrs={'class': 'form-input'}),
        }


class SubscriptionForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=get_user_model().objects.all(), disabled=True, label='Пользователь')
    price = MoneyField(default_currency='RUB')

    class Meta:
        model = Subscription
        fields = ['user', 'price']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(SubscriptionForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['user'].initial = user
        self.fields['price'].default_currency = 'RUB'
        self.fields['price'].initial = '500'
        self.fields['price'].widget.attrs['readonly'] = 'readonly'

    def save(self, commit=True):
        user_phone = self.cleaned_data.get('phone_number')
        user, created = get_user_model().objects.get_or_create(phone_number=user_phone,
                                                               defaults={'phone_number': user_phone})
        self.instance.user = user
        return super().save(commit=commit)
