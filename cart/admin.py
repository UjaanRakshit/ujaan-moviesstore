from django.contrib import admin
from .models import Order, Item, Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['name', 'feedback_text', 'date_created', 'order']
    list_filter = ['date_created']
    search_fields = ['name', 'feedback_text']
    readonly_fields = ['date_created']

admin.site.register(Order)
admin.site.register(Item)