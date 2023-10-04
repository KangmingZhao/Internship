from flask import Flask, render_template, request
import jena_sparql_endpoint
import question2sparql

#app = Flask(__name__)
app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/answer', methods=['POST'])
def answer():
    question = request.form['question']

    fuseki = jena_sparql_endpoint.JenaFuseki()
    q2s = question2sparql.Question2Sparql(
        [r'./external_dict/entities_list.txt'])
    my_query = q2s.get_sparql(question)

    answer = ""
    if my_query is not None:

        result = fuseki.get_sparql_result(my_query)
        value = fuseki.get_sparql_result_value(result)
        
        # TODO 判断结果是否是布尔值，是布尔值则提问类型是"ASK"，回答“是”或者“不知道”。
        if isinstance(value, bool):
            if value is True:
                answer = 'Yes'
            else:
                answer = 'I don\'t know. :('
        else:
            # TODO 查询结果为空，根据OWA，回答“不知道”
            if len(value) == 0:
                if '配料' in question:
                    answer = "这道菜好像不需要配料哦，请尝试问我其他问题哈。"
                else:
                    answer = '这个我真是不知道，请再问个其他问题，例如：如何制作松鼠鱼？'
            elif len(value) == 1:
                answer = value[0]
            else:
                for v in value:
                    answer += v + u'、'
                print(answer[0:-1])

    else:
        # TODO 自然语言问题无法匹配到已有的正则模板上，回答“无法理解”
        answer = '这个问题我真是无法回答。'

    return render_template('answer.html', question=question, answer=answer)

if __name__ == '__main__':
    app.run()
