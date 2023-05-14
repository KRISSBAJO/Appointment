from django.contrib import admin
from .models import AvailableTimeSlot, Category, Client, Customer, NewsletterContent, NewsletterSubscriber, Note, ProfileImage, Review, Service, Appointment, ServiceImage, ServiceType, Subscription, SubscriptionPrice, UserSubscription

admin.site.register(Client)
admin.site.register(Customer)
admin.site.register(Service)
admin.site.register(Appointment) 
admin.site.register(ProfileImage) 
admin.site.register(ServiceImage)# 
admin.site.register(Note)
admin.site.register(UserSubscription) 
admin.site.register (Subscription)# 
admin.site.register(AvailableTimeSlot)# 
admin.site.register(Review)# 
admin.site.register(NewsletterSubscriber)# 
admin.site.register(NewsletterContent) #
admin.site.register(Category)# 
admin.site.register(ServiceType)# 
admin.site.register(SubscriptionPrice)

