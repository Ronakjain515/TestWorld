import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import User
# Create your views here.


def index(request):
    return render(request, "index.html")


def login(request):
    message = ""
    if request.method == "POST":
        try:
            email = request.POST.get("email")
            password = request.POST.get("password")
            isEmailExist = User.objects.all().filter(email=email).count()
            if isEmailExist == 1:
                isUserExist = User.objects.all().filter(Q(email=email) & Q(password=password)).count()
                if isUserExist == 1:
                    request.session["email"] = email
                    request.session["password"] = password
                    return redirect("register")
                else:
                    message = "Invalid Credentials..."
            else:
                message = "Email not Exists..."
        except:
            message = "Something went wrong..."
    return render(request, "login.html", context={"message": message})


def register(request):
    return render(request, "register.html")
