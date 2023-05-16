from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView
from book.mixins import ActiveClientRequiredMixin
from .models import Client, Appointment, Review, Service, ServiceImage, Customer, ProfileImage, Customer, ServiceType, Subscription, UserSubscription
from .forms import CustomerBookingForm, CustomerRegistrationForm, DashboardAppointmentForm, EditAppointmentForm, ReviewForm, ServiceTypeForm
from .forms import AppointmentForm
from django.views.generic.edit import FormView
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View
from .forms import ClientRegistrationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date
from django.utils import timezone
from .forms import ServiceSearchForm
from django.views.generic import View,  DetailView, ListView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Client
from .forms import ClientSettingsForm, ServiceForm, ServiceImageForm  # Import ServiceImageForm       
from django.contrib.auth.models import User
from .models import Client, Customer, Appointment
from .models import Client, Appointment, Service
import json
from datetime import timedelta
from decimal import Decimal
from django.core import serializers
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import AvailableTimeSlot
from .forms import AvailableTimeSlotForm
from django.http import HttpResponseForbidden, JsonResponse
from .models import AvailableTimeSlot, Service
from django.http import JsonResponse
from .models import Appointment
import json   
from django.contrib.auth.models import User
from .models import Client, Appointment
from django.core.mail import send_mail
from django.http import Http404, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Note
from .forms import NoteForm
# Import other required modules
from .models import Appointment
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView as AuthLoginView
from .models import Client
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .forms import NewsletterSubscriptionForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, DeleteView
from .models import AvailableTimeSlot
from .forms import AvailableTimeSlotForm
from django.views.generic.edit import FormView
from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from .models import NewsletterSubscriber
from .forms import NewsletterSubscriptionForm
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views import View
from django.views import generic
from .models import Client, Service
from .forms import ServiceSearchForm
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView,
)
from django.http import JsonResponse
from .models import ServiceType
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .models import Category
from .forms import CategoryCreationForm
from django.http import HttpResponse
from .resources import AppointmentResource
import tablib
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags  
from paypalrestsdk import Payment

import paypalrestsdk
from django.contrib import messages
from .forms import SendNewsletterForm
from django.shortcuts import render, redirect
from .models import Subscription
from django.contrib.auth.models import User
from .models import UserSubscription
from django.conf import settings
import stripe
from datetime import datetime, timedelta

from .models import UserSubscription, Subscription
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from django.db.models import Count, F
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from .models import Appointment  # Make sure to import the Appointment model
from datetime import datetime, timedelta
from datetime import datetime, time
from django.core.paginator import Paginator, PageNotAnInteger
from django.views.generic import ListView
from book.models import AvailableTimeSlot
from .forms import NewsletterSubscriptionForm
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from .models import Client, SubscriptionPrice
from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class IndexView(TemplateView):
    template_name = 'book/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ServiceSearchForm()
        return context

class RegisterView(View):
    template_name = 'book/register.html'
    
    def get(self, request):
        form = ClientRegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)  # Set commit=False here
            client.working_days = form.cleaned_data['working_days']  # Add this line
            client.save()  # Save the client instance

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')

            subscription_type = form.cleaned_data.get('subscription_type')
            if subscription_type != 'free_trial':
                return redirect('book:choose_subscription', client_id=client.id)
            else:
                return redirect('book:login')
        return render(request, self.template_name, {'form': form})


class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        client = request.user.client
        if client.trial_end_date < timezone.now().date():
            return redirect('book:choose_subscription')

        appointments = Appointment.objects.filter(service__client=client)
        total_appointments = appointments.count()
        upcoming_appointments = appointments.filter(date=date.today()).count()
        pending_appointments = appointments.filter(date__gt=date.today()).count()

        # Retrieve the latest appointments
        latest_appointments = appointments.order_by('-date', '-time')

        # Add pagination to latest_appointments
        appointments_per_page = 5
        paginator = Paginator(latest_appointments, appointments_per_page)
        page = request.GET.get('page')
        latest_appointments_paginated = paginator.get_page(page)

        context = {
            'total_appointments': total_appointments,
            'upcoming_appointments': upcoming_appointments,
            'pending_appointments': pending_appointments,
            'latest_appointments': latest_appointments_paginated,  # Pass the paginated latest_appointments to the context
        }

        return render(request, 'book/dashboard.html', context)


class ChooseSubscriptionView(LoginRequiredMixin, View):
    template_name = 'book/choose_subscription.html'

    def get(self, request, client_id):
        return render(request, self.template_name, {'client_id': client_id})

    def post(self, request, client_id):
        # Redirect to the payment page
        return redirect('book:payment')




class PaymentCancelView(View):
    def get(self, request):
        return render(request, 'book/payment_cancel.html')
    
class ExecutePaymentView(View):
    def get(self, request, *args, **kwargs):
        # Set up your PayPal SDK configuration
        payment_id = request.GET.get('paymentId')
        payer_id = request.GET.get('PayerID')

        if payment_id and payer_id:
            payment = paypalrestsdk.Payment.find(payment_id)

            if payment.execute({"payer_id": payer_id}):
                print("Payment executed successfully")
                # Save payment information to your database and display a success message
                # ...
            else:
                print(payment.error)
                # Handle errors and display an error message to the user
                # ...

        return render(request, 'payment_success.html')  # Render a template for successful payment

 
