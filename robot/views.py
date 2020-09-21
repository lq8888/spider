from django.shortcuts import render, HttpResponse
# Create your views here.
from django.core import serializers
from robot.models import ZSPapers
import json
import time
def show_exam_handle_index_controller(request):
    return render(request, "robot/exam.html")


def get_exam_all_controller(request):
    time.sleep(20)
    data = {
        "status": "0"
    }
    return HttpResponse(json.dumps(data))


def get_exam_new_controller(request):
    # count = ZSPapers().objects.count()
    # print(count)
    data = {
        "status": "0"
    }
    return HttpResponse(json.dumps(data))

