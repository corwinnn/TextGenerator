import pickle
import argparse
import random
import sys
import numpy as np


def init(dump):
    with open(dump, 'rb') as file:
        d = pickle.load(file)
        for word in d:
            kol = 0
            for s_word in d[word]:
                kol += d[word][s_word]
            for s_word in d[word]:
                d[word][s_word] /= kol
    return d


def generate(model, seed, length, output):
    d = init(model)
    words = list(d.keys())
    word = random.choice(words)
    if seed is not None:
        word = seed
    out = sys.stdin
    if output is not None:
        out = open(output, 'w', encoding='utf-8')
    text = ''
    for i in range(length):
        text = text + word + ' '
        if i % 20 == 0 and i > 0:
            text += '\n'
        if word not in d:
            word = random.choice(words)
        else:
            word = np.random.choice(list(d[word].keys()), 1, p=list(d[word].values()))[0]
    out.write(text)
    out.close()


parser = argparse.ArgumentParser()
parser.add_argument('--seed', action='store', type=str, help='first word')
parser.add_argument('--length', action='store', type=int, help='length', required=True)
parser.add_argument('--output', action='store', help='choose the directory to write the text')
parser.add_argument('--model', action='store', help='choose the directory with files for dump to programm', required=True)
args = parser.parse_args()
generate(args.model, args.seed, args.length, args.output)
# generate('Qtest0.txt', 'Just', 100, 'Wtest0.txt')
