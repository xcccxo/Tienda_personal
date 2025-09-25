from rest_framework import serializers
from .models import Product, Wishlist, CartItem, Category, Element

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = '__all__'

class WishlistSerializer(serializers.ModelSerializer):
    product_details = ElementSerializer(source='product', read_only=True)
    
    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'product', 'product_details']

class CartItemSerializer(serializers.ModelSerializer):
    product_details = ElementSerializer(source='product', read_only=True)
    
    class Meta:
        model = CartItem
        fields = ['id', 'user', 'product', 'product_details', 'quantity']
