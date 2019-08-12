# Generated by Django 2.0.2 on 2019-04-24 12:59

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20190423_2128'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='viewed_num',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='blog',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
