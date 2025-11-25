from django.contrib import admin
from .models import Account, Transaction

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance') # will show the key fields in admin list view
    search_fields = ('user__username',) # to search by username

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('account', 'transaction_type', 'amount', 'timestamp')
    list_filter = ('transaction_type', 'timestamp')  # add filters for type and date
    search_fields = ('account__user__username',)
