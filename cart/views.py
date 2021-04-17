from django.shortcuts import render, redirect
from .cart import Cart
from django.conf import settings
from django.contrib import messages
from .forms import CheckoutForm
from order.utilities import checkout
import stripe
from order.utilities import checkout,notify_customer,notify_vendor
# Create your views here.

def cart_detail(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            stripe.api_key = settings.STRIPE_SECRET_KEY

            stripe_token = form.cleaned_data['stripe_token']
            try:
                charge = stripe.Charge.create(
                    amount = int(cart.get_total_cost()), 
                    currency = 'XOF',
                    description = 'Charge from Multivendor',
                    source = stripe_token
                ) 

                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email']
                phone = form.cleaned_data['phone']
                address = form.cleaned_data['address']
                zipcode = form.cleaned_data['zipcode']
                place = form.cleaned_data['place']

                order = checkout(request, first_name, last_name, email, phone, address, zipcode, place, cart.get_total_cost())

                cart.clear()
                notify_vendor(order)
                notify_customer(order)
                
                return redirect('success')

            except Exception:
                messages.error(request, 'there was something wrong with the payment') 
    else:
        form = CheckoutForm()    

    remove_from_cart = request.GET.get('remove_from_cart', '')
    change_quantity = request.GET.get('change_quantity', '')
    quantity = request.GET.get('quantity', '')

    if change_quantity:
        cart.add(change_quantity, quantity, True)
        return redirect('cart')

    if remove_from_cart:
        cart.remove(remove_from_cart)
        return redirect('cart')
    return render(request, 'cart.html', {'form':form, 'stripe_pub_key': settings.STRIPE_PUB_KEY})



def success(request):

    return render(request, 'success.html')