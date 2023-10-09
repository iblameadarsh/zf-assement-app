from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserGroups(models.TextChoices):
    Advisor = 'Advisor'
    Customer = 'Customer'



class User(AbstractUser):

    GROUP_CHOICES = (
        ('Consumer', 'Consumer'),
        ('Advisor', 'Advisor'),
    )

    name = models.CharField(max_length=125)
    email = models.EmailField(
        max_length=125,
        unique=True, 
        null=True, 
        blank=True
        )
    password = models.CharField(max_length=125)
    username = models.CharField(
        max_length=128,
        unique=True,
        blank=True,
        null=True,
    )
    phone_number = models.CharField(
        null=True,
        blank=True, 
        unique=True,
        max_length=15
    )
    usergroup = models.CharField(
        max_length=56,
        choices=GROUP_CHOICES, 
        default='Consumer'
    )
    advisor = models.ForeignKey(
        'self', 
        null=True, 
        blank=True,
        default=None,
        on_delete=models.SET_NULL,
        related_name='clients'
    )
    token = models.CharField(
        max_length=128,
        blank=True,
        null=True
    )
    valid_from = models.DateTimeField(null=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["phone_number", "name"]

    def __str__(self):
        return '%s - %s' % (self.name, self.phone_number)

