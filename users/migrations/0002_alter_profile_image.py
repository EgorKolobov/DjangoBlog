# Generated by Django 4.0.4 on 2022-05-13 12:48

import Django_practice.yandex_s3_storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.FileField(storage=Django_practice.yandex_s3_storage.ClientDocsStorage(), upload_to=''),
        ),
    ]
