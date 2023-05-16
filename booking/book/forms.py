from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views import View


from .models import Client, NewsletterSubscriber
from django.forms import TimeInput

from django import forms
from django.forms.widgets import TimeInput
from .models import Client
from django.contrib.auth.models import User

from django import forms
from .models import Client, Category, ServiceType 

from django import forms
from .models import Client, Category

class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['business_name', 'contact_email', 'contact_phone', 'working_hours_start', 'working_hours_end', 'category']

    def __init__(self, *args, **kwargs):
        super(ClientProfileForm, self).__init__(*args, **kwargs)
        self.fields['category'].widget = forms.Select(choices=[(c.id, c.name) for c in Category.objects.filter(enabled=True)])


SUBSCRIPTION_CHOICES = (
    ('free_trial', 'Free Trial'),
    ('regular', 'Regular'),
    ('premium', 'Premium'),
    ('xtra', 'Xtra'),
)
WEEKDAYS_CHOICES = (
    (0, 'Monday'),
    (1, 'Tuesday'),
    (2, 'Wednesday'),
    (3, 'Thursday'),
    (4, 'Friday'),
    (5, 'Saturday'),
    (6, 'Sunday'),
)
from django_countries.widgets import CountrySelectWidget
from django_countries.fields import CountryField

class ClientRegistrationForm(ClientProfileForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput, required=True)
    working_hours_start = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    working_hours_end = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    subscription_type = forms.ChoiceField(choices=SUBSCRIPTION_CHOICES, required=True)
    working_days = forms.MultipleChoiceField(choices=Client.WORKING_DAYS_CHOICES, widget=forms.CheckboxSelectMultiple(), required=True)
    
    # Adding new fields
    street_address = forms.CharField(max_length=255, required=False)
    city = forms.CharField(max_length=50, required=False)
    state = forms.CharField(max_length=50, required=False)
    country = CountryField().formfield(widget=CountrySelectWidget())

    class Meta(ClientProfileForm.Meta):
        fields = ClientProfileForm.Meta.fields + ['username', 'email', 'password1', 'password2', 'subscription_type', 'working_days', 'street_address', 'city', 'state', 'country']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('.com'):
            raise forms.ValidationError("Email must end with @example.com")
        return email

    def clean_contact_phone(self):
        phone = self.cleaned_data.get('contact_phone')
        if not phone.isdigit():
            raise forms.ValidationError("Phone number must be digits only")
        return phone

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        return password2

    def save(self, commit=True):
        user = User(username=self.cleaned_data['username'], email=self.cleaned_data['email'])
        user.set_password(self.cleaned_data['password1'])
        user.save()

        client = super(ClientRegistrationForm, self).save(commit=False)
        client.user = user

        if commit:
            client.save()

        return client

class SecondPageForm(forms.ModelForm):
    additional_info = forms.CharField(required=False)

    class Meta:
        model = Client
        fields = ['working_days', 'street_address', 'city', 'state', 'country']



from django import forms
from .models import Appointment, Service

class CustomerBookingForm(forms.ModelForm):
    service = forms.ModelChoiceField(queryset=Service.objects.all(), required=True)
    date = forms.DateField(widget=forms.SelectDateWidget, required=True)
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=True)

    class Meta:
        model = Appointment
        fields = ('service', 'date', 'time')

from django import forms

from django import forms
from .models import Category

class ServiceSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        label="Search",
        widget=forms.TextInput(attrs={
            'placeholder': 'SEARCH BUSINESS/CLIENT...',
            'id': 'client_search'
        })
    )
    category = forms.ModelChoiceField(
        required=False,
        queryset=Category.objects.filter(enabled=True),
        empty_label="Select Service Category"
    )
    country = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Country'})
    )
    state = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'State'})
    )
    city = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'City'})
    )


from django import forms
from django.contrib.auth.models import User
from .models import Appointment, Customer
from .models import AvailableTimeSlot

class AppointmentForm(forms.ModelForm):
    name = forms.CharField(max_length=150, required=True, label="Name")
    date = forms.DateField(widget=forms.TextInput(attrs={'readonly': 'readonly'}), required=True)
    email = forms.EmailField(required=True, label="Email")
    phone_number = forms.CharField(max_length=20, required=True, label="Phone Number")
    time_slot = forms.ModelChoiceField(queryset=AvailableTimeSlot.objects.none(), required=True, label='Time', widget=forms.HiddenInput())
    service_type = forms.ModelChoiceField(queryset=ServiceType.objects.none(), required=True, label='Service Type')

   

    class Meta:
        model = Appointment
        fields = ['service', 'service_type', 'time_slot', 'date', 'name', 'email', 'phone_number']


    def __init__(self, *args, **kwargs):
        time_slots = kwargs.pop('time_slots', None)
        client = kwargs.pop('client', None)  # Add this line
        super(AppointmentForm, self).__init__(*args, **kwargs)
        if time_slots:
            self.fields['time_slot'].queryset = time_slots
        if client:  # Add this block
            self.fields['service'].queryset = Service.objects.filter(client=client)
            self.fields['service_type'].queryset = ServiceType.objects.filter(service__client=client)
           

