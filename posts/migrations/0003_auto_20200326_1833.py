# Generated by Django 3.0.4 on 2020-03-26 18:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_skill_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='point',
            new_name='points',
        ),
    ]