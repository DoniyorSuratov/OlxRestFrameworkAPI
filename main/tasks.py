from celery import shared_task
from django.core.mail import send_mail
from django.urls import reverse, reverse_lazy


@shared_task
def send_email(emails: list, product):
    send_email(
        subject='Uploaded new Advertisement ',
        message=f'''
        Title: {product.product_type['title']}
        Description: {product.product_type['category']}
        Price: {product.product_type['price']}
        Link: http://127.0.0.1:8000/api/product-update/{product['id']}''',

        from_email='From OLX team',
        recipient_list=emails,
        fail_silently=True
    )
    return 'Done'