#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import random
import re
import time

from requests_html import HTMLSession, HTML

from robot.models import ZSPapers,ZSAnalysisQuestion,ZSChoiceQuestion,ZSCompletionQuestion,ZSExplanationQuestion,\
    ZSJudgeQuestion,ZSLongerQuestion,ZSMuchChoiceQuestion,ZSOtherQuestion,ZSShortAnswerQuestion,ZSIndefiniteQuestion,ZSMaterialQuestion

from robot.processor.log_handler import get_logger

user_agents = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Mobile Safari/537.36'
]


logger = get_logger()


class Spider(object):
    
    def __init__(self):
        self.start_url = "http://www.zhongshi.net/html/category/zhuanye/page/{}"
        self.paper_url = "http://www.zhongshi.net/html/{}.html"
        self.headers = {"User-Agent": random.choice(user_agents)}
        # 获取试卷链接列表
    
    # 获取页面对象
    def parse_url(self, url, index=None):
        session = HTMLSession()
        if index is not None:
            r = session.get(url.format(index), headers=self.headers)
        else:
            r = session.get(url, headers=self.headers)
        # 去掉页面中的空格
        r = r.html.html.replace('&nbsp;', ' ')
        # 重新构建页面
        h = HTML(html=r)
        return h
    
    # 获取试卷链接列表
    def get_paper_url(self, index):
        h = self.parse_url(self.start_url, index)
        paper_url_list = h.xpath('//body/section/div/div/article/header/h2//a/@href')
        return paper_url_list
    
    # 获取总页数
    def get_total_page(self, index):
        h = self.parse_url(self.start_url, index)
        total_page = re.search(r"共 (.*?) 页", h.text).group(1)
        return total_page

    # 获取指定题型数据
    def get_specific_question(self, content, question_type, all_question_list=None, question_dict=None,
                              choice_question_dict=None):
        pattern = re.compile(r'{}([\w\W]*)参考答案更多资料'.format(question_type))
        all_question_content = re.search(pattern, content).group()
        content_list = all_question_content.split('\n')
        content_list.pop(-1)
        for i in content_list:
            if i in ['单选题', '多选题', '判断题', '填空题', '简答题', '名词解释', '不定项', '论述题', '填空题：']:
                if question_type not in i:
                    all_question_list.append(question_dict)
                    question_dict = {"type": "1", "question": []}
                if i == '单选题':
                    question_dict["type"] = '1'
                elif i == '多选题':
                    question_dict["type"] = '2'
                elif i == '判断题':
                    question_dict["type"] = '3'
                elif i == '填空题':
                    question_dict["type"] = '4'
                elif i == '简答题':
                    question_dict["type"] = '5'
                elif i == '名词解释':
                    question_dict["type"] = '6'
                elif i == '案例分析':
                    question_dict["type"] = '7'
                elif i == '论述题':
                    question_dict["type"] = '8'
                elif i == '不定项':
                    question_dict["type"] = '9'
                else:
                    question_dict["type"] = '10'
                continue
            if question_dict["type"] in ['1', '2', '9']:
                if i[0: 1] not in ['A', 'B', 'C', 'D']:
                    choice_question_dict["single_question"].append(i)
                else:
                    choice_question_dict["answer"].append(i)
                if 'D' in i:
                    question_dict["question"].append(choice_question_dict)
                    choice_question_dict = {"single_question": [], "answer": []}
            else:
                question_dict["question"].append(i)
            if content_list[-1] == i:
                all_question_list.append(question_dict)

    # 获取题目数据
    def get_paper_data(self, paper_url):
        global zs_paper, question
        logger.info('开始获取试卷...')
        paper_tag = ''
        print(paper_url)
        h = self.parse_url(paper_url)
        # 获取页面中的所有文本
        content = h.text
        # print(content)
        # 获取试卷名称
        paper_title = h.xpath('/html/body/section/div[1]/div/header/h1/a')[0].text
        # 获取试卷时间
        paper_time = h.xpath('/html/body/section/div[1]/div/header/div/span[1]')[0].text
        # exam_id = h.xpath('/html/body/section/div[1]/div/header/div/span[1]')[0].text
        # 获取试卷标签
        tag = h.xpath('/html/body/section/div[1]/div/div[contains(@class, "article-tags")]/child')
        if len(tag) != 0:
            paper_tag = h.xpath('/html/body/section/div[1]/div/div[contains(@class, "article-tags")]/a')[0].text

        # 判断是否展示题型的标志位
        try:
            is_question_type = h.xpath('/html/body/section/div[1]/div/article/p[2]/span')[0].text
        except:
            is_question_type = h.xpath('/html/body/section/div[1]/div/article/p[3]/span')[0].text

        is_material = h.xpath('/html/body/section/div[1]/div/article/p[2]')[0].text
        # 构造试卷基本信息
        paper_msg_dict = {'paper_title': paper_title, 'paper_time': paper_time,
                          'paper_tag': paper_tag, 'type': '999', 'data_pid': paper_url[29:34]}

        # 定义题目存放格式
        all_question_list = [paper_msg_dict]
        question_type = "1"
        question_dict = {"type": question_type, "question": []}
        choice_question_dict = {"single_question": [], "answer": []}

        # 判断是否含题型
        if is_question_type.startswith('一'):
            pattern = re.compile(r'一、([\w\W]*)参考答案更多资料')
            all_question_content = re.search(pattern, content).group()
            content_list = all_question_content.split('\n')
            content_list.pop(-1)

            # 获取题目
            for i in content_list:
                if i[0: 2] in ['一、', '二、', '三、', '四、', '五、', '六、']:
                    if '一、' not in i:
                        all_question_list.append(question_dict)
                        question_dict = {"type": question_type, "question": []}
                    if i[2:] == '单选题':
                        question_dict["type"] = '1'
                    elif i[2:7] == '单项选择题':
                        question_dict["type"] = '1'
                    elif i[2:] == '多选题':
                        question_dict["type"] = '2'
                    elif i[2:] == '判断题':
                        question_dict["type"] = '3'
                    elif i[2:] == '填空题':
                        question_dict["type"] = '4'
                    elif i[2:] == '简答题':
                        question_dict["type"] = '5'
                    elif i[2:] == '名词解释':
                        question_dict["type"] = '6'
                    elif i[2:] == '案例分析':
                        question_dict["type"] = '7'
                    elif i[2:] == '论述题':
                        question_dict["type"] = '8'
                    elif i[2:] == '不定项':
                        question_dict["type"] = '9'
                    else:
                        question_dict["type"] = '10'
                    continue
                if question_dict["type"] in ['1', '2', '9']:
                    if i[0: 1] not in ['A', 'B', 'C', 'D']:
                        choice_question_dict["single_question"].append(i)
                    else:
                        choice_question_dict["answer"].append(i)
                    if 'D' in i:
                        question_dict["question"].append(choice_question_dict)
                        choice_question_dict = {"single_question": [], "answer": []}
                else:
                    question_dict["question"].append(i)
                if content_list[-1] == i:
                    all_question_list.append(question_dict)

        # 不含题型执行下面的逻辑
        elif is_question_type.startswith('1'):
            pattern = re.compile(r'1\.([\w\W]*)参考答案更多资料')
            all_question_content = re.search(pattern, content).group()
            content_list = all_question_content.split('\n')
            content_list.pop(-1)
            # print(content_list)

            # 获取题目
            for i in content_list:
                if i[0: 1] not in ['A', 'B', 'C', 'D']:
                    choice_question_dict["single_question"].append(i)
                else:
                    choice_question_dict["answer"].append(i)
                if 'D' in i:
                    question_dict["question"].append(choice_question_dict)
                    choice_question_dict = {"single_question": [], "answer": []}
            all_question_list.append(question_dict)
        elif is_question_type in ['单选题', '多选题', '判断题', '填空题', '简答题', '名词解释', '论述题', '不定项', '填空题：', '填空']:
            if is_question_type in '填空题':
                self.get_specific_question(content, '填空题', all_question_list, question_dict, choice_question_dict)
            elif is_question_type in '单选题':
                self.get_specific_question(content, '单选题', all_question_list, question_dict, choice_question_dict)
            elif is_question_type in '判断题':
                self.get_specific_question(content, '判断题', all_question_list, question_dict, choice_question_dict)
            elif is_question_type in '不定项':
                self.get_specific_question(content, '不定项', all_question_list, question_dict, choice_question_dict)
            elif is_question_type == '填空题：':
                pattern = re.compile(r'填空题：([\w\W]*)参考答案更多资料')
                all_question_content = re.search(pattern, content).group()
                content_list = all_question_content.split('\n')
                content_list.pop(0)
                content_list.pop(-1)
                question_dict['type'] = '4'

                for i in content_list:
                    question_dict["question"].append(i)
                all_question_list.append(question_dict)
        # 获取材料题
        elif len(is_material) > 50:
            all_question_list.append({"material": is_material})

            pattern = re.compile(r'1\.([\w\W]*)参考答案更多资料')
            all_question_content = re.search(pattern, content).group()
            content_list = all_question_content.split('\n')
            content_list.pop(-1)

            for i in content_list:
                if i[0: 1] not in ['A', 'B', 'C', 'D']:
                    choice_question_dict["single_question"].append(i)
                else:
                    choice_question_dict["answer"].append(i)
                if 'D' in i:
                    question_dict["question"].append(choice_question_dict)
                    choice_question_dict = {"single_question": [], "answer": []}
            question_dict['type'] = '11'
            all_question_list.append(question_dict)
        else:
            pass
        zs_paper = ZSPapers()
        # 返回json格式数据
        for data in all_question_list:
            # print(data)
            data_type = data['type']
            # print(data_type)
            if data.__contains__('data_pid'):
                zs_paper.data_pid = data['data_pid']
            # print('llllll;;;;;;;;;;'+data['data_pid'])
            # print(data.get('data_pid'))
            # print(data.__contains__('question'))
            if data.__contains__('question'):
                question = json.dumps(data['question'], ensure_ascii=False)
            if data_type == '999':
                zs_paper.exam_title = data['paper_title']
                zs_paper.exam_time = str(data['paper_time'])
               # print('======' + data['paper_time'])
                zs_paper.paper_tag = data['paper_tag']
            elif data_type == '1':
                zs_paper.choice_question = question
                try:
                    for robot_question in data['question']:
                        zs_choice_question = ZSChoiceQuestion()
                        zs_choice_question.paper_id = str(zs_paper.data_pid)
                        zs_choice_question.question_title = robot_question["single_question"][0]
                        zs_choice_question.question_option = robot_question["answer"]
                        zs_choice_question.save()
                except Exception as e:
                    pass
            elif data_type == '2':
                zs_paper.much_choice_question = question
                for robot_question in data['question']:
                    zs_much_choice_question = ZSMuchChoiceQuestion()
                    zs_much_choice_question.question_title = robot_question["single_question"][0]
                    zs_much_choice_question.question_option = robot_question["answer"]
                    zs_much_choice_question.paper_id = str(zs_paper.data_pid)
                    zs_much_choice_question.save()
            elif data_type == '3':
                zs_paper.judge_question = question
                for robot_question in list(data['question']):
                    zs_judge_question = ZSJudgeQuestion()
                    zs_judge_question.question_title = robot_question
                    zs_judge_question.paper_id = str(zs_paper.data_pid)
                    zs_judge_question.save()
            elif data_type == '4':
                zs_paper.completion_question = question
                print(data['question'])
                for robot_question in list(data['question']):
                    zs_completion_question = ZSCompletionQuestion()
                    zs_completion_question.question_title = robot_question
                    zs_completion_question.paper_id = str(zs_paper.data_pid)
                    zs_completion_question.save()
            elif data_type == '5':
                zs_paper.short_answer_question = question
                for robot_question in list(data['question']):
                    zs_short_answer_question = ZSShortAnswerQuestion()
                    zs_short_answer_question.question_title = robot_question
                    zs_short_answer_question.paper_id = str(zs_paper.data_pid)
                    zs_short_answer_question.save()
            elif data_type == '6':
                zs_paper.explanation_question = question
                for robot_question in list(data['question']):
                    zs_explanation_question = ZSExplanationQuestion()
                    zs_explanation_question.question_title = robot_question
                    zs_explanation_question.paper_id = str(zs_paper.data_pid)
                    zs_explanation_question.save()
            elif data_type == '7':
                zs_paper.analysis_question = question
                for robot_question in list(data['question']):
                    zs_analysis_question = ZSAnalysisQuestion()
                    zs_analysis_question.question_title = robot_question
                    zs_analysis_question.paper_id = str(zs_paper.data_pid)
                    zs_analysis_question.save()
            elif data_type == '8':
                zs_paper.longer_question = question
                for robot_question in list(data['question']):
                    zs_longer_question = ZSLongerQuestion()
                    zs_longer_question.question_title = robot_question
                    zs_longer_question.paper_id = str(zs_paper.data_pid)
                    zs_longer_question.save()
            elif data_type == '9':
                zs_paper.indefinite_question = question
                for robot_question in data['question']:
                    zs_indefinite_question = ZSIndefiniteQuestion()
                    zs_indefinite_question.paper_id = str(zs_paper.data_pid)
                    zs_indefinite_question.question_title = robot_question["single_question"][0]
                    zs_indefinite_question.question_option = robot_question["answer"]
                    zs_indefinite_question.save()
            elif data_type == '10':
                zs_paper.other_question = question
                for robot_question in list(data['question']):
                    zs_other_question = ZSOtherQuestion()
                    zs_other_question.question_title = robot_question
                    zs_other_question.paper_id = str(zs_paper.data_pid)
                    zs_other_question.save()
            else:
                zs_paper.material_question = data["material"]
                zs_paper.material_question = question
                for robot_question in data['question']:
                    zs_material_question = ZSIndefiniteQuestion()
                    zs_material_question.paper_id = str(zs_paper.data_pid)
                    zs_material_question.question_title = robot_question
                    zs_material_question.material_title = data["material"]
                    zs_material_question.save()
        zs_paper.save()
        print('zs_paper.save()')
        final_json = json.dumps(all_question_list, ensure_ascii=False)
        logger.info('{}试卷获取结束~'.format(paper_title))
        return final_json
    
    def run(self, page_index, total_page, is_hand_set=False):
        if not is_hand_set:
            total_page = int(self.get_total_page(1))
        
        for i in range(page_index - 1, total_page):
            for url in self.get_paper_url(i):
                self.get_paper_data(url)
                # print(final_data)
                
                # return final_data
                # time.sleep(1)
        logger.info('当前试卷index~{}'.format(i))


if __name__ == '__main__':
    spider = Spider()
    spider.run()
