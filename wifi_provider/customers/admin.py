# customers/admin.py
from django.contrib import admin
from .models import Customer, Account

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'join_date', 'data_allocation', 'savings']
    search_fields = ['name']
    list_filter = ['join_date']

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['customer', 'date', 'data_used', 'buy_balance', 'continuous_number', 'extra_off']
    search_fields = ['customer__name', 'continuous_number']
    list_filter = ['date']