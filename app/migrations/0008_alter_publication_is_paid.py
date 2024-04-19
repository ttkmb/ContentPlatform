# Generated by Django 5.0.3 on 2024-04-15 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_subscription_payment_id_subscription_payment_link_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='is_paid',
            field=models.CharField(choices=[('free', 'бесплатно'), ('paid', 'платно')], default='free', verbose_name='Статус подписки'),
        ),
    ]
