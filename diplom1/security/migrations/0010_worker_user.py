# Generated by Django 4.1.2 on 2023-04-14 18:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('security', '0009_alter_error_id_clietn_alter_error_id_worker'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='user',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
