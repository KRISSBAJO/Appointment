from django.utils import timezone
from .models import Client

def disable_expired_clients():
    expired_clients = Client.objects.filter(trial_end_date__lte=timezone.now(), disabled=False)
    expired_clients.update(disabled=True)
