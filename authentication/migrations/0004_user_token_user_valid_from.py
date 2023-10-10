# Generated by Django 4.1 on 2023-10-09 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_alter_user_usergroup_alter_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='token',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='valid_from',
            field=models.DateTimeField(null=True),
        ),
    ]