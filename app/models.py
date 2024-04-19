from autoslug import AutoSlugField
from django.conf import settings
from django.db import models
from django.urls import reverse


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='Пользователь')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата подписки')
    price = models.PositiveIntegerField(verbose_name='Сумма оплаты', default=0)
    payment_link = models.URLField(verbose_name='Ссылка на оплату', null=True, blank=True, max_length=400)
    payment_id = models.CharField(max_length=255, verbose_name='ID платежа', null=True, blank=True)
    paid_publication = models.ManyToManyField('Publication', verbose_name='Оплаченные публикации', blank=True)

    def __str__(self):
        return f'{self.user} - {self.date}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['-date']


class Publication(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Черновик'
        PUBLISHED = 'published', 'Опубликовано'

    class SubscriptionStatus(models.TextChoices):
        FREE = 'free', 'бесплатно'
        PAID = 'paid', 'платно'

    title = models.CharField(max_length=150, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание', blank=True, null=True, max_length=500)
    image = models.ImageField(upload_to='images/', verbose_name='Изображение', blank=True, null=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.CharField(choices=Status.choices, default=Status.DRAFT, verbose_name='Статус публикации')
    slug = AutoSlugField(populate_from='title', db_index=True, verbose_name='Slug', allow_unicode=True)
    is_paid = models.CharField(choices=SubscriptionStatus.choices, default=SubscriptionStatus.FREE,
                               verbose_name='Статус подписки')

    def get_absolute_url(self):
        return reverse('app:detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-time_create']
