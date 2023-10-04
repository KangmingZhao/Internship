'''
  整合所有的csv文件并保存
'''

import pandas as pd

# 读取第一个CSV文件
cuisine_dish_df1 = pd.read_csv(r'D:\PYZ\PT(Shi_xi_shi_xun)\Group\menu_tasks\data\zhe\cuisine_dish.csv')
cuisine_dish_df2 = pd.read_csv(r'D:\PYZ\PT(Shi_xi_shi_xun)\Group\menu_tasks\data\min\cuisine_dish.csv')
cuisine_dish_df3 = pd.read_csv(r'D:\PYZ\PT(Shi_xi_shi_xun)\Group\menu_tasks\data\数据汇总\川菜、粤菜\数据\cuisine_dish.csv')
cuisine_dish_df4 = pd.read_csv(r'D:\PYZ\PT(Shi_xi_shi_xun)\Group\menu_tasks\data\数据汇总\苏菜、鲁菜\table\cuisine_dish.csv')
cuisine_dish_df5 = pd.read_csv(r'D:\PYZ\PT(Shi_xi_shi_xun)\Group\menu_tasks\data\数据汇总\湘菜，徽菜\数据\cuisine_dish.csv')
# 读取第二个CSV文件
dish_df1 = pd.read_csv(r'D:\PYZ\PT(Shi_xi_shi_xun)\Group\menu_tasks\data\zhe\dish.csv')
dish_df2 = pd.read_csv(r'D:\PYZ\PT(Shi_xi_shi_xun)\Group\menu_tasks\data\min\dish.csv')
dish_df3 = pd.read_csv(r'D:\PYZ\PT(Shi_xi_shi_xun)\Group\menu_tasks\data\数据汇总\川菜、粤菜\数据\dish.csv')
dish_df4 = pd.read_csv(r'D:\PYZ\PT(Shi_xi_shi_xun)\Group\menu_tasks\data\数据汇总\苏菜、鲁菜\table\dish.csv')
dish_df5 = pd.read_csv(r'D:\PYZ\PT(Shi_xi_shi_xun)\Group\menu_tasks\data\数据汇总\湘菜，徽菜\数据\dish.csv')
# 读取第三个CSV文件
ingredient_amount_df1 = pd.read_csv(r'D:\PYZ\PT(Shi_xi_shi_xun)\Group\menu_tasks\data\zhe\ingredient_amount.csv')
ingredient_amount_df2 = pd.read_csv(r'D:\PYZ\PT(Shi_xi_shi_xun)\Group\menu_tasks\data\min\ingredient_amount.csv')
ingredient_amount_df3 = pd.read_csv(r'D:\PYZ\PT(Shi_xi_shi_xun)\Group\menu_tasks\data\数据汇总\川菜、粤菜\数据\ingre_amount_l.csv')
ingredient_amount_df4 = pd.read_csv(r'D:\PYZ\PT(Shi_xi_shi_xun)\Group\menu_tasks\data\数据汇总\苏菜、鲁菜\table\ingredient_amount.csv')
ingredient_amount_df5 = pd.read_csv(r'D:\PYZ\PT(Shi_xi_shi_xun)\Group\menu_tasks\data\数据汇总\湘菜，徽菜\数据\ingredient_amount.csv')
# 读取第四个CSV文件
main_ingredient_df1 = pd.read_csv(r'D:\PYZ\PT(Shi_xi_shi_xun)\Group\menu_tasks\data\zhe\main_ingredient.csv')
main_ingredient_df2 = pd.read_csv(r'D:\PYZ\PT(Shi_xi_shi_xun)\Group\menu_tasks\data\min\main_ingredient.csv')
main_ingredient_df3 = pd.read_csv(r'D:\PYZ\PT(Shi_xi_shi_xun)\Group\menu_tasks\data\数据汇总\川菜、粤菜\数据\main_ingredients.csv')
main_ingredient_df4 = pd.read_csv(r'D:\PYZ\PT(Shi_xi_shi_xun)\Group\menu_tasks\data\数据汇总\苏菜、鲁菜\table\main_ingredients.csv')
main_ingredient_df5 = pd.read_csv(r'D:\PYZ\PT(Shi_xi_shi_xun)\Group\menu_tasks\data\数据汇总\湘菜，徽菜\数据\main_ingredient.csv')
# 读取第五个CSV文件
condiment_df1 = pd.read_csv(r'D:\PYZ\PT(Shi_xi_shi_xun)\Group\menu_tasks\data\zhe\spices.csv')
condiment_df2 = pd.read_csv(r'D:\PYZ\PT(Shi_xi_shi_xun)\Group\menu_tasks\data\min\spices.csv')
condiment_df3 = pd.read_csv(r'D:\PYZ\PT(Shi_xi_shi_xun)\Group\menu_tasks\data\数据汇总\川菜、粤菜\数据\condiment.csv')
condiment_df4 = pd.read_csv(r'D:\PYZ\PT(Shi_xi_shi_xun)\Group\menu_tasks\data\数据汇总\苏菜、鲁菜\table\condiment.csv')
condiment_df5 = pd.read_csv(r'D:\PYZ\PT(Shi_xi_shi_xun)\Group\menu_tasks\data\数据汇总\湘菜，徽菜\数据\spices.csv')
# 读取第六个CSV文件
secondary_ingredient_df1 = pd.read_csv(r'D:\PYZ\PT(Shi_xi_shi_xun)\Group\menu_tasks\data\zhe\secondary_ingredient.csv')
secondary_ingredient_df2 = pd.read_csv(r'D:\PYZ\PT(Shi_xi_shi_xun)\Group\menu_tasks\data\min\secondary_ingredient.csv')
secondary_ingredient_df3 = pd.read_csv(r'D:\PYZ\PT(Shi_xi_shi_xun)\Group\menu_tasks\data\数据汇总\川菜、粤菜\数据\secondary_ingredients.csv')
secondary_ingredient_df4 = pd.read_csv(r'D:\PYZ\PT(Shi_xi_shi_xun)\Group\menu_tasks\data\数据汇总\苏菜、鲁菜\table\secondary_ingredients.csv')
secondary_ingredient_df5 = pd.read_csv(r'D:\PYZ\PT(Shi_xi_shi_xun)\Group\menu_tasks\data\数据汇总\湘菜，徽菜\数据\secondary_ingredient.csv')

