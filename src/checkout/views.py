from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
import stripe 
import string
import random

stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.
@login_required
def checkout(request):
    publishKey=settings.STRIPE_PUBLISHABLE_KEY
    customer_id = request.user.userstripe.stripe_id
    customer_email=request.user.email
    confirm_message = None
    
    if request.method == 'POST':
        token=request.POST['stripeToken']
        
        try:
            # Charge the user's card:
            customer = stripe.Customer.retrieve(customer_id)
            customer.sources.create(source=token)
            charge = stripe.Charge.create(
              amount=1150,
              currency="gbp",
              description="Example charge",
              customer=customer,
            )
            
            ticketNo=''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
            
            name = request.user.username
            subject = '100 years of fun boat party!'
            message = """This is confirmation that you have bought one ticket to the 100 years of fun boat party! 
            \n \n Your ticket number is  """ + ticketNo + """\n \n Get Hyped! Love, \n \n Jack, Miro, Bran and Hugo xxx"""
            
            emailFrom = settings.EMAIL_HOST_USER
            emailTo = [request.user.email]
            send_mail(subject, message, emailFrom, emailTo, fail_silently=False )
            title="WOOOOOOOO!"
            confirm_message="Thanks for buying a ticket!!"
            
            name = request.user.username
            subject = 'Ticket bought'
            message = request.user.email + ' ' + request.user.username + ' ' + ticketNo
            emailFrom = request.user.email
            emailTo = [settings.EMAIL_HOST_USER]
            send_mail(subject, message, emailFrom, emailTo, fail_silently=False )
            
            confirm_message = """Thank you for buying a ticket - check your email for email confirmation and your ticket number.
            \n If you do not receive the email / have any queries, contact 100yearsoffunparty@gmail.com"""
            
        except stripe.error.CardError as e:
            print('Error', e)
            confirm_message = e
            pass
    context= {'publishKey': publishKey, 'confirm_message': confirm_message,}
    template = 'checkout.html'
    return render(request, template, context)

    
