# ./users/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings
from .forms import LoginForm, RegisterForm


def login_view(request):
    next_url = request.GET.get("next") or "/"
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect("/")
    else:
        form = LoginForm(request)
    return render(request, "users/login.html", {
        "form": form,
        "next": next_url
    })


def logout_view(request):
    logout(request)
    return redirect("/")


# users/views.py

def register_view(request):
    next_url = request.GET.get("next") or request.POST.get("next") or "/"

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(next_url)  # ⬅️ ir a lo que había antes
    else:
        form = RegisterForm()

    return render(request, "users/register.html", {
        "form": form,
        "next": next_url
    })

