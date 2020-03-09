import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords as sp

def remove_stop_word(tokens):
    sw = set(sp.words('english'))
    return [word for word in tokens if word not in sw]

if __name__ == '__main__':
    test_string_list = ['alices', 'adventure', 'in', 'wonderland', 'commonly', \
                        'shorten', 'to', 'alice', 'in', 'wonderland', 'is', \
                        'an', 'one', 'thousand', 'eight', 'hundred', 'and', 'sixty', \
                        'five', 'novel', 'write', 'by', 'english', 'author', 'charles', \
                        'lutwidge', 'dodgson', 'under', 'the', 'pseudonym', 'lewis', 'carrollone']