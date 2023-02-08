from django.contrib import admin
from pay_right_here.accountbook.models import AccountBook, AccountBookHistory


@admin.register(AccountBook)
class AccountBookAdmin(admin.ModelAdmin):
    pass


@admin.register(AccountBookHistory)
class AccountBookHistoryAdmin(admin.ModelAdmin):
    pass
