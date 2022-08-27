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
