# Generated by Django 4.1 on 2022-09-11 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_alter_customer_customer_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='Roll_no',
            field=models.IntegerField(),
        ),
    ]