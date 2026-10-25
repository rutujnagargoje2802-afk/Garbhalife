"""
URL configuration for grabhalifew project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from homeapp import views

from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('about/',views.about,name='about'),
    path('services/',views.services,name='services'),
    path('programs/', views.programs, name='programs'),

    path('contact/', views.contact, name='contact'),
    path('store/', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path("blog/", views.blog, name="blog"),

    path(
        "blog/<slug:slug>/",
        views.blog,
        name="blog_detail"
    ),



    path(
        "cart/add/<int:product_id>/",
        views.add_to_cart,
        name="add_to_cart"
    ),

    path(
        "cart/update/<int:product_id>/",
        views.update_cart,
        name="update_cart"
    ),

    path(
        "cart/remove/<int:product_id>/",
        views.remove_from_cart,
        name="remove_from_cart"
    ),
    path(
    "payment/",
    views.payment,
    name="payment"
),
path(
    "payment/success/",
    views.payment_success,
    name="payment_success"
),
 path('payment-success/', views.payment_success, name='payment_success'),
]





if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
