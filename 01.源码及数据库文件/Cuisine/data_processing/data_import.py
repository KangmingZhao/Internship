'''
将整合后的csv文件导入到neo4j数据库中
'''

from py2neo import Graph
graph = Graph("bolt://localhost:7687", auth=("neo4j", "12345678"))

dish_node_query = "LOAD CSV WITH HEADERS FROM 'file:///dish.csv' AS line MERGE (:菜品 { 菜品名: line.菜品名, 口味: line.口味, 工艺: line.工艺, 耗时: line.耗时, 难度: line.难度, 步骤: line.步骤})"
main_ingredient_node_query = "LOAD CSV WITH HEADERS FROM 'file:///main_ingredient.csv' AS line MERGE (:原料 {原料名: line.名字})"
secondary_ingredient_node_query = "LOAD CSV WITH HEADERS FROM 'file:///secondary_ingredient.csv' AS line MERGE (:原料 {原料名: line.名字})"
condiment_node_query = "LOAD CSV WITH HEADERS FROM 'file:///condiment.csv' AS line MERGE (:原料 {原料名: line.名字})"
node_query = "foreach(菜系名 in split('浙菜，闽菜，苏菜，鲁菜，川菜，粤菜，湘菜，徽菜','，') | create(n:菜系{菜系名:菜系名}))"
rel1_query = "LOAD CSV WITH HEADERS FROM 'file:///cuisine_dish.csv' AS line MATCH (s:菜品 {菜品名: line.菜品名}) MATCH (t:菜系 {菜系名: line.菜系}) CREATE (s)-[:属于]->(t)"
rel2_query = "LOAD CSV WITH HEADERS FROM 'file:///ingredient_amount.csv' AS line OPTIONAL MATCH (s:原料 {原料名: line.原料名}) OPTIONAL MATCH (t:菜品 {菜品名: line.菜品名}) WITH s, t, line WHERE s IS NOT NULL AND t IS NOT NULL MERGE (s)-[:用量{用量:line.用量}]->(t)"
# rel3_query = "LOAD CSV WITH HEADERS FROM 'file:///ingredient_amount.csv' AS line OPTIONAL MATCH (s:原料 {辅料名: line.原料名}) OPTIONAL MATCH (t:菜品 {菜品名: line.菜品名}) CREATE (s)-[:用量{用量:line.用量}]->(t)"
# rel4_query = "LOAD CSV WITH HEADERS FROM 'file:///ingredient_amount.csv' AS line OPTIONAL MATCH (s:原料 {调料名: line.原料名}) OPTIONAL MATCH (t:菜品 {菜品名: line.菜品名}) CREATE (s)-[:用量{用量:line.用量}]->(t)"
graph.run('match (n) optional match (n)-[r]-() delete n,r')
graph.run(dish_node_query)
graph.run(main_ingredient_node_query)
graph.run(secondary_ingredient_node_query)
graph.run(condiment_node_query)
graph.run(node_query)
graph.run(rel1_query)
graph.run(rel2_query)
# graph.run(rel3_query)
# graph.run(rel4_query)
# LOAD CSV WITH HEADERS FROM 'file:///your_file.csv' AS row
# OPTIONAL MATCH (source:Node {id: row.source_id})
# OPTIONAL MATCH (target:Node {id: row.target_id})
# WITH source, target, row
# WHERE source IS NOT NULL AND target IS NOT NULL
# MERGE (source)-[r:RELATIONSHIP_TYPE]->(target)
# SET r.property = row.relationship_property
