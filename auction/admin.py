from django.contrib import admin
from .models import Item, Bid, Question

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'starting_price', 'end_date', 'is_active')
    search_fields = ('title', 'description')
    list_filter = ('is_active', 'end_date')

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('item', 'bidder', 'amount', 'timestamp')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('item', 'author', 'question_text', 'reply_text')