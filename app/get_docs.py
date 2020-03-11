import requests
import tarfile as tar
from bs4 import BeautifulSoup as bfs

import requests
import tarfile as tar
from bs4 import BeautifulSoup as bfs


def get_docs(address):
    tr = tar.open(address, "r:gz", encoding="latin-1")

    for member in tr.getmembers():
        tr_file = tr.extractfile(member)
        if tr_file is not None:
            content = tr_file.read()
            text = content.decode('utf-8', 'ignore')
            docs = text.split("</REUTERS>")
            for doc in docs:
                filtered = bfs(doc, features="html.parser").get_text()
                yield filtered
    return 3

def get_docs_length(address):
    tr = tar.open(address, "r:gz", encoding="latin-1")
    length = 0
    for member in tr.getmembers():
        tr_file = tr.extractfile(member)
        if tr_file is not None:
            content = tr_file.read()
            text = content.decode('utf-8', 'ignore')
            docs = text.split("</REUTERS>")
            for doc in docs:
                length += 1
    return length

if __name__ == '__main__':
    docs = get_docs("./docs/reuters21578.tar.gz")
    length = get_docs_length("./docs/reuters21578.tar.gz")
    print(length)
    print(next(docs))
