from django.views.generic import TemplateView
from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render
# Create your views here.




def about(request):
    """
    Renderiza la página 'Acerca de la web'.
    """
    return render(request, "core/about.html")


def terms(request):
    """
    Renderiza la página 'Acerca de la web'.
    """
    return render(request, "core/terms.html")


class HomeView(TemplateView):
    # template_name = "core/home.html" # esto es cuando entra en home
    def get(self, request, *args, **kwargs):
        return redirect('products:product_list')



def test_message_view(request):
    messages.success(request, "This is a success message!")
    messages.info(request, "This is an info message.")
    messages.warning(request, "This is a warning.")
    messages.error(request, "This is an error.")
    return redirect('core:home')




