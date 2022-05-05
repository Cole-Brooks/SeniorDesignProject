# from parking.local_settings import SERVICE_EMAIL
from celery import shared_task
from django import forms
from django.db.models import fields
from .models import Contact
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import HttpResponse
from django.conf import settings
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from customers.models import DuePaymentReminder
from django.utils.html import format_html


@shared_task
def send_due_payment_reminder():
    """Function to use for sending emails"""
    due_payments = DuePaymentReminder.objects.filter(has_been_sent=False).all()

    for due_payment in due_payments.iterator():
        message = format_html("{} {}{}. {} {} {} {} {}",
                              "You have reached the maximum due amount.",
                              "You have a total due payment of $",
                              due_payment.amount_due,
                              "\n\nMake sure to pay your bill to",
                              due_payment.parking,
                              "to have access to the parking lot next time.\n\n",
                              "Discard this message if you have already paid your bill for this parking.\n\n",
                              "Thank you!"
                              )
        try:
            send_mail('Due payment reminder', message, from_email=settings.SERVICE_EMAIL,
                      recipient_list=[due_payment.email_to], fail_silently=False, )
            due_payment.has_been_sent = True
            due_payment.save()
        except BadHeaderError:
            return HttpResponse('Invalid header found')


@shared_task
def delete_already_sent_reminders():
    """Function to use for deleting emails that have already been sent"""
    DuePaymentReminder.objects.filter(has_been_sent=True).all().delete()
