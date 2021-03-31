from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [

    path('', views.home, name="home"),
    path('cart', views.cart, name="cart"),
    path('cart/', views.cart, name="cart"),
    path('orders/', views.orders, name="orders"),
    path('orders', views.orders, name="orders"),
    path('checkout/', views.checkout, name="checkout"),
    path('checkout', views.checkout, name="checkout"),
    path('product/<str:slug>', views.show_products, name="show_products"),
    path('addtocart/<str:slug>/<str:category>',views.add_to_cart,name="addtocart"),
    path('accounts/addtocart/<str:slug>/<str:category>',views.add_to_cart,name="addtocart"),
     path('validate_payment',views.validatePayment,name="validatePayment"),
    
    
    path('managecart/<int:c_id>/',views.ManageCartView.as_view(),name="managecart"),
    path('managecart/<int:c_id>',views.ManageCartView.as_view(),name="managecart"),
      
    # submit email from
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
         name="reset_password"),
    # email sent success msg
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"),
         name="password_reset_done"),
    # link to reset password
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),
    # pass succesfully changed msg
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"), name="password_reset_complete"),

]