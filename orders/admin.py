from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Order, OrderHistory, Place

# Register your models here.

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'car', 'from_place', 'status', 'price', 'is_active', 'date', 'image', 'description')
    list_filter = ('status', 'car', 'from_place', 'to_place', 'is_active', )
    search_fields = ('user', 'car', 'from_place', 'to_place', 'price', 'description', )
    ordering = ('-id',)

    class Meta:
        model = Order
    
@admin.register(OrderHistory)
class OrderHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'user', 'from_place', 'to_place', 'price')
    list_filter = ('status', 'from_place', 'to_place')
    search_fields = ('user', 'from_place', 'to_place', 'price', )
    ordering = ('-id',)

    class Meta:
        model = OrderHistory


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'region', 'city')
    list_filter = ('region',)
    search_fields = ('region', 'city',)
    ordering = ('-id',)

    class Meta:
        model = Place