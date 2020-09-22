from django.db import models

# Create your models here.
from django.db import models


# 中师试卷
class ZSPapers(models.Model):
    # 试卷id
    data_pid = models.CharField(max_length=15, primary_key=True)
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
    # 其他题
    other_question = models.TextField()


# 单选题
class ZSChoiceQuestion(models.Model):
    # 题目标题
    question_title = models.TextField()
    # 题目选项
    question_option = models.TextField()
    # 试卷id
    paper_id = models.ForeignKey("ZSPapers", on_delete=models.DO_NOTHING)


# 判断题
class ZSJudgeQuestion(models.Model):
    # 题目标题
    question_title = models.TextField()
    # 试卷id
    paper_id = models.ForeignKey("ZSPapers", on_delete=models.DO_NOTHING)


# 填空题
class ZSCompletionQuestion(models.Model):
    # 题目标题
    question_title = models.TextField()
    # 试卷id
    paper_id = models.ForeignKey("ZSPapers", on_delete=models.DO_NOTHING)


# 简答题
class ZSShortAnswerQuestion(models.Model):
    # 题目标题
    question_title = models.TextField()
    # 试卷id
    paper_id = models.ForeignKey("ZSPapers", on_delete=models.DO_NOTHING)


# 名词解释题
class ZSExplanationQuestion(models.Model):
    # 题目标题
    question_title = models.TextField()
    # 试卷id
    paper_id = models.ForeignKey("ZSPapers", on_delete=models.DO_NOTHING)


# 案例分析题
class ZSAnalysisQuestion(models.Model):
    # 题目标题
    question_title = models.TextField()
    # 试卷id
    paper_id = models.ForeignKey("ZSPapers", on_delete=models.DO_NOTHING)


# 多选题
class ZSMuchChoiceQuestion(models.Model):
    # 题目标题
    question_title = models.TextField()
    # 题目选项
    question_option = models.TextField()
    # 试卷id
    paper_id = models.ForeignKey("ZSPapers", on_delete=models.DO_NOTHING)


# 论述题
class ZSLongerQuestion(models.Model):
    # 题目标题
    question_title = models.TextField()
    # 试卷id
    paper_id = models.ForeignKey("ZSPapers", on_delete=models.DO_NOTHING)


# 其他题
class ZSOtherQuestion(models.Model):
    # 题目标题
    question_title = models.TextField()
    # 试卷id
    paper_id = models.ForeignKey("ZSPapers", on_delete=models.DO_NOTHING)
