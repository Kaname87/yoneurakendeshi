import csv
from gensim.models import KeyedVectors
from const import *

def load_model():
    model_dir = './word2vec/entity_vector/entity_vector.model.bin'
    return KeyedVectors.load_word2vec_format(model_dir, binary=True)

def find_and_write_similar_words(target_words, topn):
    csv_header = ['target_word', 'similar_word', 'similarity']

    model = load_model()
    with open(WORD_SOURCE_FILE_NAME, 'w') as f:
        writer = csv.writer(f, lineterminator='\n') 
        writer.writerow(csv_header)
        for word in target_words:
            results = model.most_similar(f'{word}', topn=topn)
            for result in results:  
                output = [word] + list(result) 
                writer.writerow(output)

def find_similar_word(word, topn=10):
    model = load_model()
    return model.most_similar(f'{word}', topn=topn)

if __name__ == "__main__":
    # word = '檸檬'
    # print(find_similar_word(word, 20))

#     target_words = ['米', '津', '玄', '師']
#     find_and_write_similar_words(target_words, 15)