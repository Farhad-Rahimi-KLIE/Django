# customers/models.py
from django.db import models
from django.core.validators import MinValueValidator

class Customer(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    join_date = models.DateField()
    data_allocation = models.FloatField(validators=[MinValueValidator(0.0)])  # In GBs
    savings = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])

    class Meta:
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['join_date']),
        ]

    def __str__(self):
        return self.name

class Account(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='accounts')
    date = models.DateTimeField(db_index=True)
    data_used = models.FloatField(validators=[MinValueValidator(0.0)])  # In GBs
    buy_balance = models.FloatField(validators=[MinValueValidator(0.0)])
    bill_image = models.ImageField(upload_to='bills/', blank=True, null=True)
    continuous_number = models.CharField(max_length=50, unique=True)
    extra_off = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])  # Extra data discount in GBs

    class Meta:
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['continuous_number']),
        ]

    def __str__(self):
        return f"{self.customer.name} - {self.continuous_number}"