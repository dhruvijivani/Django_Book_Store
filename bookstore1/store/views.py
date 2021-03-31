# Create your views here.
from django.shortcuts import redirect, render, HttpResponse
from .models import book, Cart, Category, Order, OrderItem, Payment
from django.contrib.auth.decorators import login_required
from accounts.views import login
from store.checkout_form import CheckForm
from PIL.Image import new
from store.models import book,BookReview
from django.contrib import messages
from django.views import View
from bookstore1.settings import API_KEY, AUTH_TOKEN
from instamojo_wrapper import Instamojo
from django.contrib.auth.models import User, auth
import datetime
from django.contrib.auth import login as login_user
API = Instamojo(api_key=API_KEY, auth_token=AUTH_TOKEN, endpoint='https://test.instamojo.com/api/1.1/')
# api = Instamojo(api_key=API_KEY,
# auth_token=AUTH_TOKEN)
# Create your views here.


def home(request):
    return render(request, 'home.html')


def orders(request):
    user=request.user
    orders=Order.objects.filter(user=user).order_by('-date')
    context={
        "orders":orders
    }
    for order in orders:
        print(order.date + datetime.timedelta(days=5))
    if len(orders) == 0:
        messages.success(request, f'No Orders Yet!')
        print("No Orders Yet!")

    return render(request, 'orders.html',context=context)


def cart(request):
    cart = request.session.get('cart')
    if cart is None:
        cart = []

    for c in cart:
        book_id = c.get('book')
        Book = book.objects.get(id=book_id)
        c['book'] = Book
    print(cart)
    if len(cart) == 0:
        messages.success(request, f'Your cart is empty!')
        print("Your cart is empty!")
        return render(request,'ecart.html')
    return render(request, 'cart.html', context={'cart': cart})


def show_products(request, slug):
    Book = book.objects.get(slug=slug)
    
    if request.method == 'POST' and request.user.is_authenticated:
        stars = request.POST.get('stars',3)
        content = request.POST.get('content','')
        user=request.user
        review = BookReview.objects.create(book=Book,user=request.user,stars=stars,content=content)
        print(review)
        return redirect('show_products', slug=slug)
    return render(request, 'show_products.html', context={'book': Book})


def add_to_cart(request, slug, category):

    user = None
    if request.user.is_authenticated:
        user = request.user

    cart = request.session.get('cart')
    context = {}

    if cart is None:
        cart = []

    Book = book.objects.get(slug=slug)
    cat_temp = Category.objects.get(name=category)
    remove = request.GET.get('remove')
    books = request.GET.get('books')
    is_exist = Cart.objects.filter(Book=Book, user=user)
    print(len(is_exist))
    if len(is_exist) > 0:
        messages.info(request, f'Book already exist in your Cart!')
    else:
        flag = True
        for cart_obj in cart:
            book_id = cart_obj.get('book')
            cat_temp = cart_obj.get('category')
            if book_id == Book.id and category == cat_temp:
                flag = False
                cart_obj['quantity'] = cart_obj['quantity']+1

        if flag:
            cart_obj = {
                'book': Book.id,
                'quantity': 1,
                'category': category
            }
            
            c = Cart()
            c.Book=Book
            if c.Book.available_quantity<=0:
                messages.success(request, f'Sorry.. currently Book is Out of stock!')
            else:
                cart.append(cart_obj)
                messages.success(request, f'Book added  in your Cart!')
                c.user = user
                c.Book = Book
                c.Category = cat_temp
                c.quantity = 1
                c.Book.available_quantity=c.Book.available_quantity-c.quantity
                c.Book.save()
                c.save()

    request.session['cart'] = cart
    return_url = request.GET.get('return_url')
    cart = request.session.get('cart')
    print(cart)
    return redirect(return_url)


def cal_total_payable_amount(cart):
    total = 0
    for c in cart:
        b = c.get('book')
        price = c.get('book').price
        total_of_single_book = price * c.get('quantity')
        total = total + total_of_single_book
    return total


