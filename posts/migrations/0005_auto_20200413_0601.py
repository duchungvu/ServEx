# Generated by Django 3.0.4 on 2020-04-13 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20200409_0259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(default='Just another post', max_length=40),
        ),
    ]
