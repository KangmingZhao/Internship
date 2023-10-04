'''
导入jieba与外部词典进行分词
'''

import jieba
import jieba.posseg as pseg


class Word(object):
    def __init__(self, token, pos):
        self.token = token
        self.pos = pos


class Tagger:
    def __init__(self, dict_paths):
        # TODO 加载外部词典
        for p in dict_paths:
            jieba.load_userdict(p)

        # TODO jieba不能正确切分的词语，手动调整频率。
        jieba.suggest_freq(('制作', '方法'), True)
        jieba.suggest_freq(('制作'), True)
        jieba.suggest_freq(('如何', '制作'), True)
        
    def get_word_objects(self,sentence):
        # type: (str) -> list
        """
        把自然语言转为Word对象
        :param sentence:
        :return:
        """
        return [Word(word, tag) for word, tag in pseg.cut(sentence)]


# TODO 用于测试
if __name__ == '__main__':
    tagger = Tagger([r'./external_dict/entities_list.txt'])
    while True:
        s = input()
        for i in tagger.get_word_objects(s):
            print(i.token, i.pos)
