from django.shortcuts import render
from django.http import HttpResponse
from .db import query_neo4j
import json
from .mytask import get_data
from django.core.cache import cache


# Create your views here.
def index(request):
    return HttpResponse('Hello World.')

def entry_view(request,methods = ['GET','POST']):
    return render(request, 'neo4j/entry_view.html')


def test_data():
    data = {
        'cuision': [
            {'id': 1, 'cuision_name': '川菜'},
            {'id': 2, 'cuision_name': '粤菜'},
            ],
        'dish': [
            {'id': 3, 'dish_name': '答辩', '口味': '辣'},
            {'id': 4, 'dish_name': '苟史', '口味': '香'}
            ],
        'ingredient': [
            {'id': 5, 'ingredient_name': '水'},
            {'id': 6, 'ingredient_name': '无机盐'}
            ],
        'cuision_dish': [
            {'source': 3, 'target': 1},
            {'source': 4, 'target': 2},
            {'source': 4, 'target': 1},
            ],
        'ingredient_dish': [
            {'source': 5, 'target': 3, '用量': '一勺'},
            {'source': 6, 'target': 4, '用量': '一勺'},
            {'source': 5, 'target': 4, '用量': '一勺'}
            ]
    }
    return data


def main_view(request,methods = ['GET','POST']):
    #内置bgm和背景
    #这里进行查询操作。我需要通过查询得到一个表。这个表最好和你的csv文件是一个格式的。
    #data = test_data()
    #(cuision,dish,ingredient,cuision_dish,ingredient_dish) = get_data()
    #data = {"cuision": cuision,"dish": dish,'ingredient':ingredient,'cuision_dish':cuision_dish,'ingredient_dish':ingredient_dish}

    how_many_dishes_per_cuision = request.POST.get('dish-num-input')
    if not how_many_dishes_per_cuision:
        cached_data = cache.get('data')  # 检查缓存是否存在
        if cached_data:
            return render(request, 'neo4j/main_view.html', {'data': cached_data})
        else:
            (cuision, dish, ingredient, cuision_dish, ingredient_dish, ingredient_count) = get_data()
            data = {"cuision": cuision, "dish": dish, 'ingredient': ingredient, 'cuision_dish': cuision_dish, 'ingredient_dish': ingredient_dish, 'ingredient_count': ingredient_count}
            json_data = json.dumps(data)
            cache.set('data', json_data)  # 将结果存入缓存中
            return render(request, 'neo4j/main_view.html', {'data': json_data})
    else:
        (cuision, dish, ingredient, cuision_dish, ingredient_dish, ingredient_count) = get_data(1, how_many_dishes_per_cuision)
        # return HttpResponse(get_data(1,how_many_dishes_per_cuision))
        data = {"cuision": cuision, "dish": dish, 'ingredient': ingredient, 'cuision_dish': cuision_dish, 'ingredient_dish': ingredient_dish, 'ingredient_count': ingredient_count}
        json_data = json.dumps(data)
        cache.set('data', json_data)  # 将结果存入缓存中
        return render(request, 'neo4j/main_view.html', {'data': json_data})
            


    #return render(request,'neo4j/main_view.html',{'data': json_data})
