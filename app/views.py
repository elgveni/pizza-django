import requests
from django.shortcuts import render, redirect
from .models import Category, Gallery, Slider, Banner, Product, Review, Block, Reservation, Newsletter, EmailTemplate
from .models import AboutUs, Team, History, ContactInfo
from django.shortcuts import get_object_or_404
from .forms import ReservationForm, ContactForm, NewsletterForm, AddReviewForm
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
import ast
import re


def home(request):
    categories = Category.objects.all()
    images = Gallery.objects.all()
    sliders = Slider.objects.all()
    header_banner = get_object_or_404(Banner, id=1, is_active=True)
    promotion_banner = get_object_or_404(Banner, id=2, is_active=True)
    products = Product.objects.filter(is_active=True, category_id=2).order_by('?')[:4]
    reviews = Review.objects.filter(is_active=True).order_by('?')[:10]
    blocks = Block.objects.filter(is_active=True).order_by('order')[:7]

    form = ContactForm()

    return render(request, 'home.html', {
        'categories': categories,
        'images': images,
        'sliders': sliders,
        'header_banner': header_banner,
        'promotion_banner': promotion_banner,
        'products': products,
        'range': range(1, 6),
        'reviews': reviews,
        'blocks': blocks,
        'form': form,
    })


def about_us(request):
    header_banner = get_object_or_404(Banner, id=1, is_active=True)
    lists = AboutUs.objects.filter(is_active=True).order_by('order')
    teams = Team.objects.filter(is_active=True).order_by('?')[:4]
    histories = History.objects.filter(is_active=True).order_by('year')
    reviews = Review.objects.filter(is_active=True).order_by('?')[:4]
    images = Gallery.objects.all()

    return render(request, 'about_us.html', {
        'header_banner': header_banner,
        'lists': lists,
        'teams': teams,
        'histories': histories,
        'reviews': reviews,
        'images': images,
    })