@method_decorator(csrf_exempt, name='dispatch')
class WebhookListenerView(View):
    def post(self, request, *args, **kwargs):
        # Process the webhook event, update your records, and send a response
        return HttpResponse(status=200)

    def get(self, request, *args, **kwargs):
        return HttpResponse(status=405)  # Method not allowed
    


class InitiatePaymentView(View):
    template_name = 'book/initiate_payment.html'

    def get(self, request, *args, **kwargs):
        # get the client 
        client = Client.objects.get(user=request.user)
        # get subscription prices for the client's country
        subscription_prices = SubscriptionPrice.objects.filter(country=client.country)
        context = {'subscription_prices': subscription_prices}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # Set up your PayPal SDK configuration
        paypalrestsdk.configure({
            "mode": "sandbox",  # sandbox or live
            "client_id": settings.PAYPAL_CLIENT_ID,
            "client_secret": settings.PAYPAL_CLIENT_SECRET
        })

        # Get subscription details from the form
        subscription_id = request.POST.get("subscription_type")
        client = Client.objects.get(user=request.user)
        subscription_price = SubscriptionPrice.objects.get(subscription__id=subscription_id, country=client.country)

        # Store subscription_id in the session
        request.session['subscription_id'] = subscription_id

        # Create the payment object
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": request.build_absolute_uri(reverse('book:payment_success', kwargs={'subscription_id': subscription_id})),
                "cancel_url": request.build_absolute_uri(reverse('book:payment_cancel')),
            },

            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": subscription_price.subscription.name,
                        "sku": subscription_price.subscription.id,
                        "price": str(subscription_price.price),
                        "currency": "USD",
                        "quantity": 1
                    }]
                },
                "amount": {
                    "total": str(subscription_price.price),
                    "currency": "USD"
                },
                "description": subscription_price.subscription.description
            }]
        })

        # Create the payment and redirect the user to PayPal
        if payment.create():
            print("Payment created successfully")
            for link in payment.links:
                if link.rel == "approval_url":
                    approval_url = link.href
                    return redirect(approval_url)
        else:
            print(payment.error)
            # Handle errors and display an error message to the user
            # ...

        return redirect('/')  # Redirect to another page if there's an error


class PaymentSuccessView(View):
    def get(self, request, *args, **kwargs):
        # Update the user's records based on the subscription_id
        client = request.user.client
        subscription_id = request.session.get('subscription_id')
        print("Subscription ID:", subscription_id)

        # Fetch the Subscription instance with the given subscription_id
        subscription = Subscription.objects.get(id=subscription_id)

        # Check for the user's existing active subscription
        existing_subscription = UserSubscription.objects.filter(client=client, active=True).first()

        # Calculate start_date and end_date
        if existing_subscription:
            start_date = existing_subscription.end_date + timedelta(days=1)
        else:
            start_date = datetime.now().date()

        end_date = start_date + timedelta(days=30)

        # Create or update the user's subscription
        user_subscription, created = UserSubscription.objects.update_or_create(
            client=client,
            subscription=subscription,
            defaults={'start_date': start_date, 'end_date': end_date, 'active': True}
        )

        # Display a success message
        return render(request, 'book/success.html')
 
stripe.api_key = settings.STRIPE_SECRET_KEY

class StripePaymentView(View):
    template_name = "book/stripe_payment.html"

    def get(self, request, *args, **kwargs):
        context = {
            'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        token = request.POST.get('stripeToken')
        amount = 1000  # Amount in cents, for example: $10

        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency="usd",
                source=token,
                description="Stripe payment example",
            )
            return redirect('payments:payment_success')
        except stripe.error.CardError as e:
            # Handle card errors, such as insufficient funds or expired card
            return redirect('book:payment_failure')

        return redirect('/')

def payment_success(request):
    return render(request, 'book/payment_success.html')

def payment_failure(request):
    return render(request, 'book/payment_failure.html')

class StripeSubscriptionPaymentView(View):
    def post(self, request):
        # Get subscription details from the form
        subscription_id = request.POST.get("subscription_type")
        subscription = Subscription.objects.get(id=subscription_id)

        # Render the Stripe payment page with the selected subscription
        return render(request, 'stripe_payment.html', {'subscription': subscription})

class BusinessesView(ListView):
    model = Client
    template_name = 'book/businesses.html'
    context_object_name = 'clients'

    def get_queryset(self):
        service_id = self.kwargs['service_id']
        return Client.objects.filter(service__id=service_id)
    
class ServicesView(ListView):
    model = Service
    template_name = 'book/services.html'
    context_object_name = 'services'

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        if search_query:
            return Service.objects.filter(name__icontains=search_query)
        else:
            return Service.objects.all()

class BookingConfirmationView(LoginRequiredMixin, View):
    def get(self, request, appointment_id):
        appointment = get_object_or_404(Appointment, pk=appointment_id)
        deposit_required = appointment.service.deposit_required
        deposit_amount = appointment.service.deposit_amount

        return render(request, 'book/booking_confirmation.html', {'appointment': appointment, 'deposit_required': deposit_required, 'deposit_amount': deposit_amount})

class BookingSuccessView(View):
    def get(self, request):
        return render(request, 'book/booking_success.html')


# views.py
class ClientServiceView(View):
    def get(self, request, username):
        client = get_object_or_404(Client, user__username=username)
        service_types = ServiceType.objects.filter(service__client=client)
        service_images = ServiceImage.objects.filter(service_type__in=service_types)[:10]  # Fetch the first 10 service images
        return render(request, 'book/client_services.html', {'client': client, 'service_types': service_types, 'service_images': service_images})

class ClientBookingView(ActiveClientRequiredMixin, View):
    def get(self, request, username):
        client = get_object_or_404(Client, user__username=username)
        appointments = Appointment.objects.filter(service__client=client)  # Fetch appointments related to the client

        # Check if the client's subscription has expired
        if client.disabled:
            return HttpResponseForbidden("This client's subscription has expired. You cannot book appointments with them.")

        # Get the first available service for the client
        first_service = Service.objects.filter(client=client).first()
        if first_service:
            time_slots = AvailableTimeSlot.objects.filter(service=first_service, is_booked=False)
            form = AppointmentForm(time_slots=time_slots, client=client)
        else:
            form = AppointmentForm(client=client)

        return render(request, 'book/client_booking.html', {'form': form, 'client': client, 'appointments': appointments})

    def post(self, request, username):
        client = get_object_or_404(Client, user__username=username)
        
         # Check if the client's subscription has expired
        if client.disabled:
            return HttpResponseForbidden("This client's subscription has expired. You cannot book appointments with them.")
        
        first_service = Service.objects.filter(client=client).first()
        if first_service:
            time_slots = AvailableTimeSlot.objects.filter(service=first_service, is_booked=False)
        else:
            time_slots = AvailableTimeSlot.objects.none()
        
        
        form = AppointmentForm(request.POST, time_slots=time_slots, client=client)  # Add client=client here
        if form.is_valid():
            service_id = form.cleaned_data['service'].id
            try:
                service = Service.objects.get(id=service_id, client=client)
            except Service.DoesNotExist:
                messages.error(request, "The selected service does not exist.")
                return render(request, 'book/client_booking.html', {'form': form, 'client': client})

            appointment = form.save(commit=False)
            appointment.service = service

            # Use the existing customer or create a new one
            customer = Customer.objects.filter(user__email=form.cleaned_data['email']).first()
            if not customer:
                user = User.objects.create(username=form.cleaned_data['email'], email=form.cleaned_data['email'], first_name=form.cleaned_data['name'])
                customer = Customer.objects.create(user=user, phone_number=form.cleaned_data['phone_number'])
            
            appointment.customer = customer
            appointment.time_slot = form.cleaned_data['time_slot']
            appointment.time = form.cleaned_data['time_slot'].time  # Add thi
            appointment.save()
      
            

            # Mark the time slot as booked
            time_slot = form.cleaned_data['time_slot']
            time_slot.is_booked = True
            time_slot.save()

            # Send email to the client and the customer
            client_email = appointment.service.client.contact_email
            customer_email = appointment.customer.user.email
            subject = 'Appointment Booking Confirmation'

            client = appointment.service.client
            service = appointment.service
            date_str = appointment.date.strftime("%B %d, %Y")
            time_str = appointment.time.strftime("%I:%M %p")

            subject = "Appointment Confirmation"
            message = f"Hello,\n\n"\
                    f"Your appointment for {service.name} has been booked!\n"\
                    f"\n"\
                    f"Appointment Details:\n"\
                    f"Date: {date_str}\n"\
                    f"Time: {time_str}\n"\
                    f"Service: {service.name}\n"\
                    f"\n"\
                    f"Business Information:\n"\
                    f"Name: {client.business_name}\n"\
                    f"Email: {client.contact_email}\n"\
                    f"Phone: {client.contact_phone}\n"\
                    f"\n"\
                    f"Thank you for using our service."

            send_mail(subject, message, 'noreply@example.com', [client_email, customer_email], fail_silently=False)

            return redirect('book:booking_confirmation', appointment_id=appointment.pk)


class ClientCustomersView(View):
    def get(self, request, username):
        user = User.objects.get(username=username)
        client = Client.objects.get(user=user)
        appointments = Appointment.objects.filter(service__client=client)
        customers = set(appointment.customer for appointment in appointments)

        # Add pagination to customers
        customers_per_page = 5
        paginator = Paginator(list(customers), customers_per_page)
        page = request.GET.get('page')
        customers_paginated = paginator.get_page(page)

        context = {
            'customers': customers_paginated,
        }

        return render(request, 'book/client_customers.html', context)

class ClientSettingsView(View):
    def get(self, request, username):
        user = User.objects.get(username=username)
        client = Client.objects.get(user=user)
        settings_form = ClientSettingsForm(instance=client)
        service_form = ServiceForm()
        service_type_form = ServiceTypeForm(client=client) 
        service_image_form = ServiceImageForm(client=client)
        service_images = ServiceImage.objects.filter(service_type__service__client=client)  # Update service images queryset

        # Filter ServiceType queryset based on the associated client
        service_types = ServiceType.objects.filter(service__client=client)
        
        return render(request, 'book/client_settings.html', {
            'settings_form': settings_form,
            'service_form': service_form,
            'service_type_form': service_type_form,
            'service_image_form': service_image_form,
            'service_images': service_images,  # Pass service images to context
            'service_types': service_types  # Pass filtered ServiceType queryset to context
            
        })

    def post(self, request, username):
        user = User.objects.get(username=username)
        client = Client.objects.get(user=user)
        settings_form = ClientSettingsForm(request.POST, instance=client)
        service_form = ServiceForm(request.POST)
        service_type_form = ServiceTypeForm(request.POST, client=client)
        service_image_form = ServiceImageForm(request.POST, request.FILES, client=client)

        if settings_form.is_valid():
            settings_form.save()

        has_existing_service = Service.objects.filter(client=client).exists()
        service_form_is_valid = service_form.is_valid()

        if has_existing_service:
            messages.error(request, "Sorry, you can't create a second service. Please contact the admin.")
        elif service_form_is_valid:
            new_service = service_form.save(commit=False)
            new_service.client = client
            new_service.save()

        if service_type_form.is_valid():
            new_service_type = service_type_form.save(commit=False)
            if has_existing_service:
                existing_service = Service.objects.get(client=client)
                new_service_type.service = existing_service
            elif not has_existing_service and service_form_is_valid:
                new_service_type.service = new_service
            new_service_type.save()

        if service_image_form.is_valid():
            new_service_image = service_image_form.save(commit=False)
            service_type_id = request.POST.get('service_type')
            service_type = ServiceType.objects.get(id=service_type_id)
            new_service_image.service_type = service_type
            new_service_image.save()

        return redirect('book:client_settings', username=username)


class UpdateServiceImageView(View):
    def get(self, request, service_image_id):
        service_image = get_object_or_404(ServiceImage, id=service_image_id)
        client = request.user.client
        form = ServiceImageForm(instance=service_image, client=client)
        return render(request, 'book/update_service_image.html', {'form': form, 'service_image': service_image})

    def post(self, request, service_image_id):
        service_image = get_object_or_404(ServiceImage, id=service_image_id)
        client = request.user.client
        form = ServiceImageForm(request.POST, request.FILES, instance=service_image, client=client)
        if form.is_valid():
            form.save()
            return redirect('book:client_settings', username=request.user.username)
        return render(request, 'book/update_service_image.html', {'form': form, 'service_image': service_image})


class DeleteServiceImageView(View):
    def post(self, request, service_image_id):
        service_image = get_object_or_404(ServiceImage, id=service_image_id)
        service_image.delete()
        return redirect('book:client_settings', username=request.user.username)


class ClientReportsView(View):
    def get(self, request, username):
        user = User.objects.get(username=username)
        client = Client.objects.get(user=user)
        appointments = Appointment.objects.filter(service__client=client)

        # Add pagination to appointments
        appointments_per_page = 5
        paginator = Paginator(appointments, appointments_per_page)
        page = request.GET.get('page')
        appointments_paginated = paginator.get_page(page)

        context = {
            'appointments': appointments_paginated,
        }

        return render(request, 'book/client_reports.html', context)


class PricingView(TemplateView):
    template_name = 'book/pricing.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plans'] = [
            {
                'name': 'Regular',
                'price': '$5',
                'features': ['Register', 'Appointment - Emailed']
            },
            {
                'name': 'Premium',
                'price': '$10',
                'features': ['Register', 'Appointment - Emailed', 'Customer data saved', 'Client Dashboard']
            },
            {
                'name': 'Xtra',
                'price': '$20',
                'features': ['Register', 'Appointment - Emailed', 'Customer data saved', 'Client Dashboard', 'Customers page', 'Customers Login', 'Adverts of service', 'And many more...']
            },
        ]
        return context


class PaymentView(View):
    def get(self, request, appointment_id):
        appointment = get_object_or_404(Appointment, pk=appointment_id)
        return render(request, 'book/payment.html', {'appointment': appointment})

    def post(self, request, appointment_id):
        appointment = get_object_or_404(Appointment, pk=appointment_id)
        stripe.api_key = settings.STRIPE_SECRET_KEY

        # Get the Stripe token from the submitted form data
        stripe_token = request.POST.get('stripeToken')

        try:
            # Create a charge using the token and the appointment's deposit amount
            charge = stripe.Charge.create(
                amount=int(appointment.deposit_amount * 100),  # Convert to cents
                currency='usd',
                source=stripe_token,
                description=f"Payment for appointment {appointment_id}",
            )

            # If the payment is successful, update the appointment as paid
            if charge.status == "succeeded":
                appointment.paid = True
                appointment.save()
                return redirect('success_url')
            else:
                return JsonResponse({"error": "Payment failed."})

        except stripe.error.StripeError as e:
            # Handle Stripe errors
            return JsonResponse({"error": str(e)})



