from xml.etree import ElementTree # * XML Parser Library

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

