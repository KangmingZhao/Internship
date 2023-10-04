'''
在本地运行KBQA的文件 app.py 是据此修改而来
'''

import jena_sparql_endpoint
import question2sparql


if __name__ == '__main__':
    
    # TODO 连接Fuseki服务器。
    fuseki = jena_sparql_endpoint.JenaFuseki()
    # TODO 初始化自然语言到SPARQL查询的模块，参数是外部词典列表(即与食物有关的词表)。
    q2s = question2sparql.Question2Sparql(
        [r'./external_dict/entities_list.txt'])

    print("\n\n亲爱的食客你好啊，#老八# 在此为您提供问答服务\n")
    print("可以提问的菜系包括：粤菜、川菜、鲁菜、苏菜")
    print("                   浙菜、闽菜、湘菜、徽菜")
    print("您可以提问的问题类型包括：制作方法，所有食材，原料，特色，某道菜属于的菜系等等\n")
    print("提示：您可以提问的问题例如：")
    print("如何制作红烧划水？/ 红烧划水的制作步骤是什么？")
    print("徽菜包含哪些菜品？")
    print("咸菜榨菜丝粢饭团属于什么菜系？")
    print("麻辣小龙虾的食材有哪些？")
    print("腊肠煲仔饭的原料是什么？")
    print('松鼠鱼的 特色/特点 是什么？')
    print('蚂蚁上树的 口味/耗时/工艺/难度 如何？')


    while True:
        print("\n")
        print('-' * 150)
        print("^_^请提问：")
        question = input()
        my_query = q2s.get_sparql(question)
        #print('最终的查询语句:\n{}'.format(my_query))
        
        print('\n老八：')
        if my_query is not None:

            result = fuseki.get_sparql_result(my_query)
            #print(result)
            value = fuseki.get_sparql_result_value(result)

            # TODO 判断结果是否是布尔值，是布尔值则提问类型是"ASK"，回答“是”或者“不知道”。
            if isinstance(value, bool):
                if value is True:
                    print('Yes')
                else:
                    print('I don\'t know. :(')
            else:
                # TODO 查询结果为空，根据OWA，回答“不知道”
                if len(value) == 0:
                    if ('配料' in question):
                        print("这道菜好像不需要配料哦，试试问我其它问题哈。")
                    else:
                        print('这个我真是不知道，请再问个其它问题，例如：')
                        print('如何制作松鼠鱼？')
                elif len(value) == 1:
                    print(value[0])
                else:
                    output = ''
                    for v in value:
                        output += v + u'、'
                    print(output[0:-1])

        else:
            # TODO 自然语言问题无法匹配到已有的正则模板上，回答“无法理解”
            print('这个问题我真是无法回答。')
            print("如何制作红烧划水？/ 红烧划水的制作步骤是什么？")
            print("徽菜包含哪些菜品？")
            print("德州扒鸡的食材有哪些？")
            print("腊肠煲仔饭的原料是什么？")
            print('松鼠鱼的 特色/特点 是什么')
            print('蚂蚁上树的 口味/耗时/工艺/难度 如何')

        print('=' * 150)
