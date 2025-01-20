from decimal import Decimal
from typing import Union
from django.contrib.auth import  get_user_model
from django.db import transaction

from .signals import order_created

User= get_user_model()

from rest_framework import serializers
from .models import Product, Collection, Review, Cart, CartItem, Customer, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    price_with_tax = serializers.SerializerMethodField(method_name='get_price_with_tax')

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'inventory', 'collection', 'price_with_tax']

    def get_price_with_tax(self, product: Product) -> Decimal:
        tax_rate = Decimal(1.1)
        return product.unit_price * tax_rate

class CollectionSerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Collection
        fields = ['id', 'title','products_count']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'description', 'date']

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']

class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price= serializers.SerializerMethodField()

    def get_total_price(self, cart_item: CartItem) -> Decimal:
        return cart_item.product.unit_price * cart_item.quantity

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity','total_price']

class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True,read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart: Cart) -> int:
        return sum(item.product.unit_price * item.quantity for item in cart.items.all())

    class Meta:
        model = Cart
        fields = ['id','items','total_price']

class AddCartItemSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(min_value=1)
    product_id = serializers.IntegerField()

    def validate_product_id(self, product_id: int) -> int:
        if not Product.objects.filter(id=product_id).exists():
            raise serializers.ValidationError('Product not found')
        return product_id

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, product_id=product_id, quantity=quantity)
        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']

class UpdateCartItemSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(min_value=1)

    class Meta:
        model = CartItem
        fields = ['quantity']

class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone','birth_date','membership']

    def validate_user_id(self, user_id: int) -> int:
        try:
            User.objects.get(id=user_id)
            return user_id  # Return the ID itself, not the User object
        except User.DoesNotExist:
            raise serializers.ValidationError('User not found')

class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, order_item: OrderItem) -> Decimal:
        return order_item.product.unit_price * order_item.quantity

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'placed_at', 'payment_status', 'customer', 'items']


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(id=cart_id).exists():
            raise serializers.ValidationError('Cart not found')
        if not CartItem.objects.filter(cart_id=cart_id).exists():
            raise serializers.ValidationError('Cart is empty')
        return cart_id

    def save(self, **kwargs):
        with transaction.atomic():
            customer = Customer.objects.get(user_id=self.context['user_id'])
            order= Order.objects.create(customer=customer)
            cart_items= CartItem.objects.select_related('product').filter(cart_id=self.validated_data['cart_id'])
            order_items=[
                OrderItem(order=order, product=item.product, quantity=item.quantity, unit_price=item.product.unit_price)
                for item in cart_items
            ]
            OrderItem.objects.bulk_create(order_items)
            cart_items.delete()

            order_created.send_robust(sender=self.__class__, order=order)

            return order

class UpdateOrderSerializer(serializers.ModelSerializer ):
    class Meta:
        model = Order
        fields = ['payment_status']
