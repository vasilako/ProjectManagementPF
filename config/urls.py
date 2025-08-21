"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from django.http import HttpResponse


def health_check_view(request):
    return HttpResponse("✅ App is working.")


urlpatterns = [
    # path('health/', health_check_view, name='health_check'),
    # path('admin/', admin.site.urls),
    # path('', include('core.urls')),
    # path('products/', include('products.urls')),
]

# Add URL patterns with i18n support for internationalization and localization
urlpatterns += i18n_patterns(
    path('health/', health_check_view, name='health_check'),
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('products/', include(('products.urls', 'products'), namespace='products')),
    path('cart/', include(('cart.urls', 'cart'), namespace='cart')),
    path('orders/', include(('orders.urls', 'orders'), namespace='orders')),

)

# Configure Django to serve media files (user-uploaded content) during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
