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
import urllib3
urllib3.disable_warnings()
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
        "close",
    'Referer':
        "https://www.douban.com"
}
#
data_list=[]

def get_recipe(url_str):
    resp=requests.get(url=url_str,headers=request_headers,verify=False)
    status_code=resp.status_code
    if status_code==200:
        resp.encoding='utf-8'
        html_text=resp.text
        soup_document=BeautifulSoup(html_text,'lxml')
        #recipes = soup_document.select('div.userTop.clear')
        recipes=soup_document.select('#J_list > ul > li > div.detail > h2 > a')
        image_elements=soup_document.select('#J_list > ul > li:nth-child(1) > div.pic > a > img')
        for recipe,image_element in zip(recipes,image_elements):
            # 这是菜名
            dish_name=recipe.get("title")
            #点进去爬一爬
            dish_herf=recipe.get('href').strip()
            print(dish_herf)
            #信息     
            get_dish_detail(dish_herf,dish_name)
           
            
    else:
        print(url_str+"不懂为什么挂掉了")   
def get_dish_detail(url_str,dish_name):
    resp=requests.get(url=url_str,headers=request_headers,verify=False)
    status_code=resp.status_code
    if status_code ==200:
        resp.encoding='utf-8'
        html_text=resp.text
        #使用lxml解析为Xpath
        soup_answer=BeautifulSoup(html_text,'lxml')     
        selector=lxml.etree.HTML(html_text)
        main_ingredient_dic={}
        secondary_ingredient_dic={}
        spices_dic={}

        #加上用量
        #主料
        main_ingredient_element=selector.xpath('/html/body/div[5]/div/div[1]/div[3]/div/fieldset[1]/div/ul/li/span[1]/b')
        if not main_ingredient_element:
            main_ingredient_element=selector.xpath('/html/body/div[5]/div/div[1]/div[3]/div/fieldset[1]/div/ul/li/span[1]/a/b')
        for i in range(0,len(main_ingredient_element)):
            main_ingredient_name=main_ingredient_element[i].text
            #main_ingredient_dic.append(main_ingredient_name)
            main_ingredient_usage=selector.xpath('/html/body/div[5]/div/div[1]/div[3]/div/fieldset[1]/div/ul/li/span[2]')
            main_ingredient_dic[main_ingredient_name]=main_ingredient_usage[i].text
        time.sleep(random.uniform(0,0.3))
        #辅料
        secondary_ingredient_element=selector.xpath('/html/body/div[5]/div/div[1]/div[3]/div/fieldset[2]/div/ul/li/span[1]/a/b')
        if not secondary_ingredient_element:
            secondary_ingredient_element=selector.xpath('/html/body/div[5]/div/div[1]/div[3]/div/fieldset[2]/div/ul/li/span[1]/b')        
        for i in range(0,len(secondary_ingredient_element)):
            secondary_ingredient_name=secondary_ingredient_element[i].text
            #secondary_ingredient_list.append(secondary_ingredient_name)
            secondary_ingredient_usage=selector.xpath('/html/body/div[5]/div/div[1]/div[3]/div/fieldset[2]/div/ul/li/span[2]')
            secondary_ingredient_dic[secondary_ingredient_name]=secondary_ingredient_usage[i].text
        time.sleep(random.uniform(0,0.3))
        #调料
        spices_element=selector.xpath('/html/body/div[5]/div/div[1]/div[3]/div/fieldset[3]/div/ul/li/span[1]/a/b')
        if not spices_element:
            spices_element=selector.xpath('/html/body/div[5]/div/div[1]/div[3]/div/fieldset[3]/div/ul/li/span[1]/b')
        for i in range (0,len(spices_element)):
            spice_name=spices_element[i].text
            spices_element_usage=selector.xpath('/html/body/div[5]/div/div[1]/div[3]/div/fieldset[3]/div/ul/li/span[2]')
            #pices_list.append(spice_name)
            spices_dic[spice_name]=spices_element_usage[i].text
        time.sleep(random.uniform(0,0.3))
        #口味 工艺 耗时 难度 呃呃
        dish_info={
            '口味':None,
             '工艺':None,
            '耗时':None,
            '难度':None
             }
        detail_info_index = 1
        for i in dish_info:
            detail_text = selector.xpath('/html/body/div[5]/div/div[1]/div[3]/div/div[4]/ul/li[%d]/span[1]/a'%detail_info_index)[0].text
            dish_info[i] = detail_text
            detail_info_index += 1
        methods=''
        method_num = selector.xpath('/html/body/div[5]/div/div[1]/div[3]/div/div[6]/ul/li/div[2]/div')
        method = selector.xpath('/html/body/div[5]/div/div[1]/div[3]/div/div[6]/ul/li/div[2]/text()')
        for i in range(0,len(method_num)):
            methods += method_num[i].text + '.'  + method[i] + '  '
        data_list.append((dish_name,main_ingredient_dic,secondary_ingredient_dic,spices_dic,dish_info,methods))
    else:
        print(dish_name+"的详情页没爬出来")
        
