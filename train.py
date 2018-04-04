import argparse
import pickle
import fileinput
import sys


def train(line, d, previous_word):
    line_copy = ''
    if args.lc:
        line = line.lower()
    for symb in line:
        if symb.isalpha() or symb == ' ':
            line_copy += symb
    line_copy = previous_word + ' ' + line_copy
    l = line_copy.split()
    for i in range(len(l) - 1):
        if not l[i] in d:
            d[l[i]] = dict()
        if l[i + 1] in d[l[i]]:
            d[l[i]][l[i + 1]] += 1
        else:
            d[l[i]][l[i + 1]] = 1
    if len(l) > 0:
        previous_word = l[-1]
    else:
        previous_word = ''
    return previous_word


def read_from_file(given, model):
    d = dict()
    text = sys.stdin
    if given is not None:
        text = open(given, 'r', encoding='utf-8')
    word = ''
    for line in text:
        print(line)
        word = train(line, d, word)
    # for word in d:
      #  print(word, d[word])
    if model is not None:
        with open(model, 'wb') as f:
            pickle.dump(d, f)
    else:
        print('error')
    text.close()


parser = argparse.ArgumentParser()
parser.add_argument('--lc', action='store_true', help='transform to lower case')
parser.add_argument('--input_dir', action='store', help='choose the directory with files for training')
parser.add_argument('--model', action='store', help='choose the directory with files for dump', required=True)
args = parser.parse_args()
read_from_file(args.input_dir, args.model)