class SubscriptionPaymentView(View):
    def get(self, request):
        return render(request, 'book/subscription_payment.html')
 
# views.py
class SuccessView(View):
    def get(self, request):
        return render(request, 'book/success.html')


class CancelView(View):
    def get(self, request):
        return render(request, 'book/cancel.html')

class ContactView(View):
    def get(self, request):
        return render(request, 'book/contact.html')

def send_email(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        send_mail(
            subject,
            message,
            email,
            ['krissbajo@gmail.com'],  # Replace 'EMAIL_HOST_USER' with your email host user
            fail_silently=False,
        )
        return HttpResponseRedirect(reverse('book:contact_success'))

    return HttpResponseRedirect(reverse('book:contact'))



class ContactSuccessView(View):
    def get(self, request):
        return render(request, 'book/contactussuccess.html')


class FeaturesView(View):
    def get(self, request):
        return render(request, 'book/features.html')


class ClientCalendarView(View):
    template_name = 'book/client_calendar.html'

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return self.get_available_slots()
        return render(request, self.template_name)

    def get_available_slots(self):
        appointments = Appointment.objects.filter(status="pending")

        events = []

        for appointment in appointments:
            start_time = datetime.combine(appointment.date, appointment.time)
            end_time = start_time + timedelta(minutes=30)  # Adjust the duration of the appointment if necessary
            events.append({
                "title": f"Appointment: {appointment.customer}",
                "start": start_time.isoformat(),
                "end": end_time.isoformat(),
                "appointment_id": appointment.id,
            })

        return JsonResponse(events, safe=False)

# In views.py
class GetAppointmentDetailsView(View):
    def get(self, request, *args, **kwargs):
        appointment_id = request.GET.get('appointment_id', None)
        appointment = get_object_or_404(Appointment, id=appointment_id)
        details = f"Client: {appointment.customer}, Time: {appointment.time}"
        return JsonResponse({'details': details}, safe=False)


class AppointmentAPIView(View):
    def get(self, request, *args, **kwargs):
        appointments = Appointment.objects.filter(status='pending')
        events = []

        for appointment in appointments:
            events.append({
                'start': f'{appointment.date}T{appointment.time}',
                'end': f'{appointment.date}T{appointment.time}',
            })

        return JsonResponse(events, safe=False)


class CalendarBookingView(View):
    def post(self, request, *args, **kwargs):
        # Handle booking submission and update the database
        # ...

        return JsonResponse({'status': 'success'}, status=200)


class EditAppointmentView(View):
    def get(self, request, pk, *args, **kwargs):
        appointment = get_object_or_404(Appointment, pk=pk)
        form = EditAppointmentForm(instance=appointment)
        return render(request, 'book/edit_appointment.html', {'form': form, 'appointment': appointment})

    def post(self, request, pk, *args, **kwargs):
        appointment = get_object_or_404(Appointment, pk=pk)
        form = EditAppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('book:appointment_detail', pk=appointment.pk)
        return render(request, 'book/edit_appointment.html', {'form': form, 'appointment': appointment})


class AppointmentDetailView(DetailView):
    model = Appointment
    template_name = 'book/appointment_detail.html'


@method_decorator(login_required, name='dispatch')
class NotesView(View):
    def get(self, request, *args, **kwargs):
        notes = Note.objects.filter(user=request.user)
        return render(request, 'book/notes.html', {'notes': notes})

@method_decorator(login_required, name='dispatch')
class AddNoteView(View):
    def get(self, request, *args, **kwargs):
        form = NoteForm()
        return render(request, 'book/add_note.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('book:notes')
        return render(request, 'book/add_note.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class EditNoteView(View):
    def get(self, request, note_id, *args, **kwargs):
        note = get_object_or_404(Note, pk=note_id, user=request.user)
        form = NoteForm(instance=note)
        return render(request, 'book/edit_note.html', {'form': form, 'note': note})

    def post(self, request, note_id, *args, **kwargs):
        note = get_object_or_404(Note, pk=note_id, user=request.user)
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('book:notes')
        return render(request, 'book/edit_note.html', {'form': form, 'note': note})


@method_decorator(login_required, name='dispatch')
class DeleteNoteView(View):
    def get(self, request, note_id, *args, **kwargs):
        note = get_object_or_404(Note, pk=note_id, user=request.user)
        note.delete()
        return redirect('book:notes')


class EasySchedulingView(TemplateView):
    template_name = 'book/easy_scheduling.html'


class MobileFriendlyView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'book/mobile_friendly.html')

from django.shortcuts import render

class SecurePlatformView(TemplateView):
    template_name = "book/secure_platform.html"

class AvailableSlotsView(View):
    def get(self, request, *args, **kwargs):
        date_str = request.GET.get('date')
        service_id = request.GET.get('service_id')

        if not date_str or not service_id:
            return JsonResponse({'error': 'Invalid request'}, status=400)

        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        service = get_object_or_404(Service, pk=service_id)

        available_slots = AvailableTimeSlot.objects.filter(
            date=date,
            service=service,
            is_booked=False
        )

        response_data = {
            'available_slots': [
                {'id': slot.id, 'time': slot.time.strftime('%H:%M')}
                for slot in available_slots
            ]
        }

        return JsonResponse(response_data)


class UpdateTimeSlotsView(View):
    def get(self, request):
        service_id = request.GET.get('service_id', None)
        date_str = request.GET.get('date', None)

        if service_id and date_str:
            service = get_object_or_404(Service, id=service_id)
            date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
            time_slots = AvailableTimeSlot.objects.filter(service=service, date=date)
            time_slot_data = [{'id': time_slot.id, 'time': time_slot.time.strftime('%H:%M')} for time_slot in time_slots]
            return JsonResponse({'time_slots': time_slot_data})
        else:
            return JsonResponse({'time_slots': []})

class TimeSlotCreateView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = AvailableTimeSlotForm(client=request.user.client)
        context = {
            'form': form,
        }
        return render(request, 'book/time_slot_form.html', context)

    def post(self, request, *args, **kwargs):
        form = AvailableTimeSlotForm(request.POST, client=request.user.client)

        if form.is_valid():
            auto_generate = form.cleaned_data.get('auto_generate', False)

            if auto_generate:
                start_date = form.cleaned_data['date'] or timezone.now().date()
                weeks = form.cleaned_data['weeks']
                service_duration = form.cleaned_data['service'].duration
                working_hours_start = self.request.user.client.working_hours_start
                working_hours_end = self.request.user.client.working_hours_end
                working_days = self.request.user.client.working_days

                
                for i in range(weeks * 7):
                    current_date = start_date + timedelta(days=i)
                    current_day = current_date.strftime('%a').lower()

                    if current_day in [day[0] for day in working_days]:
                        current_datetime = datetime.combine(current_date, working_hours_start)
                        current_time = current_datetime.time()

                        while (current_datetime + service_duration).time() <= working_hours_end:
                            time_slot = AvailableTimeSlot(
                                client=self.request.user.client,
                                service=form.cleaned_data['service'],
                                date=current_date,
                                time=current_time
                            )
                            time_slot.save()
                            current_datetime += service_duration
                            current_time = current_datetime.time()

                return HttpResponseRedirect('/time_slots/')

            else:
                time_slot = form.save(commit=False)
                time_slot.client = request.user.client
                time_slot.save()
                return HttpResponseRedirect('/time_slots/')

        context = {
            'form': form,
        }
        return render(request, 'book/time_slot_form.html', context)


def generate_time_slots(working_days, start_time, end_time, service_duration):
    time_slots = []
    today = timezone.localdate()

    # Generate time slots for the next 30 days
    for day_offset in range(1, 31):
        current_date = today + timezone.timedelta(days=day_offset)
        day_of_week = current_date.strftime("%a").lower()

        if day_of_week in working_days:
            current_time = start_time

            while current_time + service_duration <= end_time:
                time_slots.append((current_date, current_time))

                # Add service_duration to current_time
                current_datetime = datetime.combine(current_date, current_time)
                updated_datetime = current_datetime + service_duration
                current_time = updated_datetime.time()

    return time_slots


class TimeSlotsListView(LoginRequiredMixin, ListView):
    model = AvailableTimeSlot
    template_name = 'book/time_slots_list.html'
    context_object_name = 'time_slots'
    paginate_by = 7

    def get_queryset(self):
        # Filter time slots based on the logged-in user's client and order by date and time
        queryset = super().get_queryset()
        return queryset.filter(client=self.request.user.client).order_by('date', 'time')


class TimeSlotUpdateView(LoginRequiredMixin, UpdateView):
    model = AvailableTimeSlot
    form_class = AvailableTimeSlotForm
    template_name = 'book/time_slot_form.html'
    success_url = '/time_slots/'

    def get_queryset(self):
        # Filter time slots based on the logged-in user's client
        queryset = super().get_queryset()
        return queryset.filter(client=self.request.user.client)

class TimeSlotDeleteView(LoginRequiredMixin, DeleteView):
    model = AvailableTimeSlot
    template_name = 'book/time_slot_confirm_delete.html'
    success_url = '/time_slots/'

    def get_queryset(self):
        # Filter time slots based on the logged-in user's client
        queryset = super().get_queryset()
        return queryset.filter(client=self.request.user.client)
    


class TimeSlotDeleteAll(View):
    def post(self, request):
        AvailableTimeSlot.objects.all().delete()
        return redirect('book:time_slots_list')

from django.contrib.auth.mixins import LoginRequiredMixin

from django.db.models import Avg

class ServiceReviewsView(View):
    def get(self, request, service_id):
        service = get_object_or_404(Service, id=service_id)
        reviews = Review.objects.filter(service=service, published=True)
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
        return render(request, 'book/service_reviews.html', {'reviews': reviews, 'avg_rating': avg_rating})


    
class ClientReviewManagementView(LoginRequiredMixin, View):
    def get(self, request):
        client = request.user.client
        reviews = Review.objects.filter(service__client=client)
        return render(request, 'book/client_review_management.html', {'reviews': reviews})

from django.views import View
from .models import Service

from django.contrib import messages

from django.contrib import messages

class AddReviewView(LoginRequiredMixin, View):
    def get(self, request, service_id):
        service = get_object_or_404(Service, id=service_id)
        completed_appointments = service.appointment_set.filter(status='completed', customer__user=request.user)

        if not completed_appointments.exists():
            messages.error(request, 'You can only review services with completed appointments.')
            return redirect('book:customer_dashboard')

        # Check if the user has already reviewed this service
        existing_review = service.review_set.filter(user=request.user)
        if existing_review.exists():
            messages.error(request, 'You have already reviewed this service.')
            return redirect('book:customer_dashboard')

        form = ReviewForm()
        return render(request, 'book/add_review.html', {'form': form, 'service': service})

    def post(self, request, service_id):
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.service = get_object_or_404(Service, id=service_id)
            review.save()
            return redirect('book:customer_dashboard') # Redirect to the customer dashboard or any other suitable page
        return render(request, 'book/add_review.html', {'form': form})

from django.views.decorators.http import require_POST

@require_POST
def publish_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, service__client=request.user.client)
    review.published = True
    review.save()
    return redirect('book:client_review_management')

class CustomerRegistrationView(View):
    template_name = 'book/customer_registration.html'
    
    def get(self, request):
        form = CustomerRegistrationForm()  # Create a separate form for customers
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)  # Use the customer registration form
        if form.is_valid():
            customer = form.save()
            messages.success(request, f'Account created for {customer.user.username}!')
            return redirect('book:login')  # Redirect to the appropriate login or dashboard
        return render(request, self.template_name, {'form': form})


