from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .tasks import order_created
from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.conf import settings
from .models import Order
from django.contrib import messages
from .taskss import payment_completed
from django.contrib.auth.decorators import login_required

@login_required
def order_create(request: HttpRequest) -> HttpResponse:
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # launch asynchronous task
            order_created.delay(order.id)
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            return render(request, 'orders/order/process.html', {'order': order, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})


def payment_done(request):
    return render(request, 'orders/order/done.html')

def payment_canceled(request):
    return render(request, 'orders/order/canceled.html')


def verify_payment(request: HttpResponse, ref: str) -> HttpResponse:
    payment = get_object_or_404(Order, ref=ref)
    verified = payment.verify_payment()
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    if verified:
        # launch asynchronous task
        payment_completed.delay(order.id)
        messages.success(request, "verification successful")
    else:
        messages.error(request, "verification failed")
        return redirect('orders:canceled')
    return redirect('orders:done')

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .models import Order

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint

@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')])
    return response
