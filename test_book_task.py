import os
from re import search
from random import randrange, choice
from timeit import default_timer as timer
from contextlib import contextmanager
from string import ascii_lowercase as letters
from itertools import product

from book_task import *


# def get_uniq_words(cnt):
#     for triple in islice(product(*[list(letters)] * 3), cnt):
#             yield ''.join(triple)


def get_uniq_words(cnt):
    return [''.join(triple) for triple in islice(product(*[list(letters)] * 3), cnt)]


def get_book(filename='book.txt', words_cnt=10**6, uniq_words_cnt=10**3):
    words = get_uniq_words(uniq_words_cnt)
    with open(filename, 'w') as f:
        for i in range(words_cnt):
            f.write('{} '.format(choice(words)))
    return filename


@contextmanager
def timeit_context(name='It'):
    start = timer()
    yield
    elapsed_time = timer() - start
    print('{} finished in {} ms'.format(name, int(elapsed_time * 1000)))


def purge(dir, pattern):
    for f in os.listdir(dir):
        if search(pattern, f) and os.path.isfile(dir + '/' + f):
            os.remove(os.path.join(dir, f))


def test_it(with_new_books=False, test_dir='test'):
    book_name_beginning = 'book__'

    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
    if with_new_books:
        purge(test_dir, book_name_beginning)

    for realization in (TextCommonPairs_1, TextCommonPairs_2, TextCommonPairs_3):
        for words_cnt_power in range(5, 8):
            for uniq_words_cnt in (5, 10, 20):
                book_name = '{}10_{}__{}.txt'.format(
                    book_name_beginning, words_cnt_power, uniq_words_cnt)
                fname = test_dir + '/' + book_name
                tcp = realization(fname) if os.path.isfile(fname) \
                        else realization(get_book(fname, words_cnt=10**words_cnt_power, 
                                                uniq_words_cnt=uniq_words_cnt))

                with timeit_context(
                    name='Test with {} words where {} is uniqs'.format(
                        10**words_cnt_power, uniq_words_cnt)):
                    tcp.get_most_common_pairs()
            print()
        print('=' * 70 + '\n')


test_it(True)
