import re
from num2words import num2words
import string

def normalize_letters(text):
    return text.lower().strip()


def normalize_numbers(text):
    return re.sub(r"(\d+)", lambda x: num2words(int(x.group(0))).replace('-', ' '), text)


def normalize_punctuation(text):
    return text.translate(str.maketrans('', '', string.punctuation))


def normalize_side_punctuation(text):
    return re.sub(r"[”“,.:;()#%!?+/'@*]", "", text)


def normalize_white_spaces(text):
    return re.sub('  +', ' ', text)


def normalize(text):
    text = normalize_letters(text)
    text = normalize_numbers(text)
    text = normalize_punctuation(text)
    text = normalize_side_punctuation(text)
    text = normalize_white_spaces(text)

    return text

if __name__ == '__main__':
    test_string = '''Alice's Adventures in Wonderland (commonly shortened to Alice in Wonderland)''' \
                  '''is an 1865 novel written by English author Charles Lutwidge Dodgson''' \
                  '''under the pseudonym Lewis Carroll.[1]'''

    print(normalize(test_string))