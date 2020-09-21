from django.db import models

# Create your models here.
from django.db import models


class ZSPapers(models.Model):
    # 时间
    data_pid = models.CharField(max_length=15)
    # 试卷名称
    exam_title = models.TextField()
    # 试卷创建时间
    exam_time = models.CharField(max_length=15)
    # 标签
    tags = models.TextField()
    # 单选题
    choice_question = models.TextField()
    # 判断题
    judge_question = models.TextField()
    # 填空题
    completion_question = models.TextField()
    # 简答题
    short_answer_question = models.TextField()
    # 名词解释
    explanation_question = models.TextField()
    # 案例分析
    analysis_question = models.TextField()
    # 多选题
    much_choice_question = models.TextField()
    # 论述题
    longer_question = models.TextField()



