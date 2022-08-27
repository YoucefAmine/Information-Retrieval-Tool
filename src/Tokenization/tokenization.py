from nltk.tokenize import RegexpTokenizer

#! Tokenization Function
def tokenization(text):
    tokenizer = RegexpTokenizer("[\w]+")  # * Split On Every Non-Letter
    return tokenizer.tokenize(text)

