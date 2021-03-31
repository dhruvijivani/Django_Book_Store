from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, request
from django.contrib.auth.models import User, auth
from store.models import book,Cart
from store.models import Category
from django.contrib.sessions.models import Session
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as loginUser,logout as logoutUser
from .forms import UserRegisterForm,UserUpdateForm,UserCreationForm,ProfileUpdateForm


# Create your views here.


def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f'Account created  for {username}!')
            return redirect('login')

    else:
        form = UserRegisterForm()
    return render(request, 'signup.html', {'form': form})


def login(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        return render(request, 'login.html', context={'form': form})
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                loginUser(request, user)

                cart = Cart.objects.filter(user = user)
                session_cart = []
                for c in cart:
                    obj ={
                        'book': c.Book.id,
                        'category':c.Book.category.name,
                        'quantity':c.quantity
                    }
                    session_cart.append(obj)
                request.session['cart']=session_cart
                return redirect('main1')
        else:
            return render(request, 'login.html', context={'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form=UserUpdateForm(request.POST,instance=request.user)
        p_form=ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'your account has been updated!')
            return redirect('profile')

    else:  
        u_form=UserUpdateForm(instance=request.user)
        p_form=ProfileUpdateForm(instance=request.user.profile)
    context={
        'u_form':u_form,
        'p_form':p_form
         }
    return render(request, 'profile.html',context)

def logout(request):
    logoutUser(request)
    return redirect('/')


def main1(request):

        books = None
        categories = Category.get_all_categories()
        categoryID = request.GET.get('category')
        if categoryID:
            books = book.get_all_books_by_categoriesid(categoryID)
        else:
            books = book.get_all_books()
        data = {}
        data['books'] = books
        data['categories'] = categories

        return render(request, 'main1.html', data)
  
def search(request):
    search = request.GET.get('search')
    books = book.objects.filter(name__icontains=search)
    params = {'books': books}
    return render(request, 'search.html', params)