@login_required(login_url="/login/")
def checkout(request):
    if request.method == 'GET':
        form = CheckForm()
        cart = request.session.get("cart")
        if cart is None:
            cart = []
        for c in cart:

            book_id = c.get('book')
            Book = book.objects.get(id=book_id)
            c['book'] = Book

        return render(request, "checkout.html", {"form": form, "cart": cart})
    else:
        form = CheckForm(request.POST)
        user = None
        if request.user.is_authenticated:
            user = request.user
        if form.is_valid():
            cart = request.session.get('cart')
            if cart is None:
                cart = []
            for c in cart:

                book_id = c.get('book')
                Book = book.objects.get(id=book_id)
                c['book'] = Book
            address = form.cleaned_data.get('address')
            state=form.cleaned_data.get('state')
            city=form.cleaned_data.get('city')
            pincode=form.cleaned_data.get('pincode')
            phone = form.cleaned_data.get('phone')
            payment_method = form.cleaned_data.get('payment_method')
            total = cal_total_payable_amount(cart)
            print(phone, payment_method, address, total)
            order = Order()
            order.address = address
            order.state=state
            order.city=city
            order.pincode=pincode
            order.phone = phone
            order.payment_method = payment_method
            order.total = total
            order.order_status = "PENDING"
            order.user = user
            order.save()
            print(order.id)
            # saving order items
            for c in cart:
                order_item = OrderItem()
                order_item.order = order
                Book = c.get('book')
                order_item.price = c.get('book').price
                order_item.quantity = c.get('quantity')
                order_item.Book = Book
                order_item.save()

            buyer_name = f'{user.first_name} {user.last_name}'
            print(buyer_name)
            # creating payment
            response = API.payment_request_create(
                amount=order.total,
                purpose='Book Payment',
                send_email=True,
                buyer_name=f'{user.first_name} {user.last_name}',
                email=user.email,
                redirect_url=f"http://localhost:8000/validate_payment?user={user.id}")

            payment_request_id = response['payment_request']['id']
            url = response['payment_request']['longurl']

            payment = Payment()
            payment.order = order
            payment.payment_request_id = payment_request_id
            payment.save()

            return redirect(url)

            # return redirect('/checkout/')
        else:
            return redirect('/checkout/')


class ManageCartView(View):
    def get(self, request, *args, **kwargs):
        c_id = self.kwargs["c_id"]
        user = request.user
        action = request.GET.get("action")
        cp_obj = book.objects.get(id=c_id)
        cart_obj = Cart.objects.get(Book=cp_obj, user=user)
        if action == "inc":
            if cart_obj.Book.available_quantity<=0:
                messages.error(request, f'Sorry.. currently Book is not available!')
                cart_obj.Book.available_quantity=0
                cart_obj.Book.save()
            else:
                cart_obj.Book.available_quantity-=1
                cart_obj.quantity += 1
                cart_obj.Book.save()
            cart_obj.save()
        elif action == "dcr":
            if cart_obj.quantity <= 1:
                cart_obj.Book.available_quantity+=1
                cart_obj.save()
                cart_obj.delete()
                cart_obj.Book.save()
            else:
                cart_obj.quantity -= 1
                cart_obj.Book.available_quantity+=1
                cart_obj.Book.save()
                cart_obj.save()
        elif action == "rmv":
            cart_obj.Book.available_quantity+=cart_obj.quantity
            cart_obj.save()
            cart_obj.Book.save()
            cart_obj.delete()

        else:
            print("error")
        cart = Cart.objects.filter(user=user)
        cart1 = request.session.get('cart')
        session_cart = []
        if cart1 is None:
            cart1 = []

        else:
            for c in cart:
                obj = {
                    'book': c.Book.id,
                    'category': c.Book.category.name,
                    'quantity': c.quantity
                }
                session_cart.append(obj)
        request.session['cart'] = session_cart

        return redirect("cart")


def validatePayment(request):
    user=None
    if request.user.is_authenticated:
        user=request.user
    user_id=request.GET.get('user')
    payment_request_id=request.GET.get('payment_request_id')
    payment_id=request.GET.get('payment_id')
    print(payment_id,payment_request_id)
    response = API.payment_request_payment_status(payment_request_id, payment_id)

               # Purpose of Payment Request
    status=response.get('payment_request').get('payment').get('status')           
    user=User.objects.get(id=user_id)
    login_user(request,user)
    if status !="Failed":
        try:
            payment=Payment.objects.get(payment_request_id=payment_request_id)
            payment.payment_id=payment_id
            payment.payment_status=status
            payment.save()
            order=payment.order
            order.order_status='PLACED'
            order.save()
            cart=[]
            request.session['cart']=cart
            Cart.objects.filter(user=user).delete()
            print(user)
            return render(request,'payment_success.html')
        except:
            
            return render(request,'payment_failed.html')
            
    else:
        return render(request,'payment_failed.html')