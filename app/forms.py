from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from django_ckeditor_5.widgets import CKEditor5Widget


class ReservationForm(forms.Form):  # forms.ModelForm):
    LIST_CHOICES = (
        ('dine-in', 'Dine-In'),
        ('carry-out', 'Carry-Out'),
        ('event-catering', 'Event Catering'),
    )

    name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=100, required=False)
    email = forms.EmailField()
    service = forms.ChoiceField(choices=LIST_CHOICES)
    message = forms.CharField(widget=forms.Textarea)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    # class Meta:
    # model = Reservation
    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())
    # fields = ['name', 'email', 'service', 'message']


class AddReviewForm(forms.Form):  # forms.ModelForm):
    username = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'id': 'contact-your-username-6',
            'data-constraints': '@Required'
        })
    )

    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-input textarea-lg',
            'id': 'contact-message-6',
            'data-constraints': '@Required'
        })
    )

    rating = forms.CharField(max_length=100, required=False)

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(attrs={
        'class': 'recaptcha'
    }), label='')


class ContactForm(forms.Form):
    SERVICE_CHOICES = [
        ('1', 'Select a Service'),
        ('dine-in', 'Dine-In'),
        ('carry-out', 'Carry-Out'),
        ('event-catering', 'Event Catering')
    ]

    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'id': 'contact-your-name-6',
            'data-constraints': '@Required'
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'id': 'contact-email-6',
            'data-constraints': '@Email @Required'
        })
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-input textarea-lg',
            'id': 'contact-message-6',
            'data-constraints': '@Required'
        })
    )

    service = forms.ChoiceField(
        choices=SERVICE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-input',
            'data-minimum-results-for-search': 'Infinity',
            'data-constraints': '@Required'
        })
    )

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(attrs={
        'class': 'recaptcha'
    }), label='')


class NewsletterTemplateForm(forms.Form):
    subject = forms.CharField(max_length=255, label="Theme of the letter")
    message = forms.CharField(
        widget=CKEditor5Widget(
            config_name='extends',
        ),
        label="Text (HTML)"
    )


class NewsletterForm(forms.Form):
    email = forms.EmailField()
