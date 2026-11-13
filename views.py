from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Cart, CartItem


# 1. HOME PAGE
def home(request):
    return render(request, 'home.html')


# 2. MENU PAGE
def menu(request):
    products = Product.objects.filter(available=True)

    return render(request, 'menu.html', {
        'products': products
    })


# 3. ABOUT PAGE
def about(request):
    return render(request, 'about.html')


# 4. BOOKING PAGE
def book(request):
    return render(request, 'book.html')


# 5. REGISTRATION PAGE
def register(request):

    if request.method == 'POST':

        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not username or not email or not password:
            messages.error(request, 'Please fill in all fields.')
            return redirect('register')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered!')
            return redirect('register')

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(
            request,
            'Registration successful! Please login.'
        )

        return redirect('login')

    return render(request, 'register.html')


# 6. LOGIN PAGE
def login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            auth_login(request, user)
            return redirect('home')

        messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


# 7. ADD PRODUCT TO CART

@login_required(login_url='login')
def add_to_cart(request, product_id):

    if request.method != 'POST':
        return redirect('menu')

    product = get_object_or_404(
        Product,
        id=product_id,
        available=True
    )

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, 'Food added to your cart!')

    return redirect('cart')




# 8. CART PAGE
@login_required(login_url='login')
def cart(request):

    user_cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_items = user_cart.items.select_related('product').all()

    total = user_cart.total()

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })