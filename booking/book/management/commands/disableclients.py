from django.core.management.base import BaseCommand
from book.disable_expired_clients import disable_expired_clients
import schedule
import time

class Command(BaseCommand):
    help = "Disable expired clients"

    def handle(self, *args, **options):
        schedule.every().day.at("00:00").do(disable_expired_clients)

        while True:
            schedule.run_pending()
            time.sleep(1)
