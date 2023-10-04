from py2neo import Graph
import pandas as pd
from .db import query_neo4j
from collections import Counter


def get_data(random = 0,how_many_dish = 1):

    query = None
    if random:
        query = """
        MATCH (c: 菜品)-[`属于`: 属于]->(`菜系`: 菜系)
        WITH `菜系`, COLLECT(c)[..%s] AS `菜品`, rand() AS random
        ORDER BY random
        MATCH (c: 菜品)<-[`用量`: 用量]-(i: 原料)
        WHERE c IN `菜品` 
        RETURN [(c)-[属于]->(菜系) | `属于`] AS `属于`, `用量`, `菜系`, `菜品`, COLLECT(i) AS `原料`
        """%how_many_dish
    else:
        query = """
        MATCH (c: 菜品)-[`属于`: 属于]->(`菜系`: 菜系)
        WITH `菜系`, COLLECT(c)[..%s] AS `菜品` 
        MATCH (c: 菜品)<-[`用量`: 用量]-(i: 原料)
        WHERE c IN `菜品`
        RETURN [(c)-[属于]->(菜系) | `属于`] AS `属于`, `用量`, `菜系`, `菜品`, COLLECT(i) AS `原料`
        """%how_many_dish

    result = query_neo4j(query, encoding='utf-8')
    cuision = []
    dish = []
    ingredient = []
    id_name = {}
    cuision_dish = []
    ingredient_dish = []
    ingredient_count = []
    for record in result:
        cuision_node = record['菜系']
        cuision.append({'id': cuision_node.identity, 'cuision_name': cuision_node['菜系名']})
        for re in record['菜品']:
            dish_node = re
            dish.append({'id': dish_node.identity, 'dish_name': dish_node['菜品名'], '口味': dish_node['口味'], '工艺': dish_node['工艺'], '耗时': dish_node['耗时'], '难度': dish_node['难度'], '步骤': dish_node['步骤']})
        for re in record['原料']:
            ingredient_node = re
            ingredient.append({'id': ingredient_node.identity, 'ingredient_name': ingredient_node['原料名']})
            id_name['%d' % ingredient_node.identity] = ingredient_node['原料名']
        for re in record['属于']:
            cuision_dish_rel = re
            cuision_dish.append({'source': cuision_dish_rel.start_node.identity, 'target': cuision_dish_rel.end_node.identity})
        ingredient_dish_rel = record['用量']
        ingredient_dish.append({'source': ingredient_dish_rel.start_node.identity, 'target': ingredient_dish_rel.end_node.identity, '用量': ingredient_dish_rel['用量']})
    # 统计原料使用的次数
    counter = Counter(item['source'] for item in ingredient_dish)
    for element, count in counter.items():
        ingredient_count.append({'原料名': id_name['%d' % element], '使用次数': count})
        
    ingredient_count = sorted(ingredient_count, key=lambda x: x['使用次数'], reverse=True)[:10]
    return (drop_duplicates(cuision), drop_duplicates(dish), drop_duplicates(ingredient), drop_duplicates(cuision_dish), drop_duplicates(ingredient_dish), ingredient_count)


def drop_duplicates(lst):
    df = pd.DataFrame(lst)
    unique_df = df.drop_duplicates().reset_index(drop=True)
    unique_list = unique_df.to_dict('records')
    return unique_list

