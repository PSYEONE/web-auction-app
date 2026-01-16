from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from auction.models import Item


class Command(BaseCommand):
    help = 'Closes expired auctions and sends emails to winners'

    def handle(self, *args, **options):
        now = timezone.now()

        # 1. Find active items where the end_date has passed
        expired_items = Item.objects.filter(is_active=True, end_date__lte=now)

        if not expired_items.exists():
            self.stdout.write(self.style.SUCCESS('No expired auctions found.'))
            return

        for item in expired_items:
            # 2. Find the winner (highest bid)
            highest_bid = item.bids.order_by('-amount').first()

            if highest_bid:
                winner = highest_bid.bidder
                self.stdout.write(f"Closing item '{item.title}'. Winner: {winner.email}")

                # 3. Send the email
                try:
                    send_mail(
                        subject=f'You won the auction: {item.title}',
                        message=f'Congratulations! You had the highest bid of £{highest_bid.amount}. Please proceed '
                                f'to payment.',
                        from_email='your_group_email@gmail.com',  # Replace this later
                        recipient_list=[winner.email],
                        fail_silently=False,
                    )
                    self.stdout.write(self.style.SUCCESS(f"Email sent to {winner.email}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Failed to send email: {e}"))

            else:
                self.stdout.write(f"Item '{item.title}' expired with no bids.")

            # 4. Mark as inactive so we don't process it again
            item.is_active = False
            item.save()
