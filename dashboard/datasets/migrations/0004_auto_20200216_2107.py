# Generated by Django 3.0.3 on 2020-02-16 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0003_auto_20190620_2044'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='contributor',
            field=models.CharField(blank=True, max_length=2048),
        ),
        migrations.AddField(
            model_name='dataset',
            name='description',
            field=models.CharField(blank=True, max_length=2048),
        ),
        migrations.AddField(
            model_name='dataset',
            name='release_date',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='dataset',
            name='url',
            field=models.CharField(blank=True, max_length=1042),
        ),
        migrations.AddField(
            model_name='dataset',
            name='version',
            field=models.CharField(blank=True, max_length=16),
        ),
    ]
