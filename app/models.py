from django.db import models
from django.utils import timezone
from datetime import timedelta
from django_ckeditor_5.fields import CKEditor5Field


class Category(models.Model):
    ICON_CHOICES = (
        ('cake', 'Cake'),
        ('teacup', 'Teacup'),
        ('teapot', 'Teapot'),
        ('egg', 'Egg'),
        ('steak', 'Steak'),
        ('hamburger', 'Hamburger'),
        ('hotdog', 'Hotdog'),
        ('pizza', 'Pizza'),
        ('sausage', 'Sausage'),
        ('chicken', 'Chicken'),
        ('fish', 'Fish'),
        ('carrot', 'Carrot'),
        ('cheese', 'Cheese'),
        ('bread', 'Bread'),
        ('ice-cream', 'Ice cream'),
        ('candy', 'Candy'),
        ('lollipop', 'Lollipop'),
        ('coffee-bean', 'Coffee bean'),
        ('coffee-cup', 'A cup of coffee'),
        ('cherry', 'Cherry'),
        ('grapes', 'Grapes'),
        ('citrus', 'Citrus'),
        ('apple', 'Apple'),
        ('leaf', 'Leaf'),
    )

    icon = models.CharField(max_length=100, choices=ICON_CHOICES)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='categories/')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Gallery(models.Model):
    image = models.ImageField(upload_to='galleries/')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()


class Slider(models.Model):
    title = models.CharField(max_length=200)
    desc = models.TextField()
    image = models.ImageField(upload_to='sliders/')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Banner(models.Model):
    title = models.CharField(max_length=200)
    desc = models.TextField(blank=True, null=True)
    caption = models.CharField(max_length=250)
    image = models.ImageField(upload_to='banners/')
    link = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    discount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Discount", default=0.00)
    desc = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='products/')
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(
        'Category',
        on_delete=models.CASCADE,
        related_name='products'
    )
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    @property
    def average_rating(self):
        total = sum(review.rating for review in self.reviews.all())
        count = self.reviews.count()
        return total / count if count else 0

    @property
    def discounted_price(self):
        if self.discount > 0:
            discount_amount = (self.discount / 100) * self.price
            final_price = self.price - discount_amount
            return "{:.2f}".format(final_price)
        return "{:.2f}".format(self.price)

    @property
    def is_new(self):
        return self.created_date >= timezone.now() - timedelta(days=30)


class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    username = models.CharField(max_length=200)
    rating = models.PositiveIntegerField(default=1, choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username}: {self.rating}"


class Block(models.Model):
    title = models.CharField(max_length=200)
    caption = models.CharField(max_length=250)
    image = models.ImageField(upload_to='blocks/')
    link = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    width = models.CharField(max_length=200)
    height = models.CharField(max_length=50)
    order = models.CharField(max_length=50)
    css_class = models.CharField(max_length=200, default='wow')
    css_col_class = models.CharField(max_length=200, default='col-sm-4')
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Reservation(models.Model):
    LIST_CHOICES = (
        ('dine-in', 'Dine-In'),
        ('carry-out', 'Carry-Out'),
        ('event-catering', 'Event Catering'),
    )

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()
    service = models.CharField(max_length=100, choices=LIST_CHOICES)
    message = models.TextField()

    def __str__(self):
        return f"Reservation by {self.name}"


class Newsletter(models.Model):
    email = models.EmailField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email


class EmailTemplate(models.Model):
    name = models.CharField(max_length=255, verbose_name="Template")
    subject = models.CharField(max_length=255, verbose_name="Theme of the letter")
    content = CKEditor5Field(verbose_name="Text (HTML)")

    def __str__(self):
        return self.name


class AboutUs(models.Model):
    title = models.CharField(max_length=200)
    caption = models.CharField(max_length=250)
    image = models.ImageField(upload_to='blocks/')
    content = CKEditor5Field(verbose_name="Text (HTML)")
    is_active = models.BooleanField(default=True)
    order = models.CharField(max_length=50)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Team(models.Model):
    username = models.CharField(max_length=200)
    job = models.CharField(max_length=200)
    avatar = models.ImageField(upload_to='teams/', blank=True, null=True)
    link_facebook = models.URLField(blank=True, null=True)
    link_twitter = models.URLField(blank=True, null=True)
    link_instagram = models.URLField(blank=True, null=True)
    link_google_plus = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username}: {self.job}"


class History(models.Model):
    title = models.CharField(max_length=250)
    year = models.PositiveIntegerField()
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}: {self.year}"


class ContactInfo(models.Model):
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    # Social media
    instagram = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    google_plus = models.URLField(blank=True, null=True)

    def __str__(self):
        return "Contact Information"
