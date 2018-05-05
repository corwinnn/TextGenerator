import argparse
import pickle
import sys
import re
import os
from collections import defaultdict


def train(line, words_dict, previous_word):
    """
    Записываем в словарь words_dict слова из строчки line,
    учитывая последнее слово предыдущей строчки
    :param line: строка для тренировки
    :param words_dict: словарь для записи
    :param previous_word: последнее слово предыдущей строки
    :return: последнее слово этой строки
    """
    line = previous_word + ' ' + line
    if args.lc:
        line = line.lower()
    words_list = re.findall(r'\w+', line)
    for i in range(len(words_list) - 1):
        if not words_list[i] in words_dict:
            words_dict[words_list[i]] = defaultdict(int)
        words_dict[words_list[i]][words_list[i + 1]] += 1
    if len(words_list) > 0:
        previous_word = words_list[-1]
    else:
        previous_word = ''
    return previous_word


def get_dict_from_dir_to_model(given_dir, file_for_model):
    """
    На данном тексте из директории given_dir тренируем программу,
    получая словарь. Кладем его в файл file_for_model.
    :param given_dir: данная директория
    :param file_for_model: место для записи модели
    """
    words_dict = dict()
    if given_dir is not None:
        for file in os.listdir(given_dir):
            if file.endswith(".txt"):
                input_file = given_dir + "/" + str(file)
                with open(input_file, 'r', encoding='utf-8') as text:
                    word = ''
                    for line in text:
                        word = train(line, words_dict, word)
    else:
        word = ''
        for line in sys.stdin:
            word = train(line, words_dict, word)
    with open(file_for_model, 'wb') as f:
        pickle.dump(words_dict, f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--lc', action='store_true',
                        help='transform to lower case')
    parser.add_argument('--input_dir', action='store',
                        help='choose the directory with files for training')
    parser.add_argument('--model', action='store',
                        help='choose the directory with files for dump',
                        required=True)
    args = parser.parse_args()
    get_dict_from_dir_to_model(args.input_dir, args.model)
