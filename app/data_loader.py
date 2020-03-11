from pytrie import SortedStringTrie as Trie
from app.text_preprocess import preprocess
from app.normalization import normalize
from app.tokenization import tokenize
from app.soundex import soundex
from app.get_docs import get_docs


def load_data(doc, name, aux, word2soundex, prefix_tree, postfix_tree):
    prep_text = preprocess(doc)
    norm_text = tokenize(normalize(doc))
    i = int(name.split()[1])

    for word in prep_text:

        if word == '':
            continue

        # Auxiliary inverted index loader
        if not word in aux:
            aux[word] = []
        if i not in aux[word]:
            aux[word].append(i)

    for word in norm_text:

        if word == '':
            continue

        sndx = soundex(word)
        # Soundex loader
        if not (sndx in word2soundex):
            word2soundex[sndx] = []
        if word not in word2soundex[sndx]:
            word2soundex[sndx].append(word)

        # Prefix tree loader
        if not word in prefix_tree:
            prefix_tree[word] = None

        rword = word[::-1]
        # Postfix_tree loader
        if not rword in postfix_tree:
            postfix_tree[rword] = None

    return aux, word2soundex, prefix_tree, postfix_tree

if __name__ == '__main__':
    aux = {'one': [0], 'five': [0], 'reuters': [0]}
    w2s = {'O500': ['one'], 'F100': ['five'], 'R362':['reuters']}
    prfx = Trie(one = None, five = None, reuters = None, chelny = None)
    psfx = Trie(eon = None, evif = None, sretuer = None, ylehc = None)
    doc = next(get_docs("./docs/reuters21578.tar.gz"))
    name = 'collection 1'

    aux, w2s, prfx, psfx = load_data(doc, name, aux, w2s, prfx, psfx)

    print(aux)
    print(w2s)
    print(prfx)
    print(psfx)

