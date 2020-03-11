def soundex(query):
    query = str.upper(query)

    soundex = ""
    soundex += query[0]
    dictionary = {"BFPV": "1", "CGJKQSXZ": "2", "DT": "3", "L": "4", "MN": "5", "R": "6", "AEIOUHWY": "."}

    for char in query[1:]:
        for key in dictionary.keys():
            if char in key:
                code = dictionary[key]
                if code != soundex[-1]:
                    soundex += code

    soundex = soundex.replace(".", "")
    soundex = soundex[:4].ljust(4, "0")

    return soundex

if __name__ == '__main__':
    test_strings = ['Alice', 'Align', 'Boris', 'Boristenko', 'Cat', 'Catostrophie', 'Catosrtophie']

    for ts in test_strings:
        print(soundex(ts))
    print('----------------------------')
    print(soundex('oejfearjkoafojfoajijkaf'))