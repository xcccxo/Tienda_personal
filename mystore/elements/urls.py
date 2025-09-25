from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = "elements"

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'admin/products', views.ProductAdminViewSet, basename='admin-product')
router.register(r'elements', views.ElementViewSet, basename='element')
router.register(r'wishlist', views.WishlistViewSet, basename='wishlist')
router.register(r'cart', views.CartViewSet, basename='cart')

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/', views.detail, name='detail'),
    path('category/<slug:slug>/', views.by_category, name='by_category'),
    path('wishlist/', views.wishlist_page, name='wishlist'),
    path('cart/', views.cart_page, name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('add-to-wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('api/', include(router.urls)),
]
