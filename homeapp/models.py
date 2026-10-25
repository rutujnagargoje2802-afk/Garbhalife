
# Create your models here.
from django.db import models

from django.utils.text import slugify

class Product(models.Model):

    CATEGORY_CHOICES = [
        ('garbhasanskar', 'Garbhasanskar'),
        ('ayurveda', 'Ayurveda'),
        ('pregnancy', 'Pregnancy Wellness'),
        ('books', 'Books'),
        ('digital', 'Digital Products'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=200)

    slug = models.SlugField(
        unique=True,
        max_length=220
    )

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    short_description = models.CharField(
        max_length=300
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    original_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )

    image = models.ImageField(
        upload_to='products/'
    )

    stock = models.PositiveIntegerField(
        default=0
    )

    is_available = models.BooleanField(
        default=True
    )

    is_featured = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name



class ConsultationEnquiry(models.Model):

    INTEREST_CHOICES = [
        ("consultation", "Ayurvedic Consultation"),
        ("garbhasanskar", "Garbhasanskar Program"),
        ("pregnancy-wellness", "Pregnancy Wellness"),
        ("yoga", "Pregnancy Yoga & Meditation"),
        ("workshop", "Workshop"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    interest = models.CharField(
        max_length=50,
        choices=INTEREST_CHOICES,
        blank=True
    )
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.phone}"


   
class Testimonial(models.Model):

    name = models.CharField(max_length=100)

    message = models.TextField()

    image = models.ImageField(
        upload_to="testimonials/images/",
        blank=True,
        null=True
    )

    video = models.FileField(
        upload_to="testimonials/videos/",
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)

    display_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["display_order", "-created_at"]

    def __str__(self):
        return self.name


class Appointment(models.Model):

    name = models.CharField(max_length=100)

    email = models.EmailField(blank=True)

    phone = models.CharField(max_length=20)

    message = models.TextField(blank=True)

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.phone}"







class BlogPost(models.Model):

    CATEGORY_CHOICES = [
        ("Pregnancy", "Pregnancy"),
        ("Ayurveda", "Ayurveda"),
        ("Garbhasanskar", "Garbhasanskar"),
        ("Nutrition", "Nutrition"),
        ("Yoga & Meditation", "Yoga & Meditation"),
        ("Motherhood", "Motherhood"),
    ]

    title = models.CharField(max_length=200)

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    featured_image = models.ImageField(
        upload_to="blog/",
        blank=True,
        null=True
    )

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES
    )

    short_description = models.TextField()

    content = models.TextField()

    author = models.CharField(
        max_length=150,
        default="Dr. Prajakta Khade-Gite"
    )

    published_date = models.DateField(
        auto_now_add=True
    )

    reading_time = models.PositiveIntegerField(
        default=5,
        help_text="Reading time in minutes"
    )

    is_featured = models.BooleanField(
        default=False
    )

    is_published = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title