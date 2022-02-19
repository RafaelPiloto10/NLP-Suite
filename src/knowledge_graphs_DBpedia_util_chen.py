# Written by Chen Gong spring 2022

import os
import tkinter.messagebox as mb
import string
import re
from re import split
from urllib import request, error
import stanza
from SPARQLWrapper import SPARQLWrapper, JSON, XML

sparql = SPARQLWrapper("http://dbpedia.org/sparql")

stanza.download('en')
stannlp = stanza.Pipeline(lang='en', processors='tokenize,ner,mwt,pos,lemma')

punksAndNum = string.punctuation + '1' + '2' + '3' + '4' + '5' + '6' + '7' + '8' + '9' + '0'


# def DBpedia_annotate(inputFile, inputDir, outputDir, annotationTypes, color1, colorls):
def DBpedia_annotate(contents, annotationTypes):
    # contents = open(inputFile, 'r', encoding='utf-8', errors='ignore').read()
    contents = preprocessing(contents)
    html_str = annotate(contents, annotationTypes)
    # TODO: create file
    return html_str


def annotate(contents, annotationTypes):
    """
    annotate the input contents. Using stanford annotator to filter out words.
    NNP and NNPs will be grouped together if they are directly followed by each other

    Parameters
    ----------
    contents: preprocessed file content
    annotationTypes:

    Returns
    -------


    """
    color1 = 'black'
    color2 = 'blue'
    html_str = '<html>\n<body>\n<div>\n'
    html_str_end = '\n</div>\n</body>\n</html>'

    # tA1 = ['<span style=\"color: ' + color1 + '\">',
    #         '</span> ']
    # tA2 = ['<a style=\"color:' + color2 + '\" href=\"',
    #        '\">',
    #        '</a> ']

    tA1 = ['<span>', '</span> ']
    tA2 = ['<a href=\"',
           '\">',
           '</a> ']

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
                query_and_html(prev_og[:-1], prev_tr[:-1], annotationTypes)
                prev_og = ""
                prev_tr = ""
                if check_eligible(str(word.text)) and pos:
                    query_and_html(str(word.text), str(word.lemma), annotationTypes)

    return html_str + html_str_end


def query_and_html(phrase_og, phrase_tr, cats, html_str, tA1, tA2):
    query = form_query_string(phrase_tr, cats)
    res = get_result(query)
    if not res:  # no url returned normal html, no annotation
        html_str += tA1[0] + phrase_og + tA1[1]
    else:  # annotate with the url
        url = res[0]
        html_str += tA2[0] + str(url) + tA2[1] + phrase_og + tA2[2]
        ## TODO choose the best link

    return html_str


def form_query_string(phrase, ont_ls):
    """

    Parameters
    ----------
    phrase
    ont_ls

    Returns
    -------

    """
    query_body = ''
    # "PREFIX https://dbpedia.org/snorql/"
    # + 'PREFIX dbpedia2: <http://dbpedia.org/property/>' + '\n' \
    query_s = 'PREFIX owl: <http://www.w3.org/2002/07/owl#>' + '\n' \
              + 'PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>' + '\n' \
              + 'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>' + '\n' \
              + 'PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>' + '\n' \
              + 'PREFIX foaf: <http://xmlns.com/foaf/0.1/>' + '\n' \
              + 'PREFIX dc: <http://purl.org/dc/elements/1.1/>' + '\n' \
              + 'PREFIX : <http://dbpedia.org/resource/>' + '\n' \
              + 'PREFIX dbpedia: <http://dbpedia.org/>' + '\n' \
              + 'PREFIX skos: <http://www.w3.org/2004/02/skos/core#>' + '\n' \
              + 'SELECT DISTINCT'

    query_s = query_s + ' ?' + 'w1'  # SELECT DISTINCT w1
    query_body = query_body + '?' + 'w1 ' + 'rdfs:label' + " \"" + phrase + "\"" + '@en'
    query_body = query_body + ".\n" + "?w1 rdf:type " + ont_ls
    query_s = query_s + "\nWHERE { "
    query_s = query_s + query_body
    query_s = query_s + "}"
    return query_s


def get_result(query):
    """
    send query request and get the result
    Parameters
    ----------
    query: a string of query

    Returns
    -------
    results a list of urls
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query().convert()
    except error.HTTPError:
        # this may occasionally give time out error depending upon server's traffic
        mb.showwarning(title='Warning',
                       message='Take a look at your command line/prompt. An HTTP error of 500 means that the YAGO server failed. Please, check command line/prompt for "Operation timed out" error\n\nTry running the script later, when the server may be be less busy.')
        return None

    # TODO process the result?
    bindings = results['results']['bindings']  # [{w1: {type: uri, value: "http:/xxx"}}]
    url_list = []
    for link in bindings:
        url_list.append(link['w1']['value'])
    return url_list


def check_eligible(phrase):
    if [x for x in phrase if (not (x in punksAndNum))] != [] and len(phrase) > 2 and phrase.lower() != "not":
        return True
    else:
        return False


def preprocessing(contents):
    """
    Preprocess the contents by removing some special chars
    Parameters
    ----------
    contents: String, raw contents in the document

    Returns
    -------
    contents: cleaned
    """
    contents = ' '.join(contents.split())  # reformat content
    contents = contents.replace('\0', '')  # remove null bytes
    contents = contents.replace('\'', '')  # remove quotation marks
    contents = contents.replace('\"', '')
    contents = contents.replace("\\", '')
    contents = contents.replace("/", ' or ')
    return contents


def stanford_annotator(content):
    return stannlp(content)


# Testing
if __name__ == '__main__':
    contents = "I went to NewYork. I am from China"
    annotationTypes = "dbo:Place"
    # phrase = "China"
    # query = form_query_string(phrase, annotationTypes)
    # res = get_result(query)
    # data = res['results']['bindings']
    # print(type(res))
    html_str = DBpedia_annotate(contents, annotationTypes)
    print(html_str)