class LoginView(AuthLoginView):
    form_class = AuthenticationForm
    template_name = 'book/login.html'
    
    def form_valid(self, form):
        """Security check complete. Log the user in."""
        login(self.request, form.get_user())

        # Check if the user is a client
        if Client.objects.filter(user=self.request.user).exists():
            return redirect('book:dashboard')  # Redirect to the client dashboard
        else:
            return redirect('book:customer_dashboard')  # Redirect to the customer dashboard
        
    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)

class CustomerDashboardView(LoginRequiredMixin, View):
    template_name = 'book/customer_dashboard.html'

    def get(self, request):
        form = DashboardAppointmentForm()

        # Get the current customer
        current_customer = Customer.objects.get(user=request.user)

        # Get all available clients
        clients = Client.objects.all()

        # Get all services and their related clients
        client_service_mapping = {client.id: [service for service in Service.objects.filter(client=client)] for client in clients}

        # Get all appointments related to the current customer
        appointments = Appointment.objects.filter(customer=current_customer).order_by('-date', '-time')

        def handle_serialization(obj):
            if isinstance(obj, timedelta):
                return str(obj)
            if isinstance(obj, Decimal):
                return float(obj)
            return obj.__dict__

        client_service_mapping_json = json.dumps(client_service_mapping, default=handle_serialization)
        clients_json = serializers.serialize('json', clients)

        # Add the current customer's information to the form
        form.fields['name'].initial = request.user.first_name
        form.fields['email'].initial = request.user.email
        form.fields['phone_number'].initial = current_customer.phone_number

        # Set the form fields as read-only for customers
        form.fields['name'].widget.attrs['readonly'] = True
        form.fields['email'].widget.attrs['readonly'] = True
        form.fields['phone_number'].widget.attrs['readonly'] = True

        context = {
            'form': form,
            'clients': clients,
            'client_service_mapping': client_service_mapping_json,
            'appointments': appointments,
            'clients_json': clients_json,
        }
        return render(request, self.template_name, context)


