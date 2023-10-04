# KBQA 智能问答系统

基于构建的中式八大菜系菜谱的知识图谱，设计知识库问答KBQA系统，根据提出的菜品相关的问题，系统自动给出答案，对于无法给出回答的情况系统也能进行回应。

## 文件夹结构
+ /external_dict：包含所有菜品和原料的实体列表entities_list.txt
+ /static: answer与index 两个分页面的静态资源、格式控制css文件
+ /templates： answer与index两个分页面的 html文件
+ query_main.py：KBQA主函数（本地）
+ app.py: KBQA主函数（基于flask框架）
+ jena_sparql_endpoint.py：启动jena_sparql服务
+ question2sparql.py：自然语言问题到SPARQL查询的转换
+ question_temp.py：自然语言到SPARQL的问题模板
+ word_tagging.py：中文分词，使用的是jieba

### **StartCommand**

* 启动 ***fuseki*** 框架 
`java -jar fuseki-server.jar`

* 启动 ***Django*** 项目
`python manage.py runserver 0.0.0.0:8080`

* 项目主页面网址
`http://127.0.0.1:8080/recipe_knowledge_graph/`