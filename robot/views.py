from django.shortcuts import render, HttpResponse
# Create your views here.
from django.core import serializers
from robot.models import ZSPapers
import json
import time
from django.views.decorators.csrf import csrf_exempt
from robot.processor.spider_run import Spider


def show_exam_handle_index_controller(request):
    return render(request, "robot/exam.html")


def get_exam_all_controller(request):
    spider = Spider()
    spider.run(1, False)
    data = {
        "status": "0"
    }
    return HttpResponse(json.dumps(data))


def get_exam_new_controller(request, num):
    page_num = int(num)
    print(num)
    spider = Spider()
    spider.run(1, page_num, True)
    data = {
        "status": "0"
    }
    return HttpResponse(json.dumps(data))
