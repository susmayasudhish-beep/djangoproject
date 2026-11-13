from django.urls import path
from .import views

urlpatterns = [
    path('',views.home,name='home'),
    path('home/',views.home,name='home_page'),
    path('menu/',views.menu,name='menu'),
    path('about/',views.about,name='about'),
    path('book/',views.book,name='book'),
    path('register/', views.register, name='register'),
    path('login/',views.login,name='login'),
    path('cart/',views.cart,name='cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]