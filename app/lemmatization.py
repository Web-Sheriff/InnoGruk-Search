from nltk.stem import WordNetLemmatizer as wnl_
import nltk

nltk.download('averaged_perceptron_tagger')
from nltk import pos_tag
from nltk.corpus import wordnet


def lemmatize(tokens):
    wn = wnl_()
    word2pos = pos_tag(tokens)
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return [wn.lemmatize(token,tag_dict.get(word2pos[i][1][0].upper(), wordnet.NOUN)) for i,token in enumerate(tokens)]


def lemmatization_word(word):
    wn = wnl_()
    return wn.lemmatize(word, 'a')


if __name__ == '__main__':
    test_string_list = ['alices', 'adventures', 'in', 'wonderland', 'commonly', \
                        'shortened', 'to', 'alice', 'in', 'wonderland', 'is', \
                        'an', 'one', 'thousand', 'eight', 'hundred', 'and', 'sixty', \
                        'five', 'novel', 'written', 'by', 'english', 'author', 'charles', \
                        'lutwidge', 'dodgson', 'under', 'the', 'pseudonym', 'lewis', 'carrollone']

    print("\n".join(lemmatize(test_string_list)))