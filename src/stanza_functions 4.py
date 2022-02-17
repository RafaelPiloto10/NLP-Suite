'''
Examples of Usage:

1. Instantiation
    from stanza_functions import stanzaPipeLine, word_tokenize_stanza, sent_tokenize_stanza, lemmatize_stanza

2. sent_tokenize_stanza
    sentences = sent_tokenize_stanza(stanzaPipeLine(text))

3. word_tokenize_stanza
    words = word_tokenize_stanza(stanzaPipeLine(text))

4. lemmatize_stanza
    lemma = lemmatize_stanza(stanzaPipeLine(word))
'''

import stanza

stanzaPipeLine = stanza.Pipeline(lang='en', processors= 'tokenize, lemma')

# returns list of word tokens
# same as nltk.tokenize.word_tokenize()
def word_tokenize_stanza(doc):
    lst = []
    for sentence in doc.sentences:
        [lst.append(token.text) for token in sentence.tokens]
    return lst

# returns list of sentence tokens
# same as nltk.tokenize.sent_tokenize()
def sent_tokenize_stanza(doc):
    return [sentence.text for sentence in doc.sentences]

# returns a single lemmatized word. input should be a single word.
# same as nltk.stem.wordnet.WordNetLemmatizer().lemmatize(text)
# IMPORTANT: Stanza lemmatizer only returns pos='v' version of lemmas
def lemmatize_stanza(doc):
    return doc.sentences[0].words[0].lemma
