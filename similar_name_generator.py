import random
import csv
import os
from dotenv import load_dotenv

from const import *

TARGET_WORD_COLUMN_IDX = 0
SIMILAR_WORD_COLUMN_IDX = 1
SIMILARITY_COLUMN_IDX = 2

def append_target_word(target_word, similar_word_list):
    TARGET_WORD_RATE = os.environ.get('TARGET_WORD_RATE')
    if float(TARGET_WORD_RATE) > 0:
        correct_word_num = int(len(similar_word_list) * float(TARGET_WORD_RATE))
        similar_word_list += [[target_word, target_word, 1.0] for x in range(correct_word_num)]
    return similar_word_list

def create_similar_word_list_all():
    similar_word_list_all = []
    similar_word_list = []
    prev_target_word = ''

    dotenv_path = os.path.dirname(__file__) + '.env'
    load_dotenv(dotenv_path)

    with open(WORD_SOURCE_FILE_NAME, 'r') as f:
        reader = csv.reader(f)
        next(reader) # Header 捨てる

        for row in reader:
            current_target_word = row[TARGET_WORD_COLUMN_IDX]
        
            if prev_target_word != '' and prev_target_word != current_target_word:
                
                # 解答が正解と違いすぎるとつまらないので、正解の文字も一定数入れておく
                similar_word_list = append_target_word(prev_target_word, similar_word_list)
                similar_word_list_all.append(similar_word_list)
                similar_word_list = []

            # '[' ']'を取り除く
            similar_word = row[SIMILAR_WORD_COLUMN_IDX].replace('[', '').replace(']', '')
            # [米]のような ケースがあるため、取り除きの結果、ターゲットと同じになるならスキップ
            if similar_word == current_target_word:
                continue

            # '[' ']'を取り除いたものを使う
            row[SIMILAR_WORD_COLUMN_IDX] = similar_word

            similar_word_list.append(row)
            prev_target_word = current_target_word
        
        # 最後の文字リスト用
        similar_word_list = append_target_word(prev_target_word, similar_word_list)
        similar_word_list_all.append(similar_word_list)
    return similar_word_list_all

def apend_random_select_word(word_list, selected_words):
    selected_words.append(random.choice(word_list))
    return selected_words

# アプリにはこちらを使う
def select_random_words(similar_word_list_all):
    selected_words = []
    for similar_word_list in similar_word_list_all:
        apend_random_select_word(similar_word_list, selected_words)
    return selected_words

# お試し用
def select_words_by_rank(similar_word_list_all, rank):
    selected_words = []
    for similar_word_list in similar_word_list_all:
        selected_words.append(similar_word_list[rank-1])
    return selected_words

def join_words(selected_words):
    words = map(lambda word: word[SIMILAR_WORD_COLUMN_IDX], selected_words)
    return ''.join(words)

def calc_avg_similarity(selected_words):
    similarities = map(lambda word: float(word[SIMILARITY_COLUMN_IDX]), selected_words)
    return sum(similarities) / len(selected_words)

def format_similarity(similarity):
    return '{:.2%}'.format(float(similarity))

def format_word_similarity(selected_words):
    result = ''
    for word in selected_words:
        target_word = word[TARGET_WORD_COLUMN_IDX]
        similar_word = word[SIMILAR_WORD_COLUMN_IDX]
        formatted_words = f'[{target_word}-{similar_word}]'.ljust(7, '　')
        
        formatted_similarity = format_similarity(word[SIMILARITY_COLUMN_IDX])
        result += f'\n{formatted_words} 類似度: {formatted_similarity}'
    return result

def format_all_result(selected_words):
    name = join_words(selected_words)
    name_similarity = format_similarity(calc_avg_similarity(selected_words))
    # print(name_similarity, name)

    format_name_similarity = f'平均類似度: {name_similarity}'
    similarity_detail = format_word_similarity(selected_words)
    return f'{name}\n{similarity_detail}\n{format_name_similarity}'

def generate_formatted_random_name():
    similar_word_list_all = create_similar_word_list_all()
    selected_words = select_random_words(similar_word_list_all)
    return format_all_result(selected_words)

if __name__ == "__main__":
    for i in range(1):
        text = generate_formatted_random_name()
        print(text)