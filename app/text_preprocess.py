from app.normalization import normalize as nz
from app.tokenization import tokenize as tz
from app.lemmatization import lemmatize as lz
from app.stop_words import remove_stop_word as rsw


def preprocess(text):
    normalized = nz(text)
    tokenized = tz(normalized)
    lemmatized = lz(tokenized)
    cleared = rsw(lemmatized)

    return cleared

if __name__ == '__main__':
    test_string = '''Alice's Adventures in Wonderland (commonly shortened to Alice in Wonderland)''' \
                  '''is an 1865 novel written by English author Charles Lutwidge Dodgson''' \
                  '''under the pseudonym Lewis Carroll.[1]'''

    print(' '.join(preprocess(test_string)))