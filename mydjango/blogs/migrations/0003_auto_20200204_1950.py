# Generated by Django 2.2.9 on 2020-02-04 11:50

from django.db import migrations
import mdeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0002_auto_20200204_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content',
            field=mdeditor.fields.MDTextField(verbose_name='文章内容'),
        ),
    ]
