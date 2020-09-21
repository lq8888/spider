#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import random
import re
import time

from requests_html import HTMLSession, HTML

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
        aa
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
    
    # 获取题目数据
    def get_paper_data(self, paper_url):
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
        # 获取试卷标签
        tag = h.xpath('/html/body/section/div[1]/div/div[contains(@class, "article-tags")]/child')
        if len(tag) != 0:
            paper_tag = h.xpath('/html/body/section/div[1]/div/div[contains(@class, "article-tags")]/a')[0].text
        
        # 判断是否展示题型的标志位
        try:
            is_question_type = h.xpath('/html/body/section/div[1]/div/article/p[2]/span')[0].text
        except:
            is_question_type = h.xpath('/html/body/section/div[1]/div/article/p[3]/span')[0].text
        
        # 构造试卷基本信息
        paper_msg_dict = {'paper_title': paper_title, 'paper_time': paper_time, 'paper_tag': paper_tag}
        
        # 定义题目存放格式
        all_question_list = []
        all_question_list.append(paper_msg_dict)
        question_type = "1"
        question_dict = {"type": question_type, "question": []}
        choice_question_dict = {"single_question": [], "answer": []}
        
        # 判断是否含题型
        if '一、' in is_question_type:
            pattern = re.compile(r'一、([\w\W]*)参考答案更多资料')
            all_question_content = re.search(pattern, content).group()
            content_list = all_question_content.split('\n')
            content_list.pop(-1)
            # print(content_list)
            
            # 获取题目
            for i in content_list:
                if i[0: 2] in ['一、', '二、', '三、', '四、', '五、', '六、']:
                    if '一、' not in i:
                        all_question_list.append(question_dict)
                        question_dict = {"type": question_type, "question": []}
                    if i[2:] == '单选题':
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
                    else:
                        question_dict["type"] = '9'
                    continue
                if question_dict["type"] in ['1', '2']:
                    if i[0: 2] not in ['A.', 'B.', 'C.', 'D.']:
                        choice_question_dict["single_question"].append(i)
                    else:
                        choice_question_dict["answer"].append(i)
                    if 'D.' in i:
                        question_dict["question"].append(choice_question_dict)
                        choice_question_dict = {"single_question": [], "answer": []}
                
                else:
                    question_dict["question"].append(i)
                if content_list[-1] == i:
                    all_question_list.append(question_dict)
        
        # 不含题型执行下面的逻辑
        else:
            pattern = re.compile(r'1\.([\w\W]*)参考答案更多资料')
            all_question_content = re.search(pattern, content).group()
            content_list = all_question_content.split('\n')
            content_list.pop(-1)
            # print(content_list)
            
            # 获取题目
            for i in content_list:
                if i[0: 2] not in ['A.', 'B.', 'C.', 'D.']:
                    choice_question_dict["single_question"].append(i)
                else:
                    choice_question_dict["answer"].append(i)
                if 'D.' in i:
                    question_dict["question"].append(choice_question_dict)
                    choice_question_dict = {"single_question": [], "answer": []}
            all_question_list.append(question_dict)
        # 返回json格式数据
       
        final_json = json.dumps(all_question_list, ensure_ascii=False)
        logger.info('{}试卷获取结束~'.format(paper_title))
        return final_json
    
    def run(self, page_index=1, total_page=50, is_hand_set=False):
        if not is_hand_set:
            total_page = int(self.get_total_page(1))
        
        for i in range(page_index - 1, total_page):
            for url in self.get_paper_url(i):
                final_data = self.get_paper_data(url)
                print(final_data)
                # return final_data
                # time.sleep(1)
        logger.info('当前试卷index~{}'.format(i))


if __name__ == '__main__':
    spider = Spider()
    spider.run()