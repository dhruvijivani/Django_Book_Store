# Generated by Django 3.1.5 on 2021-02-27 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_bookreview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookreview',
            name='stars',
            field=models.FloatField(default=1),
        ),
    ]
