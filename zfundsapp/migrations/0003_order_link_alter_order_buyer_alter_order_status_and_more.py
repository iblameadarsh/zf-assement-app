# Generated by Django 4.1 on 2023-10-09 13:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('zfundsapp', '0002_products_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='link',
            field=models.CharField(default='default', max_length=100, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='buyer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='buyer_agent', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('Complete', 'Complete'), ('Pending', 'Pending')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
