import os
import stanza
stanza.download('en')
stannlp = stanza.Pipeline(lang='en', processors='tokenize,ner,mwt,pos,lemma')


def YAGO_annotate(inputFile, inputDir, outputDir, annotationTypes,color1,colorls):
    contents = open(inputFile, 'r', encoding='utf-8', errors='ignore').read()
    contents = preprocess_content(contents)
    annotated_doc = stanford_annotator(contents)
    for sent_id in range(len(annotated_doc.sentences)):
        sent=annotated_doc.sentences[sent_id]
        #sent_ner=nerdoc.sentences[sent_id]
        prev_og = ""
        prev_tr = ""
        pos=True
        for i in range(len(sent.words)):
            word=sent.words[i]
            pos=True
            if((word.pos=="VERB")or (word.pos=="DET")or(word.pos=="ADP")or (word.pos=="PRON") or (word.pos=="AUX")):
                pos=False

            #word_ner=sent_ner.tokens[i]
            #if((word.id==1 and word_ner.ner!="o")|(word.id!=1 and (word.text[0]).isupper())):
            if(word.xpos=="NNP"or word.xpos=="NNPS"):
    pass

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