from jellyfish import levenshtein_distance
import csv
import os
import re


def load_words():
    ws = {}
    for filename in os.listdir('words'):
        with open(f'words/{filename}', 'r', encoding='utf-8') as f:
            ws[filename.split('.')[0]] = [j for i in csv.reader(f) for j in i]
    return ws


words = load_words()


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
    return max([_evaluate(word, lang_words) for lang_words in words[lang]])


def get_timestamps(timestamps_string):
    timestamps = re.sub(r'\([^)]*\)', '', timestamps_string)
    return [tuple(float(j) for j in i.split('-')) for i in timestamps.split(';')[:-1]]


def save_words(timestamps_string):
    chosen_words = ''.join(re.findall(r';|[^\W\d]', timestamps_string)).split(';')[:-1]
    with open('chosen_words.txt', 'a') as f:
        f.writelines('\n'.join(chosen_words) + '\n')


if __name__ == '__main__':
    for w in ['один', 'ж', 'жж', 'жжж', 'жжжж', 'т', 'те', 'тес', 'тест', 'Тест', 'тестик', 'тестування']:
        print(w, evaluate(w, 'uk'))
