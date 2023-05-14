from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.urls import reverse
from django.utils import timezone
from django_countries.fields import CountryField

class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    enabled = models.BooleanField(default=False)

    def __str__(self):
        return self.name



class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    working_hours_start = models.TimeField()
    working_hours_end = models.TimeField()
    trial_end_date = models.DateField(default=timezone.now() + timedelta(days=30))
    disabled = models.BooleanField(default=False)

    street_address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    country = CountryField(blank_label='(select country)')

    WORKING_DAYS_CHOICES = [
        ('mon', 'Mon'),
        ('tue', 'Tue'),
        ('wed', 'Wed'),
        ('thu', 'Thurs'),
        ('fri', 'Fri'),
        ('sat', 'Sat'),
        ('sun', 'Sun'),
    ]
    working_days = models.JSONField()
    # Add a foreign key to the Category model
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.business_name


class ProfileImage(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/')

    def __str__(self):
        return self.client.business_name
    

class Service(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    describe_service = models.TextField(blank=True, null=True)
    duration = models.DurationField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    deposit_required = models.BooleanField(default=False)
    deposit_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return self.name

    
class ServiceType(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.DurationField()

    def __str__(self):
        return self.name

class ServiceImage(models.Model):
    image = models.ImageField(upload_to='service_images/')
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        if self.service_type:
            return f"{self.service_type.service.name} - {self.service_type.name} - {self.image.name}"
        else:
            return f"No Service Type Assigned - {self.image.name}"

    

from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    additional_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"



from django.db import models
def default_service_type(client):
    default_service = Service.objects.filter(client=client).first()
    return default_service.service_type.id if default_service else None

class Appointment(models.Model):
     
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE, default=None)
    date = models.DateField()
    time = models.TimeField()
    deposit_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f'{self.customer.user.username} - {self.service.name} - {self.date} - {self.time}'

    def get_absolute_url(self):
        return reverse('book:appointment_detail', kwargs={'pk': self.pk})
    
    @property
    def balance(self):
        return self.service.price - self.deposit_paid


from django.db import models
from django.utils import timezone
from django.db import models


class AvailableTimeSlot(models.Model):
    date = models.DateField(help_text="Enter the date for the time slot")
    time = models.TimeField(help_text="Enter the time for the time slot")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, help_text="Select your service")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, help_text="Select the client offering this time slot")
    is_booked = models.BooleanField(default=False, help_text="Indicates if the time slot has been booked")

    def __str__(self):
        return f'{self.date} {self.time} - {self.service}'

    
from django.contrib.auth.models import User
from django.db import models
from django.db import models

from django_countries.fields import CountryField

class Subscription(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    stripe_price_id = models.CharField(max_length=255, default='default_value')

    def __str__(self):
        return self.name

class SubscriptionPrice(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    country = CountryField(blank_label='(select country)')
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f'{self.subscription.name} ({self.country}): {self.price}'

class UserSubscription(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    active = models.BooleanField(default=True)

    def __str__(self):
        if self.client and self.subscription:
            return f'{self.client.business_name} - {self.subscription.name}'
        elif self.client:
            return f'{self.client.business_name} - No subscription'
        elif self.subscription:
            return f'No client - {self.subscription.name}'
        else:
            return 'No client - No subscription'


    def __str__(self):
        if self.client and self.subscription:
            return f'{self.client.business_name} - {self.subscription.name}'
        elif self.client:
            return f'{self.client.business_name} - No subscription'
        elif self.subscription:
            return f'No client - {self.subscription.name}'
        else:
            return 'No client - No subscription'

from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

from django.db import models
from django.contrib.auth.models import User

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        
from ckeditor.fields import RichTextField

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.email


from django.db import models
from ckeditor.fields import RichTextField

class NewsletterContent(models.Model):
    subject = models.CharField(max_length=255)
    message = RichTextField()

    def __str__(self):
        return self.subject
