import requests
from bs4 import BeautifulSoup
from lxml import etree
import lxml
import time
import os
from tqdm import tqdm
from openpyxl import Workbook
from datetime import datetime
import random
import csv
user_agents = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
]
request_headers = {
    'user-agent':
        random.choice(user_agents),
    'Connection':
        "keep-alive",
    'Referer':
        "https://www.douban.com"
}
def get_image(url_str):
    resp=requests.get(url=url_str,headers=request_headers)
    status_code=resp.status_code
    if status_code==200:
          resp.encoding='utf-8'
          html_text=resp.text
          soup_document=BeautifulSoup(html_text,'lxml')
          recipes=soup_document.select('#J_list > ul > li > div.detail > h2 > a')
          image_elements=soup_document.select('#J_list > ul > li:nth-child(1) > div.pic > a > img')
          for dish_name_element,image_element in zip(recipes,image_elements):
               dish_name=dish_name_element.get("title").strip()
               image_url=image_element.get('data-src')
               time.sleep(random.uniform(0,0.3))
               image_resp=requests.get(image_url,headers=request_headers)
               if image_resp.status_code==200:
                    file_name=dish_name
                    file_name = file_name.replace("|", "_")
                    file_name='%s.jpg'%file_name
                    file_path='.\picture'
                    if not os.path.exists(file_path):
                        os.mkdir(file_path)
                # 保存图片到本地
                    with open(file_path + os.sep + file_name, 'wb') as f:

                        f.write(image_resp.content)
                        print(f"图片 {file_name} 保存成功！")
               else:
                    print("fuck u")
urls_chuancai = ['https://home.meishichina.com/recipe/chuancai/page/{}/'.format(str(i)) for i in range(1, 4)]
urls_yuecai = ['https://home.meishichina.com/recipe/yuecai/page/{}/'.format(str(i)) for i in range(1,4)]
    
for url in urls_yuecai:
       get_image(url)
       time.sleep(2)   
for url in urls_chuancai:
       get_image(url)
       time.sleep(1)           