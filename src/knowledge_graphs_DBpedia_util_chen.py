# Written by Chen Gong spring 2022

import os
import tkinter.messagebox as mb
import string
punksAndNum = string.punctuation + '1' + '2' + '3' + '4' + '5' + '6' + '7' + '8' + '9' + '0'

import re
from re import split
from urllib import request, error

import stanza
stanza.download('en')
stannlp = stanza.Pipeline(lang='en', processors='tokenize,ner,mwt,pos,lemma')

from SPARQLWrapper import SPARQLWrapper, JSON, XML
sparql = SPARQLWrapper("http://dbpedia.org/sparql")



def yagao_annotate(inputFile, inputDir, outputDir, annotationTypes, color1, colorls):
    contents = open(inputFile, 'r', encoding='utf-8', errors='ignore').read()
    contents = preprocess_content(contents)
    annotated_doc = stanford_annotator(contents)
    for sent_id in range(len(annotated_doc.sentences)):
        sent = annotated_doc.sentences[sent_id]
        prev_og = ""
        prev_tr = ""
        pos = True
        for i in range(len(sent.words)):
            word = sent.words[i]
            pos = True
            if (word.pos == "VERB") or (word.pos == "DET") or (word.pos == "ADP") or (word.pos == "PRON") or (
                    word.pos == "AUX"):
                pos = False
            if word.xpos == "NNP" or word.xpos == "NNPS":
                prev_tr = prev_tr + word.lemma + " "
                prev_og = prev_og + word.text + " "
            else:  # annotate the Proper noun cached previously and the current word
                annotate(prev_og[:-1], prev_tr[:-1], annotationTypes)
                prev_og = ""
                prev_tr = ""
                if check_eligible(str(word.text)) and pos:
                    annotate(str(word.text), str(word.lemma), annotationTypes)

    pass

def annotate(phrase_og, phrase_tr, cats):
    form_query_string(phrase_tr, cats)
    pass


def form_query_string(phrase, ont_ls):
    query_body = ''
    query_s = 'PREFIX owl: <http://www.w3.org/2002/07/owl#>' + '\n' \
              + 'PREFIX schema: <http://schema.org/>' + '\n' \
              + 'PREFIX bioschemas: <http://bioschemas.org/>' + '\n' \
              + 'PREFIX yago: <http://yago-knowledge.org/resource/>' + '\n' \
              + 'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>' + '\n' \
              + 'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>' + '\n' \
              + 'SELECT DISTINCT'
    query_s = query_s + '?' + 'w1'   # SELECT DISTINCT w1
    query_body = query_body + '?' + 'w1 ' + 'rdfs:label' + " \"" + phrase + "\"" + '@en'
    query_s = query_s + "\nWHERE { "
    query_s = query_s + query_body
    query_s = query_s + "}"
    return


def get_result(query):
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    try:
        results=sparql.query().convert()
    except error.HTTPError:
        # this may occasionally give time out error depending upon server's traffic
        mb.showwarning(title='Warning',
                       message='Take a look at your command line/prompt. An HTTP error of 500 means that the YAGO server failed. Please, check command line/prompt for "Operation timed out" error\n\nTry running the script later, when the server may be be less busy.')
        return None
    return results



def check_eligible(phrase):
    if [x for x in phrase if (not (x in punksAndNum))] != [] and len(phrase) > 2 and phrase.lower() != "not":
        return True
    else:
        return False


def preprocess_content(contents):
    contents = ' '.join(contents.split())  # reformat content
    contents = contents.replace('\0', '')  # remove null bytes
    contents = contents.replace('\'', '')  # remove quotation marks
    contents = contents.replace('\"', '')
    contents = contents.replace("\\", '')
    contents = contents.replace("/", ' or ')
    return contents


def stanford_annotator(content):
    return stannlp(content)
