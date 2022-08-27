#! Stop Words Function
def stopWords():
    englishST = 'englishST.txt'

    file = open(englishST, 'r')
    stopWords = file.read()
    file.close()

    return stopWords
