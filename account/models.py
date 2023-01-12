from django.db import models

# Create your models here.

ostatus = [
    ("accepted", "Accepted"),
    ("delivered", "Delivered"),
    ("canceled", "Canceled"),
    ("declined", "Declined"),
    ("returned", "Returned"),
]


class Clients(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    password = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'clients'


class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    order_no = models.CharField(max_length=10, default=None)
    cart_no = models.CharField(max_length=10)
    client = models.ForeignKey(Clients, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, null=True)
    mobile = models.CharField(max_length=30, null=False)
    address = models.CharField(max_length=255, null=False)
    cost = models.IntegerField()
    delivery_fees = models.IntegerField()
    total_cost = models.IntegerField()
    status = models.CharField(max_length=100, null=True, blank=True, choices=ostatus)
    created_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.mobile

    class Meta:
        db_table = 'orders'