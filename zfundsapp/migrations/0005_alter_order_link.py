# Generated by Django 4.1 on 2023-10-09 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zfundsapp', '0004_alter_order_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='link',
            field=models.CharField(default='20090928-a974-4b6f-9e9a-1b330a1bd4cb', max_length=100, unique=True),
        ),
    ]
