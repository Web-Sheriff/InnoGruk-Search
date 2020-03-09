from functools import reduce
from itertools import islice
from pytrie import SortedStringTrie as Trie

from app.normalization import normalize
from app.tokenization import tokenize
from app.text_preprocess import preprocess
from app.levenshtein import levenshtein, find_the_closest_words
from app.soundex import soundex


def search(query, prfx, psfx, sndx, index):
    res = []
    track = ''
    message = ''

    words = query.split()
    pr_words = tokenize(normalize(query))

    for w in words:
        for i, prw in enumerate(pr_words):
            if levenshtein(prw, w) <= 1 and '*' in w:
                pr_words[i] = w

    print('Query:', ' '.join(words))
    print('Preprocess function', preprocess(query))
    print('Preprocessed query:', ' '.join(pr_words))

    for w in pr_words:

        res_ = []
        wildcard = w.count('*')
        track += '&&('

        if wildcard:

            if wildcard > 1:
                print('InnoGruk cannot handle two wildcards yet :)')
                break

            split_wd = (w.split('*'))
            if split_wd[1] == '':

                try:
                    for key in prfx.keys(prefix=split_wd[0]):
                        if key in index:
                            res_.append(index[key])
                            track += f'{key}||'

                    res_ = list(reduce(lambda i, j: i | j, (set(x) for x in res_)))
                    track = track[:-2]

                except:
                    track += 'MIDLEFIX ERROR'

            elif split_wd[0] == '':

                try:
                    for key in psfx.keys(prefix=split_wd[1][::-1]):
                        if key in index:
                            res_.append(index[key])
                            track += f'{key}||'

                    res_ = list(reduce(lambda i, j: i | j, (set(x) for x in res_)))
                    track = track[:-2]

                except:
                    track += 'POSTFIX ERROR'

            else:
                split_wd = list(filter(None, split_wd))

                try:

                    for pref_key in prfx.keys(prefix=split_wd[0]):
                        for post_key in psfx.keys(prefix=split_wd[1][::-1]):
                            if pref_key == post_key[::-1]:

                                pre_key = preprocess(pref_key)[0]
                                if pre_key in index:
                                    res_.append(index[pre_key])
                                    track += f'{pre_key}||'

                    res_ = list(reduce(lambda i, j: i | j, (set(x) for x in res_)))
                    track = track[:-2]

                except:
                    track += 'MIDLEFIX ERROR'

            res.append(res_)

        else:
            try:
                res.append(index[w])
                track += w
            except:
                print('-------------------------------------------------')

                message += f'***\nThere are lots of words with the same soundex: ' \
                           f'{", ".join(list(islice(sndx[soundex(w)], 5)))}...\n'
                right_words = find_the_closest_words(w, sndx[soundex(w)])
                message += f'Probably, you mentioned something from {" ,".join(right_words)} instead of {w}'

                print(message)

                for ww in right_words:
                    pre_ww = preprocess(ww)[0]
                    if pre_ww in index:
                        res_.append(index[pre_ww])
                        track += f'{ww}||'

                track = track[:-2]

                res_ = list(reduce(lambda i, j: i | j, (set(x) for x in res_)))
                res.append(res_)

        track += ')'

    relevant_documents = []
    try:
        relevant_documents = list(reduce(lambda i, j: i & j, (set(x) for x in res)))
    except:
        print('NOT FOUND')
    print('-----------------------------------------------------------')
    print(len(relevant_documents))

    return relevant_documents, track[2:]


if __name__ == '__main__':
    prfx = Trie(apple=None, borrow=None, friend=None, ginger=None,
                lermontov=None, money=None, november=None, object=None)

    psfx = Trie(elppa=None, worrob=None, dneirf=None, regnig=None,
                votnomrel=None, yenom=None, rebmevon=None, tcejbo=None)

    sndx = {'A140':['apple'], 'B600':['borrow'], 'F653':['friend'], 'G526':['ginger'],
            'L655':['lermontov'], 'M500':['money'], 'N151':['november'], 'O122':['object']}

    index = {'apple':[0,1,2,3], 'borrow':[0,1,2], 'friend':[1,2,3], 'ginger':[0,2,3],
             'lermontov':[0,3], 'money':[1,2], 'november':[0,1,2,3], 'object':[4]}

    query = 'apple nov*er gingerr'

    print(search(query, prfx, psfx, sndx, index))