# Generated by Django 2.2.2 on 2019-06-21 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('annotations', '0004_auto_20190621_1635'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='annotationboundingbox',
            name='annotation',
        ),
        migrations.RemoveField(
            model_name='annotationsegmentation',
            name='annotation',
        ),
    ]
