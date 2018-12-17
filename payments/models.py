from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import JSONField


class Subscription(models.Model):

    STATE_ACTIVE = 0
    STATE_CANCELLED = 1
    STATE_PAUSED = 2

    STATE_CHOICES = (
        (STATE_ACTIVE, 'Active'),
        (STATE_CANCELLED, 'Cancelled'),
        (STATE_PAUSED, 'Paused'),
    )

    # Stripe Charge
    stripe_payment_token = models.CharField(
        max_length=32, null=True, blank=True)
    stripe_subscription_id = models.CharField(
        max_length=64, null=True, blank=True)
    stripe_customer_id = models.CharField(max_length=32, null=True, blank=True)

    state = models.PositiveSmallIntegerField(
        choices=STATE_CHOICES, default=STATE_ACTIVE)

    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
