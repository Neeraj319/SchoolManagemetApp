# Generated by Django 3.1.1 on 2020-11-21 21:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_discussion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussion',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.subject'),
        ),
    ]
