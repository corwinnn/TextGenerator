import argparse
import pickle
import sys
import re
from collections import defaultdict


def train(line, d, previous_word):
    """
    Записываем в словарь d слова из строчки line, учитывая последнее слово предыдущей строчки
    :param line: строка для тренировки
    :param d: словарь для записи
    :param previous_word: последнее слово предыдущей строки
    :return: последнее слово этой строки
    """
    line = previous_word + ' ' + line
    if args.lc:
        line = line.lower()
    words_list = re.findall('\w+', line)
    for i in range(len(words_list) - 1):
        if not words_list[i] in d:
            d[words_list[i]] = defaultdict(int)
        d[words_list[i]][words_list[i + 1]] += 1
    if len(words_list) > 0:
        previous_word = words_list[-1]
    else:
        previous_word = ''
    return previous_word


def read_from_file(given, model):
    """
    На данном тексте given тренируем программу, получая словарь. Кладем его в файл model.
    :param given: данный текст
    :param model: место для записи
    """
    d = dict()
    text = sys.stdin
    if given is not None:
        text = open(given, 'r', encoding='utf-8')
    word = ''
    for line in text:
        word = train(line, d, word)
    if model is not None:
        with open(model, 'wb') as f:
            pickle.dump(d, f)
    text.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--lc', action='store_true', help='transform to lower case')
    parser.add_argument('--input_dir', action='store', help='choose the directory with files for training')
    parser.add_argument('--model', action='store', help='choose the directory with files for dump', required=True)
    args = parser.parse_args()
    read_from_file(args.input_dir, args.model)
