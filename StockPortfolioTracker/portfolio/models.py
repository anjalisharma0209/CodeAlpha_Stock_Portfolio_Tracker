from django.db import models

class Stock(models.Model):
    ticker = models.CharField(max_length=10, unique=True)
    quantity = models.PositiveIntegerField(default=1)
    purchase_price = models.FloatField()
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.ticker
