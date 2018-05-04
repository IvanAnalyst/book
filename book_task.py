from collections import Counter
from abc import ABC, abstractmethod
from itertools import islice


class TextCommonPairs(ABC):
    def __init__(self, filename='book.txt'):
        self.text = self.get_text(filename)

    @staticmethod
    def get_text(filename):
        with open(filename) as f:
            text = f.read().split()
        return text

    @staticmethod
    def get_pairs(text):
        for w1, w2 in zip(text[:-1:], text[1::]):
            yield(w1, w2)

    @abstractmethod
    def get_most_common_pairs(self, common_pairs_cnt=5):
        pass

    
class TextCommonPairs_1(TextCommonPairs):
    @staticmethod
    def get_pairs(text):
        return zip(islice(text, None), islice(text, 1, None))

    def get_most_common_pairs(self, common_pairs_cnt=5):
        most_common_word = Counter(self.text).most_common(1)[0][0]

        pairs = [pair for pair in self.get_pairs(self.text) \
                if most_common_word in pair]
        most_common_pairs_info = Counter(pairs).most_common(common_pairs_cnt)
        most_common_pairs = [i[0] for i in most_common_pairs_info]

        return most_common_pairs


class TextCommonPairs_2(TextCommonPairs):
    @staticmethod
    def update_dict(d, pair):
        for word in pair:
            if word in d:
                d[word].append(pair)
                continue
            d[word] = [pair]

    def get_most_common_pairs(self, common_pairs_cnt=5):
        d = {}
        for p in self.get_pairs(self.text):
            self.update_dict(d, p)

        popular_word_pairs = sorted(d.items(), 
            key=lambda x: len(x[1]), reverse=True)[0][1]
        most_common_pairs_info = Counter(popular_word_pairs).most_common(
            common_pairs_cnt)
        most_common_pairs = [i[0] for i in most_common_pairs_info]

        return most_common_pairs


class TextCommonPairs_3(TextCommonPairs):
    @staticmethod
    def update_dict(d, pair):
        for word in pair:
            if word in d:
                pair_cnt = d[word]['pairs'].get(pair, 0) + 1
                d[word]['pairs'][pair] = pair_cnt
                d[word]['cnt'] += 1
                continue
            d[word] = {'pairs': {pair : 1}, 'cnt': 1}

    def get_most_common_pairs(self, common_pairs_cnt=5):
        d = {}
        for p in self.get_pairs(self.text):
            self.update_dict(d, p)

        most_common_pairs_info = sorted(d.items(), 
            key = lambda x: x[1]['cnt'])[-1][1]['pairs']
        sorted_most_common_pairs_info = sorted(most_common_pairs_info.items(), 
            key=lambda x: x[1], reverse=True)[:common_pairs_cnt]
        most_common_pairs = [i[0] for i in sorted_most_common_pairs_info]

        return most_common_pairs
