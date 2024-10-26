from django.db import models 
from django.utils import timezone

class StockModel(models.Model):
    symbol = models.CharField(max_length=20)
    date = models.DateField()
    open_price = models.FloatField()
    close_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    volume = models.BigIntegerField()
    


class EMAStrategy(models.Model):
    short_window = models.PositiveIntegerField()
    long_window = models.PositiveIntegerField()
    stock_symbol = models.CharField(max_length=20)
    initial_investment = models.FloatField()



class PredictedPriceModel(models.Model):
    symbol = models.CharField(max_length=20) 
    date = models.DateField(default=timezone.now) 
    predicted_price = models.FloatField(default=0.0)
