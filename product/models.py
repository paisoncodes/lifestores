from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=225)
    description = models.CharField(max_length=350)
    sku = models.CharField(max_length=225)
    price = models.PositiveBigIntegerField()
    image = models.URLField()

    def __str__(self):
        return self.name