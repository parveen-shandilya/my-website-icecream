# Generated by Django 3.0.5 on 2020-06-03 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0012_auto_20200603_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_updates',
            name='update_percentage',
            field=models.IntegerField(),
        ),
    ]
