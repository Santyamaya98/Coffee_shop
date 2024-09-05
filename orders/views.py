from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest

from .models import Order, OrderProduct
from products.models import Product

class MyOrderView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "orders/my_order.html"
    context_object_name = "order"

    def get_object(self, queryset=None):
        return Order.objects.filter(is_active=True, user=self.request.user).first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_object()
        if order:
            context['total_price'] = sum(
                item.product.price * item.quantity for item in order.orderproduct_set.all()
            )
        return context

class CreateOrderProductView(View):
    template_name = "orders/create_order_product.html"

    def get(self, request):
        products = Product.objects.all()
        context = {
            'products': products,
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        # Fetch or create the active order for the current user
        order, created = Order.objects.get_or_create(
            is_active=True,
            user=request.user,
        )

        # Process each product in the form
        for key, value in request.POST.items():
            if key.startswith('product_id_'):
                product_id = value
                quantity_key = key.replace('product_id_', 'quantity_')
                quantity = request.POST.get(quantity_key)

                if not quantity:
                    continue

                try:
                    quantity = int(quantity)
                    if quantity <= 0:
                        raise ValueError("Quantity must be a positive integer")
                except ValueError:
                    return HttpResponseBadRequest("Invalid quantity value")

                product = get_object_or_404(Product, id=product_id)

                # Create or update the OrderProduct instance
                order_product, created = OrderProduct.objects.get_or_create(
                    order=order,
                    product=product,
                    defaults={'quantity': quantity}
                )

                if not created:
                    # Update the quantity if the OrderProduct already exists
                    order_product.quantity += quantity
                    order_product.save()

        return redirect('my_order')