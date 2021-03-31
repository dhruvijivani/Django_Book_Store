from django.contrib import admin
from .models import book
from .models import Category,Cart,OrderItem,Order,Payment,BookReview
# Register your models here.

class AdminBook(admin.ModelAdmin):
        list_display=['name','author_name','desc', 'price', 'category','total stock','available quantity','img']
        list_display=['name','slug']
        

class AdminCategory(admin.ModelAdmin):
        list_display=['name']

class AdminCart(admin.ModelAdmin):
        list_display=['Book','quantity','user']

admin.site.register(book,AdminBook)
admin.site.register(Category,AdminCategory)
admin.site.register(Cart,AdminCart)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(BookReview)