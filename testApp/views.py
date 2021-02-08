import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from .models import User, Test, Test_User_Occurrence, Question, MCQQuestion, Test_User_Questions

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
            context["questionIndex"] = 0
            context["timer_min"] = testData.timer_minutes
            context["timer_sec"] = testData.timer_seconds

            questionOverview = list(Question.objects.values("id").filter(testId=testData).order_by("id"))
            for i in range(len(questionOverview)):
                questionOverview[i]["save"] = False
                questionOverview[i]["index"] = i + 1
            context["questionOverview"] = questionOverview

        elif request.POST.get("status") == "onGoing":
            
            questionIndex = int(request.POST.get("questionIndex"))
            context["occurrenceId"] = request.POST.get("occurrenceId")
            context["status"] = request.POST.get("onGoing")
            context["timer_min"] = request.POST.get("timer_min")
            context["timer_sec"] = request.POST.get("timer_sec")
            context["questionIndex"] = questionIndex

            occurrence = Test_User_Occurrence.objects.get(id=request.POST.get("occurrenceId"))
            questionData = Question.objects.all().filter(testId=occurrence.testId)[questionIndex]
            
            context["question"] = questionData

            answer = request.POST.get("answer")
            if answer != None:
                question = Question.objects.all().filter(testId=occurrence.testId)[questionIndex - 1]
                test_user_question = Test_User_Questions()
                try:
                    test_user_question = Test_User_Questions.objects.get(questionId=question, occurrenceId=occurrence)
                    test_user_question.answer = answer
                except test_user_question.DoesNotExist:
                    test_user_question = Test_User_Questions(questionId=question, occurrenceId=occurrence, answer=answer)
                test_user_question.save()


            test_user_question_overview = Test_User_Questions.objects.values_list("questionId", flat=True).filter(occurrenceId=occurrence)
            questionOverview_data = Question.objects.values_list("id", flat=True).filter(testId=occurrence.testId).order_by("id")
            questionOverview = []
            i = 1
            for question in questionOverview_data:
                if question in test_user_question_overview:
                    questionOverview.append({"id": question, "save": True, "index": i})
                    if questionData.id == question:
                        answerdata = Test_User_Questions.objects.values_list("answer", flat=True).filter(questionId=questionData.id, occurrenceId=occurrence)
                        context["answer"] = answerdata[0]
                else:
                    questionOverview.append({"id": question, "save": False, "index": i})
                i = i + 1
            context["questionOverview"] = questionOverview

        if questionData.type == "MCQ":
            mcqQuestion = MCQQuestion.objects.all().filter(questionId=questionData).first()
            context["mcqQuestion"] = mcqQuestion
        
        return render(request, "test.html", context=context)
    return render(request, "test.html")
