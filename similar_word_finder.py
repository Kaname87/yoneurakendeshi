import csv
from gensim.models import KeyedVectors
from const import *

def find_and_write_similar_words(target_words, topn):
    csv_header = ['target_word', 'similar_word', 'similarity']

    model_dir = './word2vec/entity_vector/entity_vector.model.bin'
    model = KeyedVectors.load_word2vec_format(model_dir, binary=True)
    with open(WORD_SOURCE_FILE_NAME, 'w') as f:
        writer = csv.writer(f, lineterminator='\n') 
        writer.writerow(csv_header)
        for word in target_words:
            results = model.most_similar(f'{word}', topn=topn)
            for result in results:  
                output = [word] + list(result) 
                writer.writerow(output)

# if __name__ == "__main__":
#     target_words = ['米', '津', '玄', '師']
#     find_and_write_similar_words(target_words, 15)