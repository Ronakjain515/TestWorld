from django.contrib import admin
from .models import User, Question, MCQQuestion, QuestionImage, Test, Test_User_Occurrence, Test_User_Questions

# Register your models here.
admin.site.register(User)
admin.site.register(Question)
admin.site.register(MCQQuestion)
admin.site.register(QuestionImage)
admin.site.register(Test)
admin.site.register(Test_User_Occurrence)
admin.site.register(Test_User_Questions)
