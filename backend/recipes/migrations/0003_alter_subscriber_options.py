# Generated by Django 3.2.3 on 2024-02-04 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscriber',
            options={'ordering': ('author',)},
        ),
    ]