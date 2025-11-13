from django.urls import path
from .views import HomeView, test_message_view, about, terms

app_name = "core"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path('test-messages/', test_message_view, name='test_messages'),
    path("about/", about, name="about"),
    path("terms/", terms, name="terms"),
]