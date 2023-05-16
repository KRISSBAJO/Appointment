from django.urls import path
from django.conf import settings

from book.forms import CustomerRegistrationForm

from django.contrib.auth.views import  LogoutView
from book.views import LoginView
from book import views
from book.views import InitiatePaymentView, PaymentSuccessView, WebhookListenerView
from book.views import FAQView



app_name = 'book'

urlpatterns = [

    path('', views.IndexView.as_view(), name='index'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='book:index'), name='logout'),
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.CustomPasswordResetDoneView.as_view(), name='custom_password_reset_done'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='custom_password_reset_confirm'),
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # ...

    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('choose_subscription/<int:client_id>/', views.ChooseSubscriptionView.as_view(), name='choose_subscription'),
    #path('bookings/<str:username>/', views.PublicBookingPageView.as_view(), name='public_booking_page'),
    path('services/', views.ServicesView.as_view(), name='services'),
    path('services/<int:service_id>/businesses/', views.BusinessesView.as_view(), name='businesses'),
    #path('booking/<str:username>/', views.BookingView.as_view(), name='booking'),
    path('booking_success/', views.BookingSuccessView.as_view(), name='booking_success'),
    path('client_services/<str:username>/', views.ClientServiceView.as_view(), name='client_services'),
    #path('<str:username>/booking/', views.ClientBookingView.as_view(), name='client_booking'),
    path('client_booking/<str:username>/', views.ClientBookingView.as_view(), name='client_booking'),
    path('client/customers/<str:username>/', views.ClientCustomersView.as_view(), name='client_customers'),
    path('client/reports/<str:username>/', views.ClientReportsView.as_view(), name='client_reports'),
    path('client/settings/<str:username>/', views.ClientSettingsView.as_view(), name='client_settings'),
    path('service_image/update/<int:service_image_id>/', views.UpdateServiceImageView.as_view(), name='update_service_image'),
    path('service_image/delete/<int:service_image_id>/', views.DeleteServiceImageView.as_view(), name='delete_service_image'),
    path('pricing/', views.PricingView.as_view(), name='pricing'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('payment/<int:appointment_id>/', views.PaymentView.as_view(), name='payment'),
    path('subscription_payment/', views.SubscriptionPaymentView.as_view(), name='subscription_payment'),
    path('success/', views.SuccessView.as_view(), name='success_url'),
    path('cancel/', views.CancelView.as_view(), name='cancel_url'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('send_email/', views.send_email, name='send_email'),
    path('contact_success/', views.ContactSuccessView.as_view(), name='contact_success'),
    path('features/', views.FeaturesView.as_view(), name='features'),
    
    path('client_calendar/', views.ClientCalendarView.as_view(), name='client_calendar'),
    path('api/appointments/', views.AppointmentAPIView.as_view(), name='api_appointments'),
    path('calendar/book/', views.CalendarBookingView.as_view(), name='calendar_book'),
    path('available_slots/<int:client_id>/', views.AvailableSlotsView.as_view(), name='available_slots'),
    path('get_appointment_details/', views.GetAppointmentDetailsView.as_view(), name='get_appointment_details'),
    path('booking_confirmation/<int:appointment_id>/', views.BookingConfirmationView.as_view(), name='booking_confirmation'),


    path('edit_appointment/<int:pk>/', views.EditAppointmentView.as_view(), name='edit_appointment'),
    path('appointment_detail/<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment_detail'),
    
    path('note', views.NotesView.as_view(), name='notes'),
    path('add/', views.AddNoteView.as_view(), name='add_note'),
    path('edit/<int:note_id>/', views.EditNoteView.as_view(), name='edit_note'),
    path('delete/<int:note_id>/', views.DeleteNoteView.as_view(), name='delete_note'),
    path('easy-scheduling/', views.EasySchedulingView.as_view(), name='easy_scheduling'),
    path('mobile-friendly/', views.MobileFriendlyView.as_view(), name='mobile_friendly'),
    path('secure-platform/', views.SecurePlatformView.as_view(), name='secure-platform'),
    
    path('time_slots/', views.TimeSlotsListView.as_view(), name='time_slots_list'),
    path('time_slots/add/', views.TimeSlotCreateView.as_view(), name='time_slot_create'),
    path('time_slots/<int:pk>/edit/', views.TimeSlotUpdateView.as_view(), name='time_slot_update'),
    path('time_slots/<int:pk>/delete/', views.TimeSlotDeleteView.as_view(), name='time_slot_delete'),
    path('time_slot_delete_all/', views.TimeSlotDeleteAll.as_view(), name='time_slot_delete_all'),
    path('api/available-slots/', views.AvailableSlotsView.as_view(), name='available_slots'),
    
    # URLS for Review
    path('services/<int:service_id>/add_review/', views.AddReviewView.as_view(), name='add_review'),
    path('service_reviews/<int:service_id>/', views.ServiceReviewsView.as_view(), name='service_reviews'),
    path('client_review_management/', views.ClientReviewManagementView.as_view(), name='client_review_management'),
    path('publish_review/<int:review_id>/', views.publish_review, name='publish_review'),
    
    
    path('register_customer/', views.CustomerRegistrationView.as_view(), name='register_customer'),
    path('customer_dashboard/', views.CustomerDashboardView.as_view(), name='customer_dashboard'),
    
    path('landing', views.LandingView.as_view(), name='landing'),
    path('test_checkboxes/', views.test_checkboxes, name='test_checkboxes'),
    
    
      
    path('subscribe_newsletter/', views.subscribe_newsletter, name='subscribe_newsletter'),
    path('disabled_client/', views.DisabledClientView.as_view(), name='disabled_client'),
    path('create_category/', views.CreateCategoryView.as_view(), name='create_category'),

   
    path('send_newsletter/', views.SendNewsletterView.as_view(), name='send_newsletter'),
    path('newsletter_success/', views.NewsletterSuccessView.as_view(), name='newsletter_success'),
    path('export_appointments/', views.export_appointments, name='export_appointments'),

    path('search_clients/', views.ClientSearchView.as_view(), name='search_clients'),
    path('search_clients_by_name/', views.ClientSearchByNameView.as_view(), name='client_search_by_name'),
    
    path("execute_payment/", views.ExecutePaymentView.as_view(), name="execute_payment"),
    path('webhook_listener/', WebhookListenerView.as_view(), name='webhook_listener'),
    path('payment_success/<int:subscription_id>/', views.PaymentSuccessView.as_view(), name='payment_success'),


     path('payment_cancelled/', views.PaymentCancelView.as_view(), name='payment_cancel'),
     path('initiate_payment/', InitiatePaymentView.as_view(), name='initiate_payment'),
     
     # Stripe 
    path('stripe_payment/', views.StripePaymentView.as_view(), name='stripe_payment'),
    #  path('payment_success/<int:subscription_id>/', views.payment_success, name='payment_success'),
    path('payment_failure/', views.payment_failure, name='payment_failure'),
    path('stripe_subscription_payment/', views.StripeSubscriptionPaymentView.as_view(), name='stripe_subscription_payment'),
    
     path('api/service-types/', views.ServiceTypeApiView.as_view(), name='get_service_types'),
     path('faq/', FAQView.as_view(), name='faq'),
   



    path('autocomplete/', views.autocomplete, name='autocomplete'),
    

    path('it_index', views.ItIndexView.as_view(), name='it_index'),

   
]
