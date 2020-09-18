from django.db import models

# Create your models here.
from django.db import models


class Exam(models.Model):
    exam_id = models.IntegerField()
    exam_name = models.TextField()
    exam_create_time = models.TextField()