def contact(request):
    header_banner = get_object_or_404(Banner, id=1, is_active=True)
    images = Gallery.objects.all()
    contact_info = ContactInfo.objects.first()

    form = ContactForm()

    return render(request, 'contacts.html', {
        'header_banner': header_banner,
        'images': images,
        'form': form,
        'contact_info': contact_info,
    })


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = category.products.all()

    return render(request, 'category_detail.html', {
        'category': category,
        'products': products,
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    products = Product.objects.filter(is_active=True).order_by('?')[:4]
    reviews = Review.objects.filter(is_active=True, product_id=product_id).order_by('?')[:10]

    form = AddReviewForm()

    return render(request, 'product_detail.html', {
        'product': product,
        'range': range(1, 6),
        'products': products,
        'reviews': reviews,
        'form': form
    })


def drag(request):
    return render(request, 'drag_and_drop.html')

def reserve_table(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            Reservation.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                service=form.cleaned_data['service'],
                message=form.cleaned_data['message']
            )

            return JsonResponse({
                'status': 'MF000'
            })
        else:
            print(form.errors)
    else:
        form = ReservationForm()
    return render(request, 'home.html', {'form': form})


def add_review(request):
    if request.method == 'POST':
        form = AddReviewForm(request.POST)
        if form.is_valid():
            Review.objects.create(
                username=form.cleaned_data['username'],
                avatar=form.cleaned_data['avatar'],
                rating=form.cleaned_data['rating'],
                product_id=form.cleaned_data['product_id'],
                comment=form.cleaned_data['comment']
            )

            return JsonResponse({
                'status': 'MF000'
            })
        else:
            print(form.errors)
    else:
        form = AddReviewForm()
    return render(request, 'product_detail.html', {'form': form})


def verify_recaptcha(request):
    if request.method == 'POST':
        recaptcha_response = request.POST.get('g-recaptcha-response')

        url = 'https://www.google.com/recaptcha/api/siteverify'
        data = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        response = requests.post(url, data=data)
        result = response.json()

        if result.get('success'):
            return JsonResponse({
                'status': 'CPT000',
                'message': 'Thank you for your order. We will write to you soon!'
            })
        else:
            return JsonResponse({
                'status': 'CPT002',
                'message': 'Something wrong with google reCaptcha'
            }, status=400)

    return JsonResponse({
        'status': 'CPT001',
        'message': 'Please, setup you "site key" and "secret key" of reCaptcha'
    }, status=400)


def newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            Newsletter.objects.create(
                email=form.cleaned_data['email'],
            )

            return JsonResponse({
                'status': 'MF000'
            })
        else:
            print(form.errors)
    else:
        form = NewsletterForm()
    return render(request, 'home.html', {'form': form})


def send_mass_html_email(subject, message_html, recipient_list):
    # Text content (if HTML doesn't support)
    text_content = "This is an alternative text message."

    # Score sent the letters
    sent_count = 0

    for recipient in recipient_list:
        # Creating the object EmailMultiAlternatives for each recipient
        email = EmailMultiAlternatives(
            subject,
            text_content,
            settings.DEFAULT_FROM_EMAIL,
            [recipient]
        )
        # Add HTML-content
        email.attach_alternative(message_html, "text/html")

        # Sending the letter
        try:
            email.send()
            sent_count += 1  # Increase the counter if success sending
        except Exception as e:
            # Log errors, if they occur
            print(f"Error sending to {recipient}: {e}")

    return sent_count


def send_mail(request):
    if request.method == 'POST':
        template_id = request.POST.get('template_id')
        if template_id:
            try:
                # Extracting the template from DB by ID
                template = EmailTemplate.objects.get(id=template_id)

                # Access to fields of subject and content
                subject = template.subject
                # message = template.content
                message = re.sub(r'src="/images/', f'src="{settings.BASE_URL}/images/', template.content)

                # Getting datas _selected_action from POST
                selected_ids = request.POST.getlist('selected_ids')

                # Checking, if the first element of list is string, representing list
                if len(selected_ids) == 1 and isinstance(selected_ids[0], str):
                    try:
                        # Using ast.literal_eval for safely transformations string to list
                        selected_ids = ast.literal_eval(selected_ids[0])
                    except (ValueError, SyntaxError):
                        # Processing probably errors when parsing a string
                        selected_ids = []

                # Transforming only that elements, which are numbers
                selected_ids = [int(id) for id in selected_ids if str(id).isdigit()]

                recipients = Newsletter.objects.filter(id__in=selected_ids).values_list('email', flat=True)

                # emails = [(subject, message, settings.DEFAULT_FROM_EMAIL, [email]) for email in recipients]

                try:
                    # sent_count = send_mass_mail(emails, fail_silently=False)
                    sent_count = send_mass_html_email("Test HTML Email", message, recipients)
                    messages.success(request, f'Successful sent letters: {sent_count}')
                except Exception as e:
                    messages.error(request, f'Error sending: {str(e)}')

                return redirect('admin:app_newsletter_changelist')
            except EmailTemplate.DoesNotExist:
                # Processing a situation, if a template with selected ID not found
                print("Template not found.")
                messages.error(request, 'Template not found.')


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Получаем корзину из сессии, если её нет, создаём пустую
    cart = request.session.get('cart', {})

    # Добавляем товар в корзину или обновляем его количество
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] += 1  # Увеличиваем количество
    else:
        cart[str(product_id)] = {
            'name': product.title,
            'price': str(product.price),  # Преобразуем цену в строку для хранения в сессии
            'quantity': 1
        }

    # Сохраняем корзину в сессии
    request.session['cart'] = cart

    return redirect('cart_detail')  # Перенаправляем на страницу корзины


def update_cart(request, product_id, quantity):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] = quantity
        if cart[str(product_id)]['quantity'] <= 0:
            del cart[str(product_id)]  # Удаляем товар, если количество <= 0

    request.session['cart'] = cart
    return redirect('cart_detail')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        del cart[str(product_id)]  # Удаляем товар из корзины

    request.session['cart'] = cart
    return redirect('cart_detail')


def cart_detail(request):
    cart = request.session.get('cart', {})
    total_price = sum(float(item['price']) * item['quantity'] for item in cart.values())
    header_banner = get_object_or_404(Banner, id=1, is_active=True)
    contact_info = ContactInfo.objects.first()

    return render(request, 'cart_detail.html', {
        'cart': cart,
        'total_price': total_price,
        'header_banner': header_banner,
        'contact_info': contact_info
    })
