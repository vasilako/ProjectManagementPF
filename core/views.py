from django.views.generic import TemplateView
from django.contrib import messages
from django.shortcuts import redirect

# Create your views here.

class HomeView(TemplateView):
    # template_name = "core/home.html" # esto es cuando entra en home
    def get(self, request, *args, **kwargs):
        return redirect('products:product_list')



def test_message_view(request):
    messages.success(request, "This is a success message!")
    messages.info(request, "This is an info message.")
    messages.warning(request, "This is a warning.")
    messages.error(request, "This is an error.")
    return redirect('')




