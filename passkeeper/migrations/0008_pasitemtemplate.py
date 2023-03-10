# Generated by Django 3.0.3 on 2023-03-10 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passkeeper', '0007_remove_appuser_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='PasItemTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password_id_temp', models.CharField(max_length=256)),
                ('username_temp', models.CharField(max_length=256)),
                ('password_temp', models.CharField(max_length=256)),
                ('url_temp', models.CharField(blank=True, max_length=256)),
                ('comment_temp', models.CharField(blank=True, max_length=256)),
            ],
        ),
    ]
