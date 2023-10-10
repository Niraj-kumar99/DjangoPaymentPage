from django.http import HttpResponse
import requests
import hashlib
from django.shortcuts import render
from .forms import PaymentRequestForm
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.template import RequestContext


def payment_request_view(request):
    API_KEY = "9b62ff8e-f03b-4421-b836-b630edad99dg"
    SALT = "18e6063d410586se913fa536be8dbf237a6c15ee"
    if request.method == 'POST':
        form = PaymentRequestForm(request.POST)

        if form.is_valid():
            api_key = API_KEY

            # Calculate the hash from the form data
            data_to_hash = "|".join([
                form.cleaned_data['address_line_1'],
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

            # Make the POST request
            requests.post(url, data=payload)

            return render(request, 'redirect_template.html', {'redirect_url': url, 'payload': payload})
    else:
        form = PaymentRequestForm()

    context = {'form': form}
    return render(request, 'payment_request.html', context)


@csrf_protect
@csrf_exempt
def payment_response_view(request):

    response_code=request.POST.get("response_code")
    transaction_id=request.POST.get("transaction_id")
    response_message=request.POST.get("response_message")
    amount=request.POST.get("amount")
    reponse_hash=request.POST.get("hash")
    SALT = "18e6063d410586se913fa536be8dbf237a6c15ee"
    # API_KEY = "9b62ff8e-f03b-4421-b836-b630edad99dg"

    hash_string=SALT
    for i in sorted(request.POST):
        if(i!='hash'):
            if len(request.POST[i]) > 0:
                hash_string+='|'
                hash_string+=request.POST[i]


    
    calculated_hash = hashlib.sha512(hash_string.encode()).hexdigest().upper()
    if(reponse_hash == calculated_hash):
        if(response_code == '0'):
            return render(request, 'success.html', {"response_message":"Transaction Success","txnid": transaction_id, "status": response_message, "amount": amount})
        
        else:
            return render(request, 'failure.html', {"response_message":"Transaction Failed", "txnid": transaction_id, "status": response_message, "amount": amount})
    else:
        return render(request, 'failure.html', {"response_message":"Transaction Failed Hash Mismatch", "txnid": transaction_id, "status": response_message, "amount": amount})