# 合并数据
cuisine_dish_merged_df = pd.concat([cuisine_dish_df1, cuisine_dish_df2, cuisine_dish_df3, cuisine_dish_df4, cuisine_dish_df5]).drop_duplicates()
dish_merged_df = pd.concat([dish_df1, dish_df2, dish_df3, dish_df4, dish_df5]).drop_duplicates()
ingredient_amount_merged_df = pd.concat([ingredient_amount_df1, ingredient_amount_df2, ingredient_amount_df3, ingredient_amount_df4, ingredient_amount_df5]).drop_duplicates()
main_ingredient_merged_df = pd.concat([main_ingredient_df1, main_ingredient_df2, main_ingredient_df3, main_ingredient_df4, main_ingredient_df5]).drop_duplicates()
condiment_merged_df = pd.concat([condiment_df1, condiment_df2, condiment_df3, condiment_df4, condiment_df5]).drop_duplicates()
secondary_ingredient_merged_df = pd.concat([secondary_ingredient_df1, secondary_ingredient_df2, secondary_ingredient_df3, secondary_ingredient_df4, secondary_ingredient_df5]).drop_duplicates()

# 导出为CSV
cuisine_dish_merged_df.to_csv(r'D:\PYZ\PT(Shi_xi_shi_xun)\Group\menu_tasks\data\merged_file\cuisine_dish.csv', index=False)
dish_merged_df.to_csv(r'D:\PYZ\PT(Shi_xi_shi_xun)\Group\menu_tasks\data\merged_file\dish.csv', index=False)
ingredient_amount_merged_df.to_csv(r'D:\PYZ\PT(Shi_xi_shi_xun)\Group\menu_tasks\data\merged_file\ingredient_amount.csv', index=False)
main_ingredient_merged_df.to_csv(r'D:\PYZ\PT(Shi_xi_shi_xun)\Group\menu_tasks\data\merged_file\main_ingredient.csv', index=False)
condiment_merged_df.to_csv(r'D:\PYZ\PT(Shi_xi_shi_xun)\Group\menu_tasks\data\merged_file\condiment.csv', index=False)
secondary_ingredient_merged_df.to_csv(r'D:\PYZ\PT(Shi_xi_shi_xun)\Group\menu_tasks\data\merged_file\secondary_ingredient.csv', index=False)
