# Generated by Django 3.1.5 on 2021-03-03 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0021_auto_20210302_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='pincode',
            field=models.TextField(max_length=6, null=True),
        ),
    ]