def save_to_csv():
    file_path = os.path.join(r'E:\Python\data\chuancai')
    if not os.path.exists(file_path):
        os.mkdir(file_path) 

    with open(file_path + os.sep + 'dish.csv','w',newline='',encoding='utf-8') as f:
             
             writer = csv.writer(f)
             writer.writerow(['菜品名','口味','工艺','耗时','难度','步骤'])

    with open(file_path + os.sep + 'main_ingredient.csv','w',newline='',encoding='utf-8') as f:
            
            writer = csv.writer(f)
            writer.writerow(['名字'])

    with open(file_path + os.sep + 'secondary_ingredient.csv','w',newline='',encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['名字'])

    with open(file_path + os.sep + 'spices.csv','w',newline='',encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['名字'])

    with open(file_path + os.sep + 'ingredient_amount.csv','w',newline='',encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['原料名','用量','菜品名'])

    with open(file_path + os.sep + 'cuisine_dish.csv','w',newline='',encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['菜品名','属于','菜系'])

# 避免重复存储
    main_ingredient_have_been_added = []
    secondary_ingredient_have_been_added = []
    spices_dict_have_been_added = []

    for data in data_list:
    
        with open(file_path + os.sep + 'dish.csv', 'a', newline='',encoding='utf-8') as f: 
            writer = csv.writer(f)
            writer.writerow([data[0],data[4]['口味'],data[4]['工艺'],data[4]['耗时'],data[4]['难度'],data[5]])
    # main_ingredient.csv
        with open(file_path + os.sep + 'main_ingredient.csv','a',newline='',encoding='utf-8') as f:
            writer = csv.writer(f)
            for main_ingredient_name in data[1]:
                if main_ingredient_name in main_ingredient_have_been_added:
                    continue
                main_ingredient_have_been_added.append(main_ingredient_name)
                writer.writerow([main_ingredient_name])
    # secondary_ingredient.csv            
        with open(file_path + os.sep + 'secondary_ingredient.csv','a',newline='',encoding='utf-8') as f:

            writer = csv.writer(f)
            for secondary_ingredient_name in data[2]:
                 if secondary_ingredient_name in secondary_ingredient_have_been_added:
                      
                    continue
                 secondary_ingredient_have_been_added.append(secondary_ingredient_name)
                 writer.writerow([secondary_ingredient_name])
            
                
        with open(file_path + os.sep + 'spices.csv','a',newline='',encoding='utf-8') as f:
                writer = csv.writer(f)
                for spices_name in data[3]:
                        if spices_name in spices_dict_have_been_added:
                            continue
                spices_name = ''
                spices_dict_have_been_added.append(spices_name)
                writer.writerow([spices_name])
                

        with open(file_path + os.sep + 'ingredient_amount.csv','a',newline='',encoding='utf-8') as f:
                 writer = csv.writer(f)
                 for main_ingredient_name in data[1]:
                    writer.writerow([main_ingredient_name,data[1][main_ingredient_name],data[0]])
                 for secondary_ingredient_name in data[2]:
                     writer.writerow([secondary_ingredient_name,data[2][secondary_ingredient_name],data[0]])
                 for spices_name in data[3]:
                    writer.writerow([spices_name,data[3][spices_name],data[0]])

        with open(file_path + os.sep + 'cuisine_dish.csv','a',newline='',encoding='utf-8') as f:
                 writer = csv.writer(f)
                 writer.writerow([data[0],'属于','川菜'])

if __name__=="__main__":
     
    urls_chuancai = ['https://home.meishichina.com/recipe/chuancai/page/{}/'.format(str(i)) for i in range(1, 4)]
    urls_yuecai = ['https://home.meishichina.com/recipe/yuecai/page/{}/'.format(str(i)) for i in range(1,4)]
    
    for url in urls_yuecai:
        get_recipe(url)
        time.sleep(1)
    
    '''
    for url in urls_yuecai:
         get_recipe(url)
         time.sleep(1)
    '''
    print("End")
    print(data_list)
    #save_to_csv()
#print(data_list)