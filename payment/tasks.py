import os
import pdfkit
from celery import shared_task
from django.contrib.staticfiles import finders
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from orders.models import Order


@shared_task
def payment_completed(order_id):
    """
    Task to send an email notification when an order is
    successfully paid.
    """
    order = Order.objects.get(id=order_id)
    subject = f'My Shop - Invoice no. {order.id}'
    message = (
        'Please, find attached the invoice for your recent purchase.'
    )
    mail = os.environ.get('EMAIL_HOST_USER')
    email = EmailMessage(
        subject, message, mail, [order.email]
    )
    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
    html = render_to_string('orders/order/pdf.html', {'order': order})
    css = finders.find('css/pdf.css')
    pdf = pdfkit.from_string(html, False, configuration=config, css=css)
    email.attach(
        f'order_{order_id}.pdf', pdf, 'application/pdf'
    )
    email.send()
