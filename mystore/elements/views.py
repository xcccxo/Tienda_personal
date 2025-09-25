from django.shortcuts import render, get_object_or_404, redirect
from .models import Element, Category, Product, Wishlist, CartItem
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.decorators import login_required
from .serializers import ProductSerializer, WishlistSerializer, CartItemSerializer, CategorySerializer, ElementSerializer

# --------------------- VISTAS NORMALES ---------------------

def add_to_cart(request, product_id):
    product = get_object_or_404(Element, id=product_id)
    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product_id=product_id,
            defaults={'quantity': 1}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()
    else:
        cart = request.session.get('cart_items', [])
        if product_id not in cart:
            cart.append(product_id)
        request.session['cart_items'] = cart
    return redirect('elements:cart')

def add_to_wishlist(request, product_id):
    product = get_object_or_404(Element, id=product_id)
    if request.user.is_authenticated:
        wishlist_item, created = Wishlist.objects.get_or_create(
            user=request.user,
            product_id=product_id
        )
    else:
        wishlist = request.session.get('wishlist_items', [])
        if product_id not in wishlist:
            wishlist.append(product_id)
        request.session['wishlist_items'] = wishlist
    return redirect('elements:wishlist')

def index(request):
    categories = Category.objects.all()
    categorized_elements = {category: Element.objects.filter(category=category) for category in categories}
    return render(request, 'elements/index.html', {
        'categories': categories,
        'categorized_elements': categorized_elements,
    })

def detail(request, pk):
    element = get_object_or_404(Element, id=pk)
    return render(request, 'elements/detail.html', {'element': element})

def by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    elements = Element.objects.filter(category=category)
    categories = Category.objects.all()
    return render(request, 'elements/by_category.html', {
        'category': category,
        'elements': elements,
        'categories': categories,
    })

def cart_page(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        product_ids = [item.product_id for item in cart_items]
    else:
        product_ids = request.session.get('cart_items', [])
        cart_items = None
    products = Element.objects.filter(id__in=product_ids)
    return render(request, 'elements/cart.html', {
        'cart_items': cart_items,
        'products': products
    })

def wishlist_page(request):
    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user)
        product_ids = [item.product_id for item in wishlist_items]
    else:
        product_ids = request.session.get('wishlist_items', [])
        wishlist_items = None
    products = Element.objects.filter(id__in=product_ids)
    return render(request, 'elements/wishlist.html', {
        'wishlist_items': wishlist_items,
        'products': products
    })

# --------------------- APIs ---------------------

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return []

class ProductAdminViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

class ElementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Element.objects.all()
    serializer_class = ElementSerializer

class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        product_id = self.request.data.get('product')
        if Wishlist.objects.filter(user=self.request.user, product_id=product_id).exists():
            return Response({'error': 'El producto ya está en tu wishlist'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['delete'])
    def remove_product(self, request):
        product_id = request.data.get('product_id')
        wishlist_item = get_object_or_404(Wishlist, user=request.user, product_id=product_id)
        wishlist_item.delete()
        return Response({'status': 'product removed from wishlist'})

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        product_id = self.request.data.get('product')
        quantity = self.request.data.get('quantity', 1)
        cart_item, created = CartItem.objects.get_or_create(
            user=self.request.user,
            product_id=product_id,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()

    @action(detail=True, methods=['post'])
    def update_quantity(self, request, pk=None):
        cart_item = self.get_object()
        quantity = request.data.get('quantity')
        if quantity and int(quantity) > 0:
            cart_item.quantity = int(quantity)
            cart_item.save()
            return Response({'status': 'quantity updated'})
        else:
            cart_item.delete()
            return Response({'status': 'item removed'})
