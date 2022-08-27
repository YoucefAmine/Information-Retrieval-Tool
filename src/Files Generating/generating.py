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