class LandingView(View):
    def get(self, request):
        return render(request, 'book/landing.html')


from django.shortcuts import render

def test_checkboxes(request):
    form = ClientRegistrationForm()
    return render(request, 'book/test_checkboxes.html', {'form': form})


def subscribe_newsletter(request):
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            new_subscriber = form.save()
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "error", "errors": form.errors})
    else:
        form = NewsletterSubscriptionForm()

    return render(request, 'book/index.html', {'form': form})


class SendNewsletterView(View):
    def get(self, request):
        form = SendNewsletterForm()
        return render(request, 'book/send_newsletter.html', {'form': form})

    def post(self, request):
        form = SendNewsletterForm(request.POST)
        if form.is_valid():
            newsletter_content = form.save(commit=False)  # Do not save the instance to the database
            subject = newsletter_content.subject
            message = form.cleaned_data['message']  # Get the cleaned message content
            self.send_newsletter_email(subject, message)
            messages.success(request, 'Newsletter sent successfully!')
            return redirect('book:send_newsletter')
        return render(request, 'book/send_newsletter.html', {'form': form})

    def send_newsletter_email(self, subject, message):
        subscribers = NewsletterSubscriber.objects.all()
        recipient_list = [subscriber.email for subscriber in subscribers]

        from_email = settings.EMAIL_HOST_USER

        html_content = render_to_string('book/email_template.html', {'message': message})
        text_content = strip_tags(html_content)

        for recipient in recipient_list:
            msg = EmailMultiAlternatives(subject, text_content, from_email, [recipient])
            msg.attach_alternative(html_content, "text/html")
            msg.send()


