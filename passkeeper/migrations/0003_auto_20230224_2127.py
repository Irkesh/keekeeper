# Generated by Django 3.0.3 on 2023-02-24 21:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('passkeeper', '0002_auto_20230224_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pasitem',
            name='pass_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='passkeeper.Category'),
        ),
    ]