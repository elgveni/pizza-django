from django.contrib import admin
from .models import Product, Review, Banner, Slider, Gallery, Category, Block, Reservation, Newsletter, AboutUs
from .models import EmailTemplate, Team, History, ContactInfo
from django.shortcuts import render

admin.site.register(Category)
admin.site.register(Gallery)
admin.site.register(Slider)
admin.site.register(Banner)
admin.site.register(Block)
admin.site.register(Reservation)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'discount', 'average_rating']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'username', 'rating', 'created_at']


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_date')
    actions = ['send_newsletter']

    # Add custom action for newsletter
    def send_newsletter(self, request, queryset):
        templates = EmailTemplate.objects.all()
        selected_ids = request.POST.getlist('_selected_action') or queryset.values_list('id', flat=True)

        return render(request, 'admin/send_newsletter.html', {
            'recipients': queryset,
            'templates': templates,
            'selected_ids': selected_ids
        })

    send_newsletter.short_description = 'Sending newsletter chosen users'


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject')


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_date')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['username', 'job', 'created_at']


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'year', 'created_at']


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    actions = []

    def has_add_permission(self, request):
        # We prohibit adding new records if at least one already exists
        if ContactInfo.objects.exists():
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        # Disable the ability to delete via the admin panel
        return False