class NewsletterSuccessView(TemplateView):
    template_name = 'book/newsletter_success.html'




# Your other views and imports

class DisabledClientView(View):
    def get(self, request):
        return render(request, 'book/disabled_client.html')



class ItIndexView(TemplateView):
    template_name = 'book/it_index.html'


class CustomPasswordResetView(PasswordResetView):
    template_name = 'book/password_reset.html'
    email_template_name = 'book/password_reset_email.html'
    extra_email_context = {'custom_password_reset_confirm': 'custom_password_reset_confirm'}
    success_url = reverse_lazy('book:custom_password_reset_done')  # Add this line

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'book/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'book/password_reset_confirm.html'

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'book/password_reset_complete.html'
    


def export_appointments(request):
    appointment_resource = AppointmentResource()
    dataset = appointment_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="appointments.xls"'
    return response




class CreateCategoryView(CreateView):
    model = Category
    form_class = CategoryCreationForm
    template_name = 'book/create_category.html'
    success_url = reverse_lazy('success_page')  # Replace 'success_page' with the URL name of your success page

    def form_valid(self, form):
        new_category = form.save(commit=False)
        new_category.enabled = False
        new_category.save()

        # Send an email to the site admin
        send_mail(
            'New category created',
            f'A new category has been created: {new_category.name}. Please review it.',
            'noreply@yourdomain.com',
            ['admin@yourdomain.com'],
            fail_silently=False,
        )
        
        return super().form_valid(form)

class ClientSearchView(generic.ListView):
    model = Client
    template_name = 'book/search_results.html'
    context_object_name = 'clients'
    
    def get_queryset(self):
        category = self.request.GET.get('category', '')
        country = self.request.GET.get('country', '')
        state = self.request.GET.get('state', '')
        city = self.request.GET.get('city', '')

        queryset = Client.objects.all()

        if category:
            queryset = queryset.filter(category__id=category)
            
        if country:
            queryset = queryset.filter(country__icontains=country)
            
        if state:
            queryset = queryset.filter(state__icontains=state)
            
        if city:
            queryset = queryset.filter(city__icontains=city)

        return queryset.distinct()


def autocomplete(request):
    query = request.GET.get('term', '')
    categories = Category.objects.filter(name__icontains=query, enabled=True)[:10]
    results = [{'id': category.id, 'value': category.name} for category in categories]
    return JsonResponse(results, safe=False)




class ClientSearchByNameView(generic.ListView):
    model = Client
    template_name = 'book/client_search_by_name_results.html'
    context_object_name = 'clients'

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        country_query = self.request.GET.get('country', '')
        state_query = self.request.GET.get('state', '')
        city_query = self.request.GET.get('city', '')
        
        filters = Q(business_name__icontains=search_query)
        
        if country_query:
            filters &= Q(country__icontains=country_query)
        if state_query:
            filters &= Q(state__icontains=state_query)
        if city_query:
            filters &= Q(city__icontains=city_query)

        queryset = Client.objects.filter(filters) if any([search_query, country_query, state_query, city_query]) else Client.objects.none()

        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clients = self.get_queryset()

        # Check if queryset is empty
        if not clients:
            context['message'] = 'No clients found matching your search criteria. Please modify your search and try again.'
            return context

        avg_ratings = {}
        client_details = {}

        for client in clients:
            total_rating = 0
            count = 0

            # Check if the client has a related Service object
            if hasattr(client, 'service'):
                service = client.service  # Access the related Service object directly

                for review in service.review_set.all():
                    total_rating += review.rating
                    count += 1

                avg_ratings[client.id] = total_rating / count if count > 0 else 0

                # Fetch city, state, and country for each client
                client_details[client.id] = {
                    'city': client.city,
                    'state': client.state,
                    'country': client.country,
                }

        context['avg_ratings'] = avg_ratings
        context['client_details'] = client_details

        return context



@method_decorator(csrf_exempt, name='dispatch')
class ServiceTypeApiView(View):
    def get(self, request):
        service_id = request.GET.get('service_id')

        if service_id is not None:
            service_types = ServiceType.objects.filter(service__id=service_id)
            service_types_data = [
                {
                    'id': service_type.id,
                    'name': service_type.name,
                } for service_type in service_types
            ]
            return JsonResponse(service_types_data, safe=False, status=200)

        return JsonResponse({'error': 'Missing service_id'}, status=400)



class FAQView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'book/faq.html')
