import os

def load_index(dict, path):
    for key in dict:
        files_list = ' '.join(map(str, dict[key]))
        with open(f'{path}/{key}', 'a') as filehandle:
            filehandle.write(files_list + ' ')

    dict.clear()


def index_find(key, path):
    names = os.listdir(path)
    if key in names:
        with open(f'{path}/{key}', 'r') as filehandle:
            return list(map(int, filehandle.read().split()))
    else:
        raise FileNotFoundError


def get_index_keys(path):
    return os.listdir(path)


if __name__ == '__main__':
    index = {'apple': [0, 1, 2, 3], 'borrow': [0, 1, 2], 'friend': [1, 2, 3], 'ginger': [0, 2, 3],
             'lermontov': [0, 3], 'money': [1, 2], 'november': [0, 1, 2, 3], 'object': [4]}
    load_index(index, './index')

    print(index_find('apple', './index'))
    print(get_index_keys('./index'))