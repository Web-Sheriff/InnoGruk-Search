from functools import reduce
from itertools import islice
from pytrie import SortedStringTrie as Trie

from app.normalization import normalize
from app.stop_words import remove_stop_word
from app.tokenization import tokenize
from app.text_preprocess import preprocess
from app.levenshtein import levenshtein, find_the_closest_words
from app.soundex import soundex
from app.index_loader import load_index, get_index_keys, index_find


def search_disk(query, prfx, psfx, sndx, aux, path):
    index_keys = get_index_keys(path)

    res = []
    track = ''
    message = ''

    words = query.split()
    clear_query = ''
    for w in words:
        clear_query += ''.join(map(str, remove_stop_word([w]))) + ' '

    pr_words = tokenize(normalize(clear_query))

    for w in words:
        for i, prw in enumerate(pr_words):
            if levenshtein(prw, w) <= 1 and '*' in w:
                pr_words[i] = w
    print(pr_words)

    message += f'Query: {" ".join(words)}\n'
    message += f'Preprocessed query: {" ".join(pr_words)}\n'

    for w in pr_words:

        res_ = []
        wildcard = w.count('*')
        track += '&&('

        if wildcard:

            split_wd = (w.split('*'))
            if split_wd[1] == '':

                try:
                    for key in prfx.keys(prefix=split_wd[0]):
                        if key in index_keys:
                            res_.append(index_find(key, path))
                            if key in aux:
                                res_.append(aux[key])
                                track += f'{key}||'
                            else:
                                track += f'{key}||'

                    res_ = list(reduce(lambda i, j: i | j, (set(x) for x in res_)))
                    track = track[:-2]

                except:
                    track += 'POSTFIX ERROR'

            elif split_wd[0] == '':

                try:
                    for key in psfx.keys(prefix=split_wd[1][::-1]):
                        if key[::-1] in index_keys:
                            res_.append(index_find(key[::-1], path))
                            if key[::-1] in aux:
                                res_.append(aux[key[::-1]])
                                track += f'{key[::-1]}||'
                            else:
                                track += f'{key[::-1]}||'

                    res_ = list(reduce(lambda i, j: i | j, (set(x) for x in res_)))
                    track = track[:-2]

                except:
                    track += 'PREFIX ERROR'

            else:
                split_wd = list(filter(None, split_wd))

                try:

                    for pref_key in prfx.keys(prefix=split_wd[0]):
                        for post_key in psfx.keys(prefix=split_wd[1][::-1]):
                            if pref_key == post_key[::-1]:

                                pre_key = preprocess(pref_key)[0]
                                if pre_key in index_keys:
                                    res_.append(index_find(pre_key, path))
                                    if pre_key in aux:
                                        res_.append(aux[pre_key])
                                        track += f'{pre_key}||'
                                    else:
                                        track += f'{pre_key}||'


                    res_ = list(reduce(lambda i, j: i | j, (set(x) for x in res_)))
                    track = track[:-2]

                except:
                    track += 'MIDLEFIX ERROR'

            res.append(res_)

        else:
            try:
                res.append(index_find(w, path))
                if w in aux:
                    res.append(aux[w])
                track += w
            except:
                try:
                    right_words = []
                    if soundex(w) not in sndx:
                        message += f'There is no soundex for the word \"{w}\"\n'
                    else:
                        right_words = find_the_closest_words(w, sndx[soundex(w)])
                        message += f'First five words with the same soundex: ' \
                                   f'\"{", ".join(list(islice(sndx[soundex(w)], 5)))}\"...\n'

                    if right_words:
                        message += f'Probably, you mentioned \"{", ".join(right_words)}\" instead of \"{w}\"\n'
                    else:
                        message += 'InnoGruk has not recognized what you mention\n'

                    for ww in right_words:
                        pre_ww = preprocess(ww)[0]
                        if pre_ww in index_keys:
                            res_.append(index_find(pre_ww, path))
                            if pre_ww in aux:
                                res.append(aux[pre_ww])
                                track += f'{ww}||'
                            else:
                                track += f'{ww}||'

                    if track[-1] == '|':
                        track = track[:-2]

                    res_ = list(reduce(lambda i, j: i | j, (set(x) for x in res_)))
                    res.append(res_)
                except:
                    right_words = []
                    if soundex(w) in sndx:
                        right_words = find_the_closest_words(w, sndx[soundex(w)])
                    track += 'INDEX ERROR'
                    if right_words:
                        message += f'These words: \"{w}, {", ".join(right_words)}\" do not belong to index\n'
                    else:
                        message += f'The word \"{w}\" does not belong to index\n'

        track += ')'

    relevant_documents = []
    try:
        relevant_documents = list(reduce(lambda i, j: i & j, (set(x) for x in res)))
    except:
        pass

    message += f'InnoGruk found {len(relevant_documents)} documents by your query\n'

    return message, sorted(relevant_documents), track[2:]


if __name__ == '__main__':
    prfx = Trie(apple=None, borrow=None, friend=None, ginger=None,
                lermontov=None, money=None, november=None, object=None)

    psfx = Trie(elppa=None, worrob=None, dneirf=None, regnig=None,
                votnomrel=None, yenom=None, rebmevon=None, tcejbo=None)

    sndx = {'A140': ['apple'], 'B600': ['borrow'], 'F653': ['friend'], 'G526': ['ginger'],
            'L655': ['lermontov'], 'M500': ['money'], 'N151': ['november'], 'O122': ['object']}

    index = {'apple': [0, 1, 2, 3], 'borrow': [0, 1, 2], 'friend': [1, 2, 3], 'ginger': [0, 2, 3],
             'lermontov': [0, 3], 'money': [1, 2], 'november': [0, 1, 2, 3], 'object': [4]}

    aux = {}

    path = './index'

    load_index(index, path)

    query = 'ap'

    message, result, track = search_disk(query, prfx, psfx, sndx, aux, './index')
    print(message)
    print(result)
    print(track)
