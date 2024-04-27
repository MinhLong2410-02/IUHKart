from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string



def send_welcome_mail(request, user):
    ''' Send welcome mail to vendor. '''
    current_site = get_current_site(request)

    body = render_to_string("mail.html",
                            {'current_site': request.META['HTTP_USER_AGENT'], 'domain': current_site.domain, 'user': request.user.vendor})

    mail = EmailMessage(
        subject="Welcome to IUHKart!",
        body=body,
        from_email=settings.EMAIL_HOST_USER,
        to=[request.user.vendor.email],
    )
    mail.content_subtype = "HTML"
    mail.send()
    return None
