from django.db import models
from django.contrib.auth.models import User, auth
import datetime
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
      return self.name
    @staticmethod
    def get_all_categories():
        return Category.objects.all()

   
class book(models.Model):
    name = models.CharField(max_length=100)
    slug=models.CharField(max_length=200,null=True,unique=True,default="")
    author_name = models.CharField(max_length=100, default='')
    img = models.ImageField(upload_to='pics')
    desc = models.TextField()
    price = models.IntegerField()
    total_Stock=models.IntegerField(default=5)
    available_quantity=models.IntegerField(default=5)
    offer = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,default=1)

    def __str__(self):
      return self.name

    @staticmethod
    def get_all_books():
        return book.objects.all()
    @staticmethod
    def get_all_books_by_categoriesid(category_id):
        if category_id:
            return book.objects.filter(category=category_id)
        else:
            return book.get_all_books()    

    def get_rating(self):
        total=sum(int(review['stars']) for review in self.reviews.values())

        return int(total/ self.reviews.count())

class Cart(models.Model):
    Book=models.ForeignKey(book,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    # total=models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.name
    
class Order(models.Model):
    orderStatus =  (
        ('PENDING' , "Pending"), 
        ('PLACED' , "Placed"), 
        ('CANCELED' , "Canceled"), 
        ('COMPLETED' , "Completed"), 
    )
    method =  (

        ('ONLINE' , "Online"), 
    )
    order_status = models.CharField(max_length=15 , choices=orderStatus)
    payment_method = models.CharField(max_length=15 , choices=method)
    city=models.CharField(max_length=20,null=True)
    state=models.CharField(max_length=20,null=True)
    pincode=models.CharField(max_length=6,null=True)
    address = models.CharField(max_length=100  , null = False)
    phone = models.CharField(max_length=10 , null=False )
    user = models.ForeignKey(User , on_delete = models.CASCADE)
    total = models.IntegerField(null=False)
    date = models.DateTimeField(null= False , auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order , on_delete = models.CASCADE)
    Book=models.ForeignKey(book,on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False) 
    price = models.IntegerField(null=False) 
    date = models.DateTimeField(null= False , auto_now_add=True)
    

class Payment(models.Model):
    order = models.ForeignKey(Order , on_delete = models.CASCADE)
    date = models.DateTimeField(null= False , auto_now_add=True)
    payment_status = models.CharField(max_length=15 , default='FAILED')
    payment_id = models.CharField(max_length=60)
    payment_request_id = models.CharField(max_length=60 , unique=True , null=False)

    

class BookReview(models.Model):
    book=models.ForeignKey(book,related_name='reviews',on_delete=models.CASCADE)
    user=models.ForeignKey(User,related_name='reviews',on_delete=models.CASCADE)
    content = models.TextField(blank=True,null=True)
    stars=models.IntegerField(default=3)

    date_added=models.DateTimeField(auto_now_add=True)

    