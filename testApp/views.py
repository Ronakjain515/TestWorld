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
                    return redirect("index")
                else:
                    message = "Invalid Credentials..."
            else:
                message = "Email not Exists..."
        except:
            message = "Something went wrong..."
    return render(request, "login.html", context={"message": message})


def register(request):
    message = ""
    if request.method == "POST":
        try:
            name = request.POST['name']
            email = request.POST['email']
            password = request.POST['password']
            isUserExist = User.objects.all().filter(email=email).count()
            if isUserExist == 0:
                user = User(name=name, email=email, password=password)
                user.save()
                return redirect("login")
            else:
                message = "Email already Exist"
        except:
            message = "Something went wrong...."
    return render(request, "register.html", context={"message": message})
