from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.views import generic
from django.urls import reverse_lazy
# Create your views here.
def logout_view(request):
    logout(request)
    return redirect('products/')
# views.py
class RegisterView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'users/register.html'  # Asegúrate de crear esta plantilla
    success_url = reverse_lazy('login')  # Redirige a la página de inicio de sesión después del registro
