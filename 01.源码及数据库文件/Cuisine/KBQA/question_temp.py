"""

设置问题模板，为每个模板设置对应的SPARQL语句，并提供如下模板：

1. 如何制作某道菜品？
2. 某道菜品需要哪些原料？
3. 某个菜系包含哪些具体菜品？
4. 某道菜品属于哪个菜系
5. 某个菜品的特色是什么？
6. 某个菜品的制作步骤是什么？

...

还可以自己定义其他的匹配规则。

"""
from refo import finditer, Predicate, Star, Any, Disjunction
import re

# TODO SPARQL前缀和模板

SPARQL_PREXIX = u"""
PREFIX : <http://kg.course/ai-food-time/>
"""

SPARQL_SELECT_TEM = u"{prefix}\n" + \
    u"SELECT DISTINCT {select} WHERE {{\n" + \
    u"{expression}\n" + \
    u"}}\n"

SPARQL_COUNT_TEM = u"{prefix}\n" + \
    u"SELECT COUNT({select}) WHERE {{\n" + \
    u"{expression}\n" + \
    u"}}\n"

SPARQL_ASK_TEM = u"{prefix}\n" + \
    u"ASK {{\n" + \
    u"{expression}\n" + \
    u"}}\n"

INDENT = "    "


class W(Predicate):
    def __init__(self, token=".*", pos=".*"):
        self.token = re.compile(token + "$")
        self.pos = re.compile(pos + "$")
        super(W, self).__init__(self.match)

    def match(self, word):
        m1 = self.token.match(word.token)
        m2 = self.pos.match(word.pos)
        return m1 and m2


class Rule(object):
    def __init__(self, condition_num, condition=None, action=None):
        assert condition and action
        self.condition = condition
        self.action = action
        self.condition_num = condition_num

    def apply(self, sentence):
        matches = []
        for m in finditer(self.condition, sentence):
            i, j = m.span()
            matches.extend(sentence[i:j])

        return self.action(matches), self.condition_num


class KeywordRule(object):
    def __init__(self, condition=None, action=None):
        assert condition and action
        self.condition = condition
        self.action = action

    def apply(self, sentence):
        matches = []
        for m in finditer(self.condition, sentence):
            i, j = m.span()
            matches.extend(sentence[i:j])
        if len(matches) == 0:
            return None
        else:
            return self.action()


class QuestionSet:
    def __init__(self):
        pass

    @staticmethod
    def has_basic_food_info_question(word_objects):
        """
        食材的基本信息是什么
        :param word_objects:
        :return:
        """
        keyword = None
        for r in food_basic_keyword_rules:
            keyword = r.apply(word_objects)
            if keyword is not None:
                break

        select = u"?x"
        sparql = None
        for w in word_objects:
            if w.pos == pos_food:
                e = u"?s :名称 '{food}'. \n" \
                    u"?s {keyword} ?x.".format(food=w.token, keyword=keyword)

                sparql = SPARQL_SELECT_TEM.format(
                    prefix=SPARQL_PREXIX, select=select, expression=e)

                break

        return sparql


class PropertyValueSet:
    def __init__(self):
        pass
    
    @staticmethod
    def return_material_value():
        return u':选材'

    @staticmethod
    def return_main_value():
        return u':主料'

    @staticmethod
    def return_excipient_value():
        return u':辅料'

    @staticmethod
    def return_ingredient_value():
        return u':配料'

    @staticmethod
    def return_makesteps_value():
        return u':制作步骤'

    @staticmethod
    def return_features_value():
        return u':特色'
    
    @staticmethod
    def return_taste_value():
        return u':口味'
    
    @staticmethod
    def return_craft_value():
        return u':工艺'
    
    @staticmethod
    def return_time_value():
        return u':耗时'
    
    @staticmethod
    def return_difficulty_value():
        return u':难度'

    @staticmethod
    def return_cuisine_value():
        return u':属于'

    @staticmethod
    def return_include_value():
        return u':包含'


# TODO 定义关键词
pos_food = "ai"
food_entity = (W(pos=pos_food))


makestep = (W("制作") + W("步骤") | W("做法") | W("烹饪") + W("方法") | W("制作") + W("方法") | W("制作"))
material = (W("取材") | W("原料") | W("用到") | W("选材") | W("食材"))
main_component = (W("主料") | W("主要原料"))
excipient = (W("辅料"))
ingredient = (W("配料"))
feature = (W("特色") | W("特点"))
taste = (W("口味"))
craft = (W("工艺"))
time = (W("耗时"))
difficulty = (W("难度"))
what = (W("哪些") | W("什么"))
how = (W("怎样") | W("如何"))
make = W("制作")
cuisine = (W("属于"))
include = (W("包含")|W("包括"))

food_basic = (makestep | material | main_component | excipient | ingredient | feature| taste | craft | time | difficulty | cuisine |include)


rules = [
    Rule(condition_num=2, condition=(food_entity + Star(Any(), greedy=False) + food_basic + Star(Any(), greedy=False)) | (Star(Any(), greedy=False) + make + Star(Any(), greedy=False) + food_entity + Star(Any(), greedy=False)), action=QuestionSet.has_basic_food_info_question),
]

# TODO 具体的属性词匹配规则

food_basic_keyword_rules = [

    KeywordRule(condition=food_entity + Star(Any(), greedy=False) + material +
                Star(Any(), greedy=False), action=PropertyValueSet.return_material_value),
    KeywordRule(condition=food_entity + Star(Any(), greedy=False) + makestep +
                Star(Any(), greedy=False), action=PropertyValueSet.return_makesteps_value),
    KeywordRule(condition=food_entity + Star(Any(), greedy=False) + main_component +
                Star(Any(), greedy=False), action=PropertyValueSet.return_main_value),
    KeywordRule(condition=food_entity + Star(Any(), greedy=False) + excipient +
                Star(Any(), greedy=False), action=PropertyValueSet.return_excipient_value),
    KeywordRule(condition=food_entity + Star(Any(), greedy=False) + ingredient +
                Star(Any(), greedy=False), action=PropertyValueSet.return_ingredient_value),
    KeywordRule(condition=food_entity + Star(Any(), greedy=False) + feature +
                Star(Any(), greedy=False), action=PropertyValueSet.return_features_value),
    KeywordRule(condition=makestep + Star(Any(), greedy=False) + food_entity +
                Star(Any(), greedy=False), action=PropertyValueSet.return_makesteps_value),

    KeywordRule(condition=food_entity + Star(Any(), greedy=False) + taste +
                Star(Any(), greedy=False), action=PropertyValueSet.return_taste_value),
    KeywordRule(condition=food_entity + Star(Any(), greedy=False) + craft +
                Star(Any(), greedy=False), action=PropertyValueSet.return_craft_value),
    KeywordRule(condition=food_entity + Star(Any(), greedy=False) + time +
                Star(Any(), greedy=False), action=PropertyValueSet.return_time_value),
    KeywordRule(condition=food_entity + Star(Any(), greedy=False) + difficulty +
                Star(Any(), greedy=False), action=PropertyValueSet.return_difficulty_value),

    KeywordRule(condition=food_entity + Star(Any(), greedy=False) + cuisine +
                Star(Any(), greedy=False), action=PropertyValueSet.return_cuisine_value),
    KeywordRule(condition=food_entity + Star(Any(), greedy=False) + include +
                Star(Any(), greedy=False), action=PropertyValueSet.return_include_value),
]
