
from django import forms
from .models import Product

class product_form(forms.Form):
    name = forms.CharField(max_length=200, label="Nombre")
    description = forms.CharField(max_length=300)
    price = forms.DecimalField(max_digits=10, decimal_places=2)
    available = forms.BooleanField(initial=True,  required=False)
    photo = forms.ImageField(label="Foto", required=False)

    def save(self):
        Product.objects.create(
            name=self.cleaned_data['name'],
            description=self.cleaned_data['description'],
            price=self.cleaned_data['price'],
            available=self.cleaned_data['available'],
            photo=self.cleaned_data['photo'],
        )
