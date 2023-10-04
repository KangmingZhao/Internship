'''
将所有涉及到的实体都作为词语生成 entities_list
'''

import pandas as pd
import os


df_dishes = pd.read_csv(r"../data/dish.csv", usecols=["菜品名"])
df_ingredients = pd.read_csv(r"../data/ingredient_amount.csv", usecols=["原料名"])
df_cuisine = pd.read_csv(r"../data/cuisine.csv", usecols=["菜系名"])

merged_series = pd.concat([df_dishes["菜品名"], df_ingredients["原料名"], df_cuisine["菜系名"]],axis=0)

# 去重操作
df_merged_unique = merged_series.drop_duplicates()

# 将合并后的Series保存为TXT文件
merged_series.to_csv(r"./entities_list.txt", index=False, header=False)

with open(r"./entities_list.txt", "r+",encoding='utf-8') as file:
    lines = file.readlines()
    file.seek(0)  # 移动文件指针到文件开头
    for line in lines:
        file.write(line.strip() + ' ai\n')

print("合并成功")