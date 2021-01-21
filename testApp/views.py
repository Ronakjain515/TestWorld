import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import User, Test, Test_User_Occurrence, Question, MCQQuestion

# Create your views here.


def index(request):
    context = {}
    try:
        if request.session["email"]:
            context["email"] = request.session["email"]
    except KeyError:
        pass

    context["tests"] = Test.objects.all()

    return render(request, "index.html", context=context)


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


def logout(request):
    try:
        del request.session["email"]
        del request.session["password"]
    except:
        pass
    return redirect("index")


def test(request):
    if request.method == "POST" and request.session["email"]:
        context = {}

        if request.POST.get("status") == "start":
            userData = User.objects.get(Q(email=request.session["email"]) & Q(password=request.session["password"]))
            testData = Test.objects.get(id=request.POST.get("testId"))
            
            occurrence = Test_User_Occurrence(testId=testData, userId=userData)
            occurrence.save()
            
            questionData = Question.objects.all().filter(testId=testData).first()

            context["occurrenceId"] = occurrence.id
            context["status"] = "onGoing"
            context["question"] = questionData
            context["timer"] = testData.timer

            questionOverview = list(Question.objects.values("id").filter(testId=testData))
            for i in range(len(questionOverview)):
                questionOverview[i]["save"] = False
                questionOverview[i]["index"] = i + 1
            context["questionOverview"] = questionOverview

            if questionData.type == "MCQ":
                mcqQuestion = MCQQuestion.objects.all().filter(questionId=questionData).first()
                context["mcqQuestion"] = mcqQuestion


        elif request.POST.get("status") == "onGoing":
            pass

        return render(request, "test.html", context=context)
    return render(request, "test.html")
