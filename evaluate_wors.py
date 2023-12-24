from jellyfish import levenshtein_distance
import csv
import os
import re


words = {}
for filename in os.listdir('words'):
    with open(f'words/{filename}', 'r') as f:
        words[filename.split('.')[0]] = [j for i in csv.reader(f) for j in i]


def _evaluate(new_word, known_word, max_=0.9, min_=0.1):
    new_word = re.sub(r'[\W\d_]', '', new_word).lower()
    length = len(new_word)
    max_distance = max(length, len(new_word))
    distance = levenshtein_distance(known_word, new_word)
    if length < 3:
        return min_
    r = 1 - distance / max_distance
    if r > 0.8:
        return max_
    if length < 5 and r <= 0.5:
        return min_
    if max_distance * r < 4:
        return max(min_, r/2)
    return r  # 1 / (distance + 1)


def evaluate(word, lang):
    return max([_evaluate(word, w) for w in words[lang]])


if __name__ == '__main__':
    for w in ['один', 'ж', 'жж', 'жжж', 'жжжж', 'т', 'те', 'тес', 'тест', 'тестик', 'тестування']:
        print(w, evaluate(w, 'uk'))
