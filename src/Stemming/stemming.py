from nltk.stem import PorterStemmer

#! Stemming Function
def stemming(token):
    return PorterStemmer().stem(token)  # * Stemming Using Porter Stemmer
