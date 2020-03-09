import numpy as np


def levenshtein(seq1, seq2):
    size_x = len(seq1) + 1
    size_y = len(seq2) + 1
    matrix = np.zeros((size_x, size_y))
    for x in range(size_x):
        matrix[x, 0] = x
    for y in range(size_y):
        matrix[0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if seq1[x - 1] == seq2[y - 1]:
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,
                    matrix[x - 1, y - 1],
                    matrix[x, y - 1] + 1
                )
            else:
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,
                    matrix[x - 1, y - 1] + 1,
                    matrix[x, y - 1] + 1
                )

    return (int(matrix[size_x - 1, size_y - 1]))


def find_the_closest_words(in_word, word_list):
    min = 1000
    result = []
    for word in word_list:
        distance = levenshtein(in_word, word)
        if distance < min:
            min = distance

    for word in word_list:
        distance = levenshtein(in_word, word)
        if distance == min:
            result.append(word)

    return result


if __name__ == '__main__':
    test_strings = [('Alice', 'Align'), ('Boris', 'Boristenko'), ('Cat', 'Catostrophie')]
    for ts in test_strings:
        print(levenshtein(ts[0], ts[1]))

    print(find_the_closest_words('word', ['jsfdk','worg', 'worm', 'dord','kjlla']))