from django.contrib import admin
from .models import Order, Item, Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['name', 'feedback_text', 'date_created', 'order']
    list_filter = ['date_created']
    search_fields = ['name', 'feedback_text']
    readonly_fields = ['date_created']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'total', 'date', 'region_code'
    ]
    list_filter = ['date', 'region_code']
    search_fields = ['user__username']

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'movie', 'price', 'quantity']
    list_filter = ['order__region_code', 'movie']
    search_fields = ['order__id', 'movie__name']