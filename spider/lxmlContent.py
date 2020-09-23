# _author:'louqiang'
# __time__ = '2020/9/12 9:37 AM'

from urllib.parse import urlencode
import requests

# from requests_html import HTMLSession
#
# # page每个页面的数组
url = "http://www.zhongshi.net/html/category/zhuanye/page/{} "
# # 每套题的html
examUrl = "http://www.zhongshi.net/html/41807.html "
# # ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240"
#
# session = HTMLSession()
# r = session.get(examUrl.format("40511"))
#
# print()
# # print(examUrl.format("40511"))
# print(r.html.text)

for page in range(1,1551): var = {
    # url.format(page)
    # print(url.format(page))

}
import requests
from lxml import etree

response = requests.get(examUrl.format("40511"))
# print(response.text)

html = etree.HTML(response.text)
# items = html.xpath("//tr[@class='article-content']")
titie = html.xpath('//body/section/div/div/article/p//text()')
# titie = html.xpath('//body[contains(@class, "table-top20")]/tbody/tr//text()')
print(titie)

