# Generated by Django 2.2.2 on 2019-06-27 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_auto_20190627_0855'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofileinfo',
            name='about',
            field=models.CharField(default='Hey there i am using felixora', max_length=124),
        ),
    ]
