from django.shortcuts import render
from .models import Product
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ConsultationEnquiry
from .models import Testimonial, Appointment
from django.shortcuts import get_object_or_404
import razorpay
from django.conf import settings
from .models import Product, BlogPost



def home(request):

    # ==============================
    # APPOINTMENT FORM
    # ==============================

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        Appointment.objects.create(
            name=name,
            email=email,
            phone=phone,
            message=message
        )

        messages.success(
            request,
            "Your appointment request has been submitted successfully."
        )

        return redirect("home")


    # ==============================
    # TESTIMONIALS
    # ==============================

    testimonials = Testimonial.objects.filter(
        is_active=True
    )


    # ==============================
    # CONTEXT
    # ==============================

    context = {
        "testimonials": testimonials,
    }


    return render(
        request,
        "home.html",
        context
    )

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')


def services(request):
    return render(request, 'services.html')

def programs(request):
    return render(request, 'programs.html')



from django.shortcuts import render, get_object_or_404
from .models import BlogPost


def blog(request, slug=None):

    # ==============================
    # SINGLE BLOG POST
    # ==============================

    if slug:

        post = get_object_or_404(
            BlogPost,
            slug=slug,
            is_published=True
        )

        return render(
            request,
            "blog.html",
            {
                "post": post,
                "single_post": True,
            }
        )


    # ==============================
    # BLOG LIST
    # ==============================

    posts = BlogPost.objects.filter(
        is_published=True
    ).order_by("-published_date")


    featured_post = BlogPost.objects.filter(
        is_published=True,
        is_featured=True
    ).order_by("-published_date").first()


    categories = BlogPost.objects.filter(
        is_published=True
    ).values_list(
        "category",
        flat=True
    ).distinct()


    context = {
        "posts": posts,
        "featured_post": featured_post,
        "categories": categories,
        "single_post": False,
    }


    return render(
        request,
        "blog.html",
        context
    )
def contact(request):

    if request.method == "POST":

        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        interest = request.POST.get("interest")
        message = request.POST.get("message")

        ConsultationEnquiry.objects.create(
            name=name,
            phone=phone,
            email=email,
            interest=interest,
            message=message
        )

        messages.success(
            request,
            "Thank you! Your enquiry has been submitted successfully."
        )

        return redirect("contact")

    return render(request, "contact.html")

def store(request):

    products = Product.objects.filter(
        is_available=True
    ).order_by('-created_at')

    featured_products = Product.objects.filter(
        is_available=True,
        is_featured=True
    ).order_by('-created_at')

    context = {
        'products': products,
        'featured_products': featured_products,
    }

    return render(
        request,
        'store.html',
        context
    )

def cart(request):

    cart_data = request.session.get("cart", {})

    cart_items = []

    total = 0

    for product_id, quantity in cart_data.items():

        product = get_object_or_404(
            Product,
            id=product_id,
            is_available=True
        )

        subtotal = product.price * quantity

        total += subtotal

        cart_items.append({
            "product": product,
            "quantity": quantity,
            "subtotal": subtotal,
        })

    context = {
        "cart_items": cart_items,
        "total": total,
    }

    return render(
        request,
        "cart.html",
        context
    )



def add_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
        is_available=True
    )

    cart = request.session.get("cart", {})

    product_id = str(product_id)

    current_quantity = cart.get(product_id, 0)

    if current_quantity < product.stock:

        cart[product_id] = current_quantity + 1

        request.session["cart"] = cart
        request.session.modified = True

        messages.success(
            request,
            f"{product.name} added to your cart."
        )

    else:

        messages.warning(
            request,
            "Sorry, maximum available stock reached."
        )

    return redirect("cart")

def update_cart(request, product_id):

    if request.method == "POST":

        try:
            quantity = int(
                request.POST.get("quantity", 1)
            )
        except (ValueError, TypeError):
            quantity = 1

        product = get_object_or_404(
            Product,
            id=product_id,
            is_available=True
        )

        cart = request.session.get("cart", {})

        product_id = str(product_id)

        if quantity <= 0:

            cart.pop(product_id, None)

        elif quantity <= product.stock:

            cart[product_id] = quantity

        else:

            cart[product_id] = product.stock

            messages.warning(
                request,
                f"Only {product.stock} items are available."
            )

        request.session["cart"] = cart
        request.session.modified = True

    return redirect("cart")
def remove_from_cart(request, product_id):

    cart = request.session.get("cart", {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


def cart_count(request):  # must accept 'request'
    cart = request.session.get("cart", {})
    total_items = sum(cart.values()) if cart else 0
    return {"cart_count": total_items}






def payment(request):
    cart_data = request.session.get("cart", {})

    if not cart_data:
        messages.warning(request, "Your cart is empty.")
        return redirect("cart")

    cart_items = []
    total = 0

    for product_id, quantity in cart_data.items():
        product = get_object_or_404(
            Product,
            id=product_id,
            is_available=True
        )

        subtotal = product.price * quantity
        total += subtotal

        cart_items.append({
            "product": product,
            "quantity": quantity,
            "subtotal": subtotal,
        })

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        pincode = request.POST.get("pincode")
        payment_method = request.POST.get("payment_method")

        if not all([name, email, phone, address, city, state, pincode, payment_method]):
            messages.error(request, "Please fill all required fields.")
            return redirect("payment")

        request.session["checkout_data"] = {
            "name": name, "email": email, "phone": phone,
            "address": address, "city": city, "state": state,
            "pincode": pincode, "payment_method": payment_method,
        }
        request.session.modified = True

        if payment_method == "cod":
            messages.success(request, "Your order details have been submitted successfully.")
            return redirect("payment_success")

    # ==============================================================================
    # ADDED BACK: RAZORPAY INITIALIZATION LOGIC
    # ==============================================================================
    amount = int(total * 100)  # Amount must be in paise
    razorpay_order_id = ""

    try:
        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )
        razorpay_order = client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": 1
        })
        razorpay_order_id = razorpay_order["id"]
    except Exception as e:
        print(f"Razorpay Order Generation Failure Log: {e}")
        # Server fallbacks to let the page load gracefully if key setup isn't done yet

    context = {
        "cart_items": cart_items,
        "total": total,
        "amount": amount,
        "razorpay_order_id": razorpay_order_id,
        "razorpay_key": settings.RAZORPAY_KEY_ID,
    }

    return render(request, "payment.html", context)

def payment_success(request):
    """
    Renders the success confirmation page after an order is processed.
    """
    return render(
        request,
        "payment_success.html"
    )
