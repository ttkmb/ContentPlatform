from django.db import models


class Publication(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Черновик'
        PUBLISHED = 'published', 'Опубликовано'

    title = models.CharField(max_length=150, verbose_name='Заголовок')
    description = models.TextField(verbose_name='Описание', blank=True, null=True, max_length=500)
    image = models.ImageField(upload_to='images/', verbose_name='Изображение', blank=True, null=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.CharField(choices=Status.choices, default=Status.DRAFT, verbose_name='Статус публикации')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-time_create']
