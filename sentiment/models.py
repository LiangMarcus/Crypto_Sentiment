from django.db import models

# Create your models here.
class CryptoData(models.Model):
    crypto = models.CharField(max_length= 100)
    sentiment_score =models.IntegerField()
    price = models.IntegerField()
    class Meta:
        verbose_name_plural = "Cryptocurrency Data"
    def __str__(self):
        return f'{self.crypto}-{self.price}--{self.sentiment_score}'
    