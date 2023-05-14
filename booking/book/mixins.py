from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Client

class ActiveClientRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        if not self.request.user.is_authenticated:  # Add this line
            return True  # User is not authenticated, so no restriction should be applied

        try:
            client = Client.objects.get(user=self.request.user)
            return not client.disabled
        except Client.DoesNotExist:
            return True  # User is not a client, so no restriction should be applied

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse('book:disabled_client'))
