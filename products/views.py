#from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.views.generic import ListView
from rest_framework.views import APIView
from rest_framework.response import Response


from .forms import product_form
from .models import Product
from .serializers import ProductSerializer
"""
def base_view(request):
    return render(request, 'products/base.html')

# Create your views here.
def products_view(request):
    coffee_products = [
        {"title":"Tinto"},
        {"title":"Aromatica"},
        {"title":"Empanada"},
        {"price":1000},
        {"price":1000},
        {"price":2500},
    ]
    context = {
        "coffee_products": coffee_products
    }
    return render(request, "products/products_view.html", context)
"""

class ProductFormView(generic.FormView):
    template_name = 'products/add_product.html'
    form_class = product_form
    success_url = reverse_lazy('add_product')
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
class ListProductView(ListView):
    model = Product
    template_name = 'products/list_product.html'
    context_object_name = "products"

class ProductListAPI(APIView):
    authentication_clases = []
    permission_classes = []
    
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)