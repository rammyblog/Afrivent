# Generated by Django 2.2.5 on 2019-10-01 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0002_auto_20191001_0906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_confirmation',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='ref_code',
            field=models.CharField(max_length=250),
        ),
    ]
