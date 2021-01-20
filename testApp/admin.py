from django.contrib import admin
from .models import User, Question, MCQQuestion, QuestionImage, Test

# Register your models here.
admin.site.register(User)
admin.site.register(Question)
admin.site.register(MCQQuestion)
admin.site.register(QuestionImage)
admin.site.register(Test)