class DashboardAppointmentForm(forms.ModelForm):
    name = forms.CharField(max_length=150, required=True, label="Name", widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Date'}), required=True)
    time_slot = forms.ModelChoiceField(queryset=AvailableTimeSlot.objects.none(), required=False, widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_time_slot'}))
    email = forms.EmailField(required=True, label="Email", widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    phone_number = forms.CharField(max_length=20, required=True, label="Phone Number", widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}))
    service_type = forms.ModelChoiceField(queryset=ServiceType.objects.none(), required=True, label='Service Type')

    class Meta:
        model = Appointment
        fields = ['service', 'service_type', 'date', 'time_slot', 'name', 'email', 'phone_number']

    def __init__(self, *args, **kwargs):
        client = kwargs.pop('client', None)
        super(DashboardAppointmentForm, self).__init__(*args, **kwargs)
        if client:
            self.fields['service'].queryset = Service.objects.filter(client=client)
            self.fields['service_type'].queryset = ServiceType.objects.filter(service__client=client)



      
from django import forms
from .models import AvailableTimeSlot, Service

class AvailableTimeSlotForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.SelectDateWidget,
        required=False,
        help_text="Enter the date for the time slot"
    )
    time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        required=False,
        help_text="Enter the time for the time slot"
    )
    auto_generate = forms.BooleanField(
        required=False,
        initial=False,
        help_text="Enable to auto-generate time slots for the specified number of weeks"
    )
    weeks = forms.IntegerField(
        required=False,
        initial=1,
        help_text="Specify the number of weeks for auto-generating time slots"
    )

    class Meta:
        model = AvailableTimeSlot
        fields = ['service', 'date', 'time', 'auto_generate', 'weeks']

    def __init__(self, *args, **kwargs):
        client = kwargs.pop('client', None)
        super(AvailableTimeSlotForm, self).__init__(*args, **kwargs)

        if client:
            self.fields['service'].queryset = Service.objects.filter(client=client)



from django import forms
from .models import Client, Service, ProfileImage, ServiceImage

class ClientSettingsForm(forms.ModelForm):
    business_name = forms.CharField(max_length=255)
    contact_email = forms.EmailField()
    contact_phone = forms.CharField(max_length=20)
    working_hours_start = forms.TimeField()
    working_hours_end = forms.TimeField()
    profile_image = forms.ImageField(required=False)
    service_images = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}))
    working_days = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=Client.WORKING_DAYS_CHOICES)

    class Meta:
        model = Client
        fields = [
            'business_name',
            'contact_email',
            'contact_phone',
            'working_hours_start',
            'working_hours_end',
            'profile_image',
            'service_images',
            'working_days'
        ]

    def __init__(self, *args, **kwargs):
        super(ClientSettingsForm, self).__init__(*args, **kwargs)
        self.fields['service_images'].label = "Service Images (You can select multiple images)"

    def save(self, commit=True):
        client = super(ClientSettingsForm, self).save(commit=False)

        if 'profile_image' in self.files:
            profile_image = ProfileImage(image=self.files['profile_image'], client=client)
            profile_image.save()
            client.profile_image = profile_image

        if commit:
            client.save()

        if 'service_images' in self.files:
            for image in self.files.getlist('service_images'):
                service_image = ServiceImage(image=image, client=client)
                service_image.save()
                client.service_images.add(service_image)

        return client


class ServiceForm(forms.ModelForm):
    name = forms.CharField(max_length=255)
    price = forms.DecimalField(max_digits=10, decimal_places=2)
    describe_service = forms.CharField(widget=forms.Textarea(attrs={'rows': 1}), required=False)
    deposit_required = forms.BooleanField(required=False)
    deposit_amount = forms.DecimalField(max_digits=10, decimal_places=2, required=False)

    class Meta:
        model = Service
        fields = [
            'name',
            'price',
            'duration',
            
            'deposit_required',
            'deposit_amount',
        ]
class ServiceTypeForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 1}), required=False)

    class Meta:
        model = ServiceType
        fields = ['name', 'description', 'price', 'duration', 'service']

    def __init__(self, *args, client, **kwargs):
        super(ServiceTypeForm, self).__init__(*args, **kwargs)
        self.fields['service'].queryset = Service.objects.filter(client=client)
        

from django import forms
from .models import ServiceImage
class ServiceImageForm(forms.ModelForm):
    class Meta:
        model = ServiceImage
        fields = ['image', 'service_type']

    def __init__(self, *args, client, **kwargs):
        super(ServiceImageForm, self).__init__(*args, **kwargs)
        self.fields['service_type'].queryset = ServiceType.objects.filter(service__client=client)


class EditAppointmentForm(forms.ModelForm):
    date = forms.DateField(widget=forms.SelectDateWidget, required=True)
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=True)

    class Meta:
        model = Appointment
        fields = ['service', 'date', 'time', 'status']


from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']


from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customer

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Customer

class CustomerRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=150, required=True, label="Full Name")
    email = forms.EmailField(required=True, label="Email")
    phone_number = forms.CharField(max_length=20, required=True, label="Phone Number")

    class Meta:
        model = User
        fields = ['name', 'email', 'phone_number', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["name"]
        if commit:
            user.save()
            customer = Customer(user=user, phone_number=self.cleaned_data["phone_number"])
            customer.save()
        return customer  # Return the customer instance instead of the user instance

from django import forms
from .models import NewsletterSubscriber

class NewsletterSubscriptionForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))

    class Meta:
        model = NewsletterSubscriber
        fields = ('email',)

from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import NewsletterContent

class SendNewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterContent
        fields = ('subject', 'message')
        widgets = {
            'message': CKEditorWidget(),
        }

from django import forms
from .models import Category

class CategoryCreationForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
