from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=10)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Test(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=100)
    noOfQuestion = models.IntegerField()
    timer = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + " - " + self.description


class Question(models.Model):
    testId = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.CharField(max_length=2000)
    type = models.CharField(max_length=10)
    answer = models.CharField(max_length=500)

    def __str__(self):
        return self.question


class MCQQuestion(models.Model):
    questionId = models.ForeignKey(Question, on_delete=models.CASCADE)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)

    def __str__(self):
        return self.option1


class QuestionImage(models.Model):
    questionId = models.ForeignKey(Question, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="questionImage/")


class Test_User_Occurrence(models.Model):
    testId = models.ForeignKey(Test, on_delete=models.CASCADE)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    