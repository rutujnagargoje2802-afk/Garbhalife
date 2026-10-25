from django.contrib import admin
from .models import Product
from .models import ConsultationEnquiry
from .models import Testimonial
from .models import Appointment


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'category',
        'price',
        'stock',
        'is_available',
        'is_featured',
    )

    list_filter = (
        'category',
        'is_available',
        'is_featured',
    )

    search_fields = (
        'name',
        'description',
    )

    prepopulated_fields = {
        'slug': ('name',)
    }



@admin.register(ConsultationEnquiry)
class ConsultationEnquiryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "phone",
        "email",
        "interest",
        "created_at",
    )

    list_filter = (
        "interest",
        "created_at",
    )

    search_fields = (
        "name",
        "phone",
        "email",
    )

    ordering = (
        "-created_at",
    )



@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "is_active",
        "display_order",
        "created_at",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "name",
        "message",
    )

    ordering = (
        "display_order",
        "-created_at",
    )

from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "phone",
        "email",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "name",
        "phone",
        "email",
    )

    ordering = (
        "-created_at",
    )


    from django.contrib import admin
from .models import BlogPost

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    # 1. Columns displayed on the list page
    list_display = (
        'title', 
        'category', 
        'author', 
        'published_date', 
        'is_featured', 
        'is_published'
    )
    
    # 2. Clickable fields that link to the edit page
    list_display_links = ('title',)
    
    # 3. Sidebar filtering panels for fast navigation
    list_filter = ('category', 'is_featured', 'is_published', 'published_date')
    
    # 4. Search bar lookups (looks through title, short description, and author names)
    search_fields = ('title', 'short_description', 'author')
    
    # 5. Automatically generates the slug in real-time as you type the title
    prepopulated_fields = {'slug': ('title',)}
    
    # 6. Enables quick inline toggles directly from the main directory dashboard row
    list_editable = ('is_featured', 'is_published')
    
    # 7. Organizes fields into grouped visual sections on the edit form page
    fieldsets = (
        ('Core Details', {
            'fields': ('title', 'slug', 'category', 'author')
        }),
        ('Content Elements', {
            'fields': ('featured_image', 'short_description', 'content', 'reading_time')
        }),
        ('Publication Visibility Settings', {
            'fields': ('is_featured', 'is_published'),
            'description': 'Control where and how this post appears on your storefront blog layouts.'
        }),
    )
