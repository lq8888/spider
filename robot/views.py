from django.shortcuts import render
from robot.models import  Exam
# Create your views here.


def show_exam_handle_index_controller(request):
    return render(request, "robot/exam.html")


