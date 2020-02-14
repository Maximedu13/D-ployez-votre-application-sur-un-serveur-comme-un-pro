"""Create your models here."""
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    """Category class"""
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class Product(models.Model):
    """Product class"""
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    nutriscore = models.CharField(max_length=1)
    stores = models.CharField(max_length=200, null=False)
    image = models.URLField(null=False, default='image')
    brand = models.CharField(max_length=200, null=False)
    calories = models.IntegerField(null=True)
    lipids = models.FloatField(null=True)
    sugars = models.FloatField(null=True)
    proteins = models.FloatField(null=True)
    salts = models.FloatField(null=True)
    url_off = models.URLField(null=False, unique=True)

    def __str__(self):
        return self.name

class Favorite(models.Model):
    """Favorite class"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
