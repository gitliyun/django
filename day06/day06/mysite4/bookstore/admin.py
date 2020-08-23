from django.contrib import admin
from .models import *
# Register your models here.

class BookAdmin(admin.ModelAdmin):

    list_display = ['id', 'title', 'price', 'market_price']
    list_display_links = ['title']
    list_filter = ['pub']
    search_fields = ['title', 'pub']
    list_editable = ['price', 'market_price']


admin.site.register(Book, BookAdmin)
admin.site.register(Author)
