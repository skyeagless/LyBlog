# Generated by Django 2.0.2 on 2019-04-30 03:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20190430_1059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vieweddetail',
            name='blog',
            field=models.OneToOneField(default='', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='blog.Blog'),
        ),
    ]
