# Generated by Django 4.0.2 on 2022-05-21 03:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('winwall', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('image', models.URLField()),
                ('is_exported', models.BooleanField()),
                ('slug', models.SlugField()),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='winwall',
            name='collection_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='winwall.collection'),
            preserve_default=False,
        ),
    ]