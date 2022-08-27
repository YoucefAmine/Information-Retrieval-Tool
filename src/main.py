'''
Created on Thu Dec 30 15:18:52 2021
@author: AMINE Youcef-Abdenour
'''

from xml.etree import ElementTree # * XML Parser Library
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer

############################################### Functions ################################################

#! Tokenization Function
def tokenization(text):
    tokenizer = RegexpTokenizer("[\w]+")  # * Split On Every Non-Letter
    return tokenizer.tokenize(text)


#! Stop Words Function
def stopWords():
    englishST = 'englishST.txt'

    file = open(englishST, 'r')
    stopWords = file.read()
    file.close()

    return stopWords


#! Stemming Function
def stemming(token):
    return PorterStemmer().stem(token)  # * Stemming Using Porter Stemmer


#! Indexing Function
def indexing(dom):
    items = {}  # * Terms Dict {term: {docId: [positions in the document]}}

    #! Parsing XML File
    for x in dom.findall('DOC'):  # * Reading All DOC Tags in XML File
        docId = x.find('DOCNO').text  # * Document Id
        headline = x.find('HEADLINE').text  # * Document Headline
        text = headline + x.find('TEXT').text  # * Document Text

        #! Tokenization & Normalization
        tokens = tokenization(text.lower())

        #! Indexing
        position = 0  # * Position Of The Token In The Document
        for token in tokens:  # * Reading Tokens One by One
            if token not in stopWords():  # ! Removing Stop Words
                item = stemming(token)  # ! Stemming Using Porter
                position += 1
                #! Inverted Index Implimentation
                if item not in items.keys():  # ? Item Doesn't Exist In The Index? (New Term)
                    # * Create a New Item In The Index
                    items[item] = {docId: [position]}
                # ? Item Exists In The Index? (Term Exists In Other Document That We Read It Before, Or This Term Exists In This Document, And We Read It Before)
                else:
                    # * Document List That The Item Exist In
                    itemDocs = items[item].keys()
                    # ? Document Doesn't Exist In The Document List Of The Item? (We Didn't Met With This Term In This Document Before)
                    if docId not in itemDocs:
                        # * Create Document Number With The Position Of The Item In The Document
                        items[item][docId] = [position]
                    # ? Document Exists In The Document List? (We Already Met With This Term In This Document Before; Term Duplicate In This Document)
                    else:
                        # * Append Just The Position Of The Item In The Positions Table
                        items[item][docId].append(position)

    return items


#! Generating File Result Function
def generateFileResult(fileResult, items):
    with open(fileResult, 'w') as newFile:
        for key, value in items.items():  # * Reading All The Items In The 'Items DICT'
            # * Creating The Keys Of The Dict In File Result(Terms With Document Frequency)
            newFile.write('%s: %s \n' % (key, len(value.items())))

            # * Reading All The Items In The Value Of The Dict(Nested Dict) {term: {docId: [positions in the document]}}
            for k, v in value.items():
                # * Converting All Positions(Int) Into Strings (To Use Built-in Join Function)
                stringV = [str(sv) for sv in v]
                stringV = ','.join(stringV)
                # * Creating DocId And Term Positions in The Document
                newFile.write('\t%s: %s \n' % (k, stringV))
            newFile.write('\n')


#! Search Function
def search(queriesFile, fileResultQueries):
    #! Reading The Query From User Input
    # query = input('Enter The Query: ')

    #! Reading The Query From File
    with open(queriesFile, "r") as queriesFile:
        i = 0
        for line in queriesFile:
            i += 1
            query = line.strip('q%d:' % i)

            tokens = tokenization(query.lower())

            documentsReleventTemp = []
            documentsRelevent = []
            documentsReleventDictOne = {}
            documentsReleventDictTwo = {}
            op = 0  # 0: Or, 1: And
            neg = 0  # 1: Not, 0: !Not
            successiveTokens = 0

            for token in tokens:  # * Reading Tokens One by One
                if token == 'not':
                    neg = 1

                if token == 'and':
                    op = 1

                if token == 'or':
                    op = 0

                if token not in ['not', 'and', 'or']:
                    successiveTokens += 1
                    # op = None

                # ! Remove Stop Words('or, not, and' are stopWords)
                if token not in stopWords():
                    item = stemming(token)  # ! Stemming Using Porter

                    if item in items.keys():  # ! item exists in docs?
                        for doc in items[item].keys():
                            documentsReleventTemp.append(doc)

                            if op == None:
                                if successiveTokens == 1:
                                    documentsReleventDictOne[doc] = items[item][doc]
                                else:
                                    documentsReleventDictTwo[doc] = items[item][doc]

                        #! 'Not' Case
                        if neg == 1:
                            neg = 0
                            successiveTokens = 0
                            documentsReleventTempCopy = documentsReleventTemp.copy()
                            documentsReleventTemp.clear()
                            for item in items.keys():
                                for doc in items[item].keys():
                                    if doc not in documentsReleventTempCopy:
                                        documentsReleventTemp.append(doc)

                            documentsReleventTempCopy.clear()

                        #! 'And' Case
                        if op == 1:
                            op = 0
                            successiveTokens = 0
                            documentsReleventTempCopy = documentsRelevent.copy()
                            documentsRelevent.clear()

                            for doc in documentsReleventTemp:
                                if doc in documentsReleventTempCopy:
                                    documentsRelevent.append(doc)

                            documentsReleventTempCopy.clear()

                        #! 'Or' Case (Normal Case)
                        if op == 0:
                            successiveTokens = 0
                            for doc in documentsReleventTemp:
                                documentsRelevent.append(doc)

                        documentsReleventTemp.clear()
                        documentsReleventDictOne.clear()
                        documentsReleventDictTwo.clear()

                elif successiveTokens > 0:
                    successiveTokens -= 1
            with open(fileResultQueries, 'a') as fileResult:
                stringV = [str(sv) for sv in set(documentsRelevent)]
                stringV = ','.join(stringV)
                fileResult.write('%s: \t %s \n' % (i, stringV))

            documentsRelevent.clear()


#####################################################################################################


############################################### Main ################################################

#! Loading Files
fileName = 'trec.sample.xml'
fileResult = 'index.txt'
queriesFile = 'queries.lab2.txt'
fileResultQueries = 'results.boolean.txt'

tree = ElementTree.parse(fileName)
root = tree.getroot()

#! Preprocessing & Indexing
items = indexing(root)

#! Generating fileResult
generateFileResult(fileResult, items)

#! Searching(Queries File)
search(queriesFile, fileResultQueries)
#####################################################################################################
