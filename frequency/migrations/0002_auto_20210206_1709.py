# Generated by Django 3.1.6 on 2021-02-06 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frequency', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url',
            name='frequency_list',
            field=models.TextField(null=True),
        ),
    ]
