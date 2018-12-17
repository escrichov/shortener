from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
import stripe
import json

from .models import Subscription


@login_required
def payment_cancel(request):

    try:
        subscription = Subscription.objects.get(user=request.user)
    except Subscription.DoesNotExist:
        return render(request, 'payments/payment_cancelled.html', context={})

    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_subscription = stripe.Subscription.retrieve(
        subscription.stripe_subscription_id)
    stripe_subscription.cancel_at_period_end = True
    stripe_subscription.save()

    subscription.state = Subscription.STATE_CANCELLED
    subscription.save(update_fields=['state'])

    return render(request, 'payments/payment_cancelled.html', context={})


@login_required
def payment_checkout(request):

    # Token is created using Checkout or Elements!
    # Get the payment token ID submitted by the form:
    payment_token = request.POST.get('stripeToken')
    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        subscription = Subscription.objects.get(user=request.user)
    except Subscription.DoesNotExist:
        subscription = None

    if subscription is None:
        customer = stripe.Customer.create(
            email=request.user,
            source=payment_token,
        )

        stripe_subscription = stripe.Subscription.create(
            customer=customer['id'],
            items=[{'plan': 'plan_E6ugdyKJuqMedj'}],
        )

        subscription = Subscription()
        subscription.stripe_payment_token = payment_token
        subscription.stripe_subscription_id = stripe_subscription['id']
        subscription.stripe_customer_id = customer['id']
        subscription.state = Subscription.STATE_ACTIVE
        subscription.user = request.user
        subscription.save()
    else:
        # Update payment token in customer
        customer = stripe.Customer.retrieve(subscription.stripe_customer_id)
        customer.source = payment_token
        customer.save()

        # Update stripe subscription
        stripe_subscription = stripe.Subscription.retrieve(
            subscription.stripe_subscription_id)
        if stripe_subscription:
            stripe_subscription.cancel_at_period_end = False
            stripe_subscription.save()
        else:
            stripe_subscription = stripe.Subscription.create(
                customer=customer['id'],
                items=[{'plan': 'plan_E6ugdyKJuqMedj'}],
            )

        # Update payment token in subscription
        subscription.stripe_payment_token = payment_token
        subscription.stripe_subscription_id = stripe_subscription['id']
        subscription.state = Subscription.STATE_ACTIVE
        subscription.save(
            update_fields=['stripe_payment_token', 'stripe_subscription_id', 'state'])

    context = {}

    return render(request, 'payments/payment_confirmation.html', context)
