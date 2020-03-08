import nltk

nltk.download('wordnet')


def tokenize(text):
    return nltk.word_tokenize(text)

if __name__ == '__main__':

    test_string = 'alices adventures in wonderland commonly shortened to alice ' \
                  'in wonderland is an one thousand eight hundred and sixty five ' \
                  'novel written by english author charles lutwidge dodgson ' \
                  'under the pseudonym lewis carrollone'
    print(tokenize(test_string))