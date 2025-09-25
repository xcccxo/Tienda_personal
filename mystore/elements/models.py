from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Type(models.Model):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Element(models.Model):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    description = models.TextField()
    content = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    type = models.ForeignKey('Type', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=50)
    image = models.ImageField(upload_to='products/')
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Element, on_delete=models.CASCADE)  # Cambiado de Product a Element

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Element, on_delete=models.CASCADE)  # Cambiado de Product a Element
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.product.title} x {self.quantity}"