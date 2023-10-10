import requests
import hashlib
import logging
from django.shortcuts import render
from .forms import PaymentRequestForm
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from decimal import Decimal, ROUND_DOWN


def payment_request_view(request):
    API_KEY = "9b62ff8e-f03b-4421-b836-b630edad99dg"
    SALT = "18e6063d410586se913fa536be8dbf237a6c15ee"
    if request.method == 'POST':
        form = PaymentRequestForm(request.POST)

        if form.is_valid():
            # amount = Decimal(form.cleaned_data['amount']).quantize(Decimal('0.00'), rounding=ROUND_DOWN)
            api_key = API_KEY

            # Calculate the hash from the form data
            data_to_hash = "|".join([
                form.cleaned_data['address_line_1'],
                # form.cleaned_data['address_line_2'],
                str(form.cleaned_data['amount']),
                str(api_key),
                form.cleaned_data['city'],
                form.cleaned_data['country'],
                form.cleaned_data['currency'],
                form.cleaned_data['description'],
                form.cleaned_data['email'],
                form.cleaned_data['mode'],
                form.cleaned_data['name'],
                form.cleaned_data['order_id'],
                form.cleaned_data['phone'],
                form.cleaned_data['return_url'],
                form.cleaned_data['state'],
                form.cleaned_data['zip_code'],
                ])
        
            hashSequence = f"{SALT}|{data_to_hash}"    
            hash = hashlib.sha512(hashSequence.encode()).hexdigest().upper()

            # Prepare the data for the POST request
            url = "https://uatpgbiz.omniware.in/v2/paymentrequest"
            payload = {**form.cleaned_data, 'hash': hash, 'api_key': API_KEY}

            # return HttpResponseRedirect("https://pgbiz.omniware.in/v2/paymentrequest")
            # Make the POST request
            response = requests.post(url, data=payload)

            # Handle the response as needed
            if response.status_code == 200:
                # Payment request successful
                # Handle success
                pass
            else:
                # Payment request failed
                # Handle failure
                pass
            return render(request, 'redirect_template.html', {'redirect_url': url, 'payload': payload})
    else:
        form = PaymentRequestForm()

    context = {'form': form}
    return render(request, 'payment_request.html', context)
