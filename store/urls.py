from django.urls import path
from rest_framework.routers import SimpleRouter,DefaultRouter
from rest_framework_nested import routers
from . import views

# Router

router = DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet, basename='cart')
router.register('customers', views.CustomerViewSet, basename='customer')
router.register('orders', views.OrderViewSet, basename='order')

# Nested router for cart items
carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', views.CartItemViewSet, basename='cart-items')

product_router= routers.NestedDefaultRouter(router, 'products',lookup='product')
product_router.register('reviews',views.ReviewViewSet,basename='product-reviews')


# URLConf
urlpatterns = router.urls + product_router.urls + carts_router.urls
