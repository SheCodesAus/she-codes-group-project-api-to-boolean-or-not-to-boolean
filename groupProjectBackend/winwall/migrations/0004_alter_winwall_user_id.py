# Generated by Django 4.0.2 on 2022-05-19 13:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('winwall', '0003_alter_stickynote_owner_alter_stickynote_win_wall'),
    ]

    operations = [
        migrations.AlterField(
            model_name='winwall',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_win_walls', to=settings.AUTH_USER_MODEL),
        ),
    ]
