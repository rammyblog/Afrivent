# Generated by Django 2.2.5 on 2019-10-01 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ref_code',
            field=models.CharField(default=False, max_length=250),
        ),
    ]
