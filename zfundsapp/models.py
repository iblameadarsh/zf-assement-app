from django.db import models
import uuid 
# Create your models here.

class Products(models.Model):

    CATEGORIES = (
        ('mutual_funds', 'Mutual Funds'),
        ('retirement_products', 'Retirement Products')
    )
    name = models.CharField(
        max_length=128
    )
    code = models.CharField(
        max_length=30,
        unique=True,
    )
    category = models.CharField(
        max_length=128,
        default=None,
        choices=CATEGORIES,
        blank=True,
        null=True
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        null=True
    )


    def __str__(self) -> str:
        return self.name
    

class Order(models.Model):

    user = models.ForeignKey(
        'authentication.User',
        on_delete=models.CASCADE,
        default=1
    )
    buyer = models.ForeignKey(
        'authentication.User',
        related_name='buyer_agent',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    products = models.ManyToManyField(
        Products,
        blank=True,
    )
    order_date = models.DateTimeField(
        auto_now_add=True
    )
    total_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2
    )
    STATUS_CHOICES = [
        ('Complete', 'Complete'),
        ('Pending', 'Pending'),
    ]
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES, 
        blank=True,
        null=True
    )
    link = models.CharField(max_length=100, unique=True, default=str(uuid.uuid4()))

    def __str__(self):
        return f"Order #{self.id}"


