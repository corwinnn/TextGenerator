import pickle
import argparse
import random
import sys
import numpy as np


def init(dump):
    """
    Достает из данного файла словарь, полученный при тренировке.
    Нормирует значения, чтобы получалась вероятность.
    :param dump: даннный файл
    :return: полученный словарь
    """
    with open(dump, 'rb') as file:
        words_dict = pickle.load(file)
        for word in words_dict:
            word_number = sum(words_dict[word].values())
            for second_word in words_dict[word]:
                words_dict[word][second_word] /= word_number
    return words_dict


def generate(model, seed, length, output, symbols_in_line=20):
    """
    Генерирует последовательность слов длины length.
    Начальное слово - seed.
    Словарь лежит в model.
    Результат выводит в output.
    :param symbols_in_line: кол-во символов помещающихся в строку
    :param model: файл со словарем
    :param seed: начальное слово
    :param length: длина генерируемой последовательности
    :param output: куда записать ответ
    """
    words_dict = init(model)
    words = list(words_dict.keys())
    if seed is not None:
        word = seed
    else:
        word = random.choice(words)
    if output is not None:
        out = open(output, 'w', encoding='utf-8')
    else:
        out = sys.stdout        
    text = ''
    for i in range(length):
        text = text + word + ' '
        if i % symbols_in_line == 0 and i > 0:
            text += '\n'
            out.write(text)
            text = ''
        if word not in words_dict:
            word = random.choice(words)
        else:
            word = np.random.choice(list(words_dict[word].keys()),
                                    1, p=list(words_dict[word].values()))[0]
    out.write(text)
    out.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', action='store', type=str, help='first word')
    parser.add_argument('--length', action='store',
                        type=int, help='length', required=True)
    parser.add_argument('--output', action='store',
                        help='choose the directory to write the text')
    parser.add_argument('--model', action='store',
                        help='choose the directory with files'
                        ' for dump to programm',
                        required=True)
    args = parser.parse_args()
    generate(args.model, args.seed, args.length, args.output)
