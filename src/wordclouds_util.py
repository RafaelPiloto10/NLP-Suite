import sys
import GUI_util
import IO_libraries_util

if not IO_libraries_util.install_all_packages(GUI_util.window, "wordclouds_util",
                                              ['wordcloud', 'numpy', 'matplotlib', 'ntpath', 'PIL', 'stanza', 'csv']):
    sys.exit(0)

# The script uses Andreas Christian Mueller WordCloud package
# https://amueller.github.io/word_cloud/

import os
from collections import Counter
import numpy as np
from PIL import Image

import pandas as pd
from collections import defaultdict
import tkinter.messagebox as mb
import matplotlib.pyplot as plt  # pip install matplotlib
import csv
import ntpath  # to split the path from filename
import stanza

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator, get_single_color_func

import IO_files_util
import IO_user_interface_util

try:
    stanza.download('en')
except BaseException:
    import IO_internet_util

    IO_internet_util.check_internet_availability_warning("wordclouds_util.py (stanza.download(en))")


# Written by Tony C. Gu
# Users could use websites such as https://www.remove.bg/ or others to remove image backgrounds
def change_transparent_to_white(img):
    """
    Converts transparent pixels in image to non-alpha white
    :param img: the Image to be changed
    :return: the Image with transparent pixel changed to white
    """
    img = img.convert("RGBA")
    datas = img.getdata()

    new_data = []
    for item in datas:
        if item[3] == 0:  # if alpha value is zero, it is transparent
            new_data.append((255, 255, 255, 255))
        else:
            new_data.append(item)

    img.putdata(new_data)
    return img


def change_white_to_transparent(img):
    """
    Converts RGB-white pixels to alpha-white (transparent) pixels
    param img: the Image to be changed
    return: the Image with white pixel changed to transparent
    """
    img = img.convert("RGBA")
    datas = img.getdata()

    new_data = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:  # if it is white
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

    img.putdata(new_data)
    return img


# Obsolete
# def transform_format(val):
#     val = np.where(val == 0, 255, val)
#     return val


class GroupedColorFunc(object):
    """
    Create a color function object which assigns DIFFERENT SHADES of
    specified colors to certain words based on the color to words mapping.

    Uses wordcloud.get_single_color_func

    Parameters
    ----------
    color_to_words : dict(str -> list(str))
    A dictionary that maps a color to the list of words.

    default_color : str
    Color that will be assigned to a word that's not a member
    of any value from color_to_words.
    """

    def __init__(self, color_to_words, default_color):
        self.color_func_to_words = [
            (self.get_single_color(color), set(words))
            for (color, words) in color_to_words.items()]

        self.default_color_func = self.get_single_color(default_color)

    @staticmethod
    def get_single_color(color):
        color = color[1:-1]
        color_list = color.split(", ")
        return 'rgb({:.0f}, {:.0f}, {:.0f})'.format(int(color_list[0]), int(color_list[1]), int(color_list[2]))

    def get_color_func(self, word):
        """Returns a single_color_func associated with the word"""
        try:
            color_func = next(
                color_func for (color_func, words) in self.color_func_to_words
                if word in words)
        except StopIteration:
            color_func = self.default_color_func

        return color_func

    def __call__(self, word, **kwargs):
        return self.get_color_func(word)


# CYNTHIA: wordcloud function particularly designed for SVO
def SVOWordCloud(svoFile, doc, outputDir, transformed_image_mask, prefer_horizontal):
    # read SVO result in
    svo_df = pd.read_csv(svoFile)
    svo_df = svo_df.fillna("")
    words_list = []
    # red for S, blue for V, green for O
    red_code = "(250, 0, 0)"
    blue_code = "(0, 0, 250)"
    green_code = "(0, 250, 0)"
    default_code = "(169, 169, 169)"  # grey
    color_list = {
        red_code: [],
        blue_code: [],
        green_code: []
    }
    for _, row in svo_df.iterrows():
        if row["S"] != "":
            # check if the strings contains special character
            words_list.append(" ".join(["".join(filter(str.isalnum, s)) for s in row["S"].lower().split(" ")]))
            color_list[red_code].append(
                " ".join(["".join(filter(str.isalnum, s)) for s in row["S"].lower().split(" ")]))
        if row["V"] != "":
            words_list.append(" ".join(["".join(filter(str.isalnum, s)) for s in row["V"].lower().split(" ")]))
            color_list[blue_code].append(
                " ".join(["".join(filter(str.isalnum, s)) for s in row["V"].lower().split(" ")]))
        if row["O"] != "":
            words_list.append(" ".join(["".join(filter(str.isalnum, s)) for s in row["O"].lower().split(" ")]))
            color_list[green_code].append(
                " ".join(["".join(filter(str.isalnum, s)) for s in row["O"].lower().split(" ")]))
    words_count_dict = Counter(words_list)
    # print (words_count_dict)
    if len(transformed_image_mask) != 0:
        wc = WordCloud(width=800, height=800, max_words=1000, prefer_horizontal=prefer_horizontal,
                       mask=transformed_image_mask,
                       contour_width=3, contour_color='firebrick', background_color='white').generate_from_frequencies(
            words_count_dict)
    else:
        wc = WordCloud(width=800, height=800, max_words=1000, prefer_horizontal=prefer_horizontal, contour_width=3,
                       background_color='white').generate_from_frequencies(words_count_dict)
    grouped_color_func = GroupedColorFunc(color_list, default_code)
    wc.recolor(color_func=grouped_color_func)
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    output_file_name = IO_files_util.generate_output_file_name(doc, '', outputDir, '.png', 'WC', 'img')
    wc.to_file(output_file_name)
    return output_file_name


# for label separate column with separate color only
def processColorList(current_text, color_to_words, csv_field_color_list, my_file):
    cur_list = []
    column_color = {}

    for item in csv_field_color_list:
        if item != '|':
            cur_list.append(item)
        else:
            for key in cur_list[:-1]:
                column_color[key] = cur_list[-1]
            cur_list = []

    reader = csv.DictReader(my_file)  # read rows into a dictionary format
    for row in reader:  # read a row as {column1: value1, column2: value2,...}
        for (k, v) in row.items():  # go over each column name and value
            if k in column_color:
                if " " in v:
                    color_to_words[column_color[k]] += ["".join(filter(str.isalnum, s)) for s in v.lower().split(" ")]
                else:
                    color_to_words[column_color[k]].append("".join(filter(str.isalnum, v.lower())))
                current_text += v.lower() + " "
    return current_text, color_to_words


# add bg_image_flag parameter to indicate whether to add background image
def display_wordCloud_sep_color(doc, output_dir, text, color_to_words, transformed_image_mask, collocation,
                                prefer_horizontal, bg_image=None, bg_image_flag=False):
    # stopwords dealt with in main function
    stopwords = ''
    c_wid = 0 if bg_image_flag else 3
    if len(transformed_image_mask) != 0:
        wc = WordCloud(collocations=collocation, width=800, height=800, max_words=1000,
                       prefer_horizontal=prefer_horizontal, stopwords=stopwords, mask=transformed_image_mask,
                       contour_width=c_wid, contour_color='firebrick', background_color='white').generate(text)
    else:
        wc = WordCloud(collocations=collocation, width=800, height=800, max_words=1000,
                       prefer_horizontal=prefer_horizontal, stopwords=stopwords, contour_width=c_wid,
                       background_color='white').generate(text)
    default_color = "(169, 169, 169)"  # dark grey; black is 0,0,0
    grouped_color_func = GroupedColorFunc(color_to_words, default_color)
    wc.recolor(color_func=grouped_color_func)
    plt.figure(figsize=(8, 8), facecolor=None)
    output_file_name = IO_files_util.generate_output_file_name(doc, '', output_dir, '.png', 'WC', 'img')
    if bg_image_flag and bg_image is not None:
        img = change_white_to_transparent(wc.to_image())
        img = img.resize(bg_image.size)
        img = Image.alpha_composite(bg_image, img)
        plt.imshow(img, interpolation='bilinear')
        plt.axis("off")
        # title must be set before layout
        plt.tight_layout(pad=0)
        # Save the image in the output folder
        plt.figure()
        plt.axis('off')
        fig = plt.imshow(img, interpolation='nearest')
        plt.savefig(output_file_name,
                    bbox_inches='tight',
                    pad_inches=0,
                    format='png',
                    dpi=300)
    else:
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        wc.to_file(output_file_name)
    return output_file_name


def display_wordCloud(doc, inputDir, outputDir, textToProcess, doNotListIndividualFiles, transformed_image_mask,
                      collocation, prefer_horizontal, bg_image=None, bg_image_flag=True):
    comment_words = ' '
    # stopwords = set(STOPWORDS)
    # for val in textToProcess:
    #     # typecast each val to string
    #     val = str(textToProcess)
    # # split the value
    # tokens = val.split()
    # # Converts each token into lowercase and delete non-alphabetic chars
    # regex = re.compile('[^a-zA-Z]')
    # for i in range(len(tokens)):
    #     tokens[i] = regex.sub('', tokens[i].lower())
    # for words in tokens:
    #     comment_words = comment_words + words + ' '
    c_wid = 0 if bg_image_flag else 3
    if len(transformed_image_mask) != 0:
        wordcloud = WordCloud(width=800, height=800,
                              background_color='white',
                              max_words=1000,
                              mask=transformed_image_mask,
                              prefer_horizontal=prefer_horizontal,
                              # stopwords = stopwords,
                              contour_width=c_wid,
                              contour_color='firebrick',
                              # min_font_size = 10, collocations=collocation).generate(comment_words)
                              # min_font_size = 10, collocations=collocation).generate(textToProcess)
                              collocations=collocation).generate(textToProcess)
    else:
        wordcloud = WordCloud(width=800, height=800,
                              background_color='white',
                              max_words=1000,
                              prefer_horizontal=prefer_horizontal,
                              # stopwords = stopwords,
                              contour_width=c_wid,
                              # min_font_size = 10, collocations=collocation).generate(comment_words)
                              # min_font_size = 10, collocations = collocation).generate(textToProcess)
                              collocations=collocation).generate(textToProcess)
    if doNotListIndividualFiles:
        plt.title(inputDir)
        output_file_name = IO_files_util.generate_output_file_name('', inputDir, outputDir, '.png', 'WC', 'img')
    else:
        plt.title(ntpath.basename(doc))
        output_file_name = IO_files_util.generate_output_file_name(doc, '', outputDir, '.png', 'WC', 'img')
    # plot the WordCloud image
    plt.figure(figsize=(8, 8), facecolor=None)
    if bg_image_flag and bg_image is not None:
        img = change_white_to_transparent(wordcloud.to_image())
        img = img.resize(bg_image.size)
        img = Image.alpha_composite(bg_image, img)
        plt.imshow(img, interpolation='bilinear')
        plt.axis("off")
        # title must be set before layout
        plt.tight_layout(pad=0)
        # Save the image in the output folder
        plt.figure()
        plt.axis('off')
        fig = plt.imshow(img, interpolation='nearest')
        plt.savefig(output_file_name,
                    bbox_inches='tight',
                    pad_inches=0,
                    format='png',
                    dpi=300)
    else:
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        wordcloud.to_file(output_file_name)
    return output_file_name


# Returns 2 booleans:
#   the first one tells user that the program MUST exit;
#   the second that a file is empty and processing moves to the next file
def check_file_empty(current_text, doc, n_docs, num_empty_docs):
    if len(current_text) == 0:
        num_empty_docs = num_empty_docs + 1
        if n_docs == 1:
            mb.showerror(title='File empty',
                         message='The file ' + doc + ' is empty.\n\nPlease, use another file and try again.')
            return True, True, num_empty_docs  # must exit script
        else:
            IO_user_interface_util.timed_alert(GUI_util.window, 3000, 'Empty file',
                                               'The file ' + doc + ' is empty.')
        return False, True, num_empty_docs
    else:
        return False, False, num_empty_docs


# Modified by Tony @ 01/23/2022: added bg_image and bg_image_flag
def process_csv_columns(doc, input_dir, output_dir, open_output_files, csv_field_color_list,
                        do_not_list_individual_files, bg_image=None, bg_image_flag=False):
    transformed_image_mask = []
    collocation = False
    prefer_horizontal = .9
    current_text = ''
    color_to_words = defaultdict(list)
    with open(doc, 'r', encoding='utf-8', errors='ignore') as my_file:
        if len(csv_field_color_list) != 0:
            # process csvField_color_list
            current_text, color_to_words = processColorList(current_text, color_to_words, csv_field_color_list, my_file)
            tempOutputfile = display_wordCloud_sep_color(doc, output_dir, current_text, color_to_words,
                                                         transformed_image_mask, collocation, prefer_horizontal,
                                                         bg_image=bg_image, bg_image_flag=bg_image_flag)
            files_to_open.append(tempOutputfile)
            IO_files_util.OpenOutputFiles(GUI_util.window, open_output_files, files_to_open)


def python_wordCloud(input_filename, input_dir, output_dir, selected_image, use_contour_only, prefer_horizontal,
                     lemmatize, exclude_stopwords, exclude_punctuation, lowercase, differentPOS_differentColors,
                     differentColumns_differentColors, csv_field_color_list, do_not_list_individual_files,
                     open_output_files, collocation):
    # https://www.geeksforgeeks.org/generating-word-cloud-python/
    # Python program to generate WordCloud
    # for a more sophisticated Python script see
    #   https://www.datacamp.com/community/tutorials/wordcloud-python
    #   they provide code to display wc in a selected image
    global files_to_open
    files_to_open = []

    transformed_image_mask = []

    use_contour_only = not use_contour_only

    if prefer_horizontal == 0:
        prefer_horizontal = .9
    else:
        prefer_horizontal = 1

    if differentColumns_differentColors or input_filename[-3:] == 'csv':
        fileType = '.csv'
    else:
        fileType = '.txt'

    img = None

    if len(selected_image) != 0:
        # In order to create a shape for your wordcloud, first you need to find a PNG file to use as the mask.
        # Mask images may be in different formats, resulting in different outcomes and confusing the WordCloud function.
        # The masking function requires all white part of the mask should be 255 not 0 (integer type).
        # This value represents the "intensity" of the pixel.
        # Values of 255 are pure white, whereas values of 1 are black.
        # You can use the provided function below to transform your mask if your mask has the same format as above.
        # Note! If you have a mask with a background that is not 0, but 1 or 2, adjust the function to match your mask.
        img = Image.open(selected_image)
        img = change_transparent_to_white(img)
        image_mask = np.array(img)
        print("image_mask (SHOULD ALL BE 0 VALUES)", image_mask)
        number_images = len(image_mask.shape)
        # if i == 1:  # only print once
        print("\n\n\nnumber_images", number_images)

        # Transform your mask into a new one that will work with the function:
        if number_images == 1:
            transformed_image_mask = np.ndarray((image_mask.shape[0]), np.int32)
        elif number_images == 2:
            transformed_image_mask = np.ndarray((image_mask.shape[0], image_mask.shape[1]), np.int32)
        elif number_images == 3:
            transformed_image_mask = np.ndarray((image_mask.shape[0], image_mask.shape[1], image_mask.shape[2]),
                                                np.int32)
        else:
            return
        transformed_image_mask = image_mask

        # for j in range(len(image_mask)):
        #     transformed_image_mask[j] = list(map(transform_format, image_mask[j]))

        # Check the expected result of your mask
        # if i == 1:  # only print once
        print("transformed_image_mask (SHOULD ALL BE 255 VALUES)", transformed_image_mask)

    # can only process a single conll table
    if len(input_dir) > 0:
        fileType = '.txt'

    if differentColumns_differentColors:
        process_csv_columns(input_filename, input_dir, output_dir, open_output_files, csv_field_color_list,
                            do_not_list_individual_files, bg_image=img, bg_image_flag=use_contour_only)
        return

    input_docs = IO_files_util.getFileList(input_filename, input_dir, fileType, silent=False)
    n_docs = len(input_docs)
    if n_docs == 0:
        return

    # RED for NOUNS, BLUE for VERBS, GREEN for ADJECTIVES, GREY for ADVERBS
    # YELLOW for anything else; no longer used
    red_code = "(250, 0, 0)"
    blue_code = "(0, 0, 250)"
    green_code = "(0, 250, 0)"
    grey_code = "(80, 80, 80)"
    yellow_code = "(255, 255, 0)"
    color_to_words = {
        red_code: [],  # red/nouns
        blue_code: [],  # blue/verbs
        green_code: [],  # green/adjs
        grey_code: [],  # grey/advs
        yellow_code: []  # all other word POS types; no longer used
    }
    combined_text = ''
    current_text = ''
    text_to_process = ''
    stopwords = ''
    num_empty_docs = 0
    i = 0

    run_stanza = False
    if fileType == '.txt':
        # Always tokenize to convert each token to lowercase to avoid the same improper word to appear with lower and
        # upper case at the beginning of a sentence
        stanford_nlp = stanza.Pipeline(lang='en', processors='tokenize, mwt')
        run_stanza = True
        if lemmatize:
            # stanza.download('en')  # set the annotator that gives postag
            stanford_nlp = stanza.Pipeline(lang='en', processors='tokenize, mwt, lemma')
            run_stanza = True
        if exclude_stopwords:
            stopwords = set(STOPWORDS)
            # stanza.download('en')  # set the annotator that gives postag
            stanford_nlp = stanza.Pipeline(lang='en', processors='tokenize, mwt')
            run_stanza = True
        if exclude_punctuation or differentPOS_differentColors:
            # stanza.download('en')  # set the annotator that gives postag
            stanford_nlp = stanza.Pipeline(lang='en', processors='tokenize, mwt, pos')
            run_stanza = True
        if lemmatize and (exclude_punctuation or differentPOS_differentColors):
            # stanza.download('en')  # set the annotator that gives postag
            stanford_nlp = stanza.Pipeline(lang='en', processors='tokenize, mwt, lemma, pos')
            run_stanza = True

        # stanford_nlp = stanza.Pipeline(lang='en', processors='tokenize, ner, mwt, pos, lemma')

    if run_stanza:
        start_time = IO_user_interface_util.timed_alert(GUI_util.window, 3000, 'Running STANZA & wordcloud',
                                                        'Started running STANZA and wordcloud at', True,
                                                        'Please, be patient. Depending upon the number of documents '
                                                        'processed this may take a few minutes.',
                                                        True, '', False)
    for doc in input_docs:
        i += 1
        head, tail = os.path.split(doc)
        print("Processing file " + str(i) + "/" + str(n_docs) + ' ' + tail)
        if doc.endswith('.csv'):  # processing CoNLL table that contains pos values
            try:
                df = pd.read_csv(doc)
                postags_ = df['POStag']
                forms_ = df['Form']
                lemmas_ = df['Lemma']

                # text: summing tokens in each line together
                if lemmatize:
                    current_text = " ".join(lemmas_)
                    words_ = lemmas_
                else:
                    current_text = " ".join(forms_)
                    words_ = forms_

                for j in range(len(words_)):
                    # print("word: ", forms_[i])
                    # print("pos: ", postags_[i])
                    # RED for NOUNS, BLUE for VERBS, GREEN for ADJECTIVES, GREY for ADVERBS
                    # YELLOW for anything else; no longer used
                    if len(postags_[j]) >= 2 and postags_[j][0:2] == "VB":
                        color_to_words[blue_code].append(words_[j])
                    elif len(postags_[j]) >= 2 and postags_[j][0:2] == "NN":
                        color_to_words[red_code].append(words_[j])
                    elif len(postags_[j]) >= 2 and postags_[j][0:2] == "JJ":
                        color_to_words[green_code].append(words_[j])
                    elif len(postags_[j]) >= 2 and postags_[j][0:2] == "RB":
                        color_to_words[grey_code].append(words_[j])
                    # else:  # should not process? Skip any other tags?
                    #     color_to_words[yellow_code].append(words_[j])
                    if postags_[j][0:2] == "NN" or postags_[j][0:2] == "VB" or \
                            postags_[j][0:2] == "JJ" or postags_[j][0:2] == "RB":
                        text_to_process = text_to_process + ' ' + words_[j]
            except BaseException:
                mb.showwarning(title='Not a CoNLL table',
                               message=doc + " is not a CoNLL table.\n\nPlease, select in input a proper csv CoNLL "
                                             "file with Form, Lemma, and POStag columns and try again.")
                return
        elif doc.endswith('.txt'):
            with open(doc, 'r', encoding='utf-8', errors='ignore') as my_file:
                text_to_process = ''
                current_text = my_file.read()
                # check for empty file
                error, error2, num_empty_docs = check_file_empty(current_text, doc, n_docs, num_empty_docs)
                if error:
                    return
                if error2:
                    continue
                if run_stanza:
                    text_to_process = ''
                    annotated = stanford_nlp(current_text)
                    for sent_id in range(len(annotated.sentences)):
                        for word in annotated.sentences[sent_id].words:
                            # RED for NOUNS, BLUE for VERBS, GREEN for ADJECTIVES, GREY for ADVERBS
                            # YELLOW for anything else; no longer used
                            if lemmatize:
                                word_str = word.lemma
                            else:
                                word_str = word.text
                            if exclude_stopwords:
                                if word_str in stopwords:
                                    continue  # do not process stopwords & punctuation marks
                            # print("   word_str",word_str,"word.pos",word.pos)
                            # convert to lower case for same improper words that may appear after a full stop
                            if lowercase:
                                if word_str == '':
                                    word_str = word.text
                                word_str = word_str.lower()
                            if exclude_punctuation:
                                if word.pos == "PUNCT":
                                    continue  # do not process stopwords & punctuation marks
                            if word.pos == "NOUN":
                                color_to_words[red_code].append(word_str)
                            elif word.pos == "VERB":
                                color_to_words[blue_code].append(word_str)
                            elif word.pos == "ADJ":
                                color_to_words[green_code].append(word_str)
                            elif word.pos == "ADV":
                                color_to_words[grey_code].append(word_str)
                            if differentColumns_differentColors:
                                if word.pos in ("NOUN", "VERB", "ADJ", "ADV"):
                                    text_to_process = text_to_process + ' ' + word_str
                            else:
                                text_to_process = text_to_process + ' ' + word_str
                    if len(text_to_process) == 0:
                        text_to_process = current_text

        if not do_not_list_individual_files or len(input_filename) > 0:
            if differentPOS_differentColors:
                temp_output_file = display_wordCloud_sep_color(doc, output_dir, text_to_process, color_to_words,
                                                               transformed_image_mask, collocation, prefer_horizontal,
                                                               bg_image=img, bg_image_flag=use_contour_only)
            else:
                temp_output_file = display_wordCloud(doc, input_dir, output_dir, text_to_process,
                                                     do_not_list_individual_files,
                                                     transformed_image_mask, collocation, prefer_horizontal,
                                                     bg_image=img,
                                                     bg_image_flag=use_contour_only)
            files_to_open.append(temp_output_file)
            # write an output txt file that can be used for internet wordclouds services
            if lemmatize or exclude_stopwords:
                with open(temp_output_file[:-8] + '.txt', 'w', encoding='utf-8', errors='ignore') as f:
                    f.write(text_to_process)
        combined_text = combined_text + text_to_process

    if len(input_dir) > 0:
        if differentPOS_differentColors:
            temp_output_file = display_wordCloud_sep_color(input_dir, output_dir, combined_text, color_to_words,
                                                           transformed_image_mask, collocation, prefer_horizontal,
                                                           bg_image=img, bg_image_flag=use_contour_only)
        else:
            temp_output_file = display_wordCloud(input_dir, input_dir, output_dir, combined_text,
                                                 do_not_list_individual_files,
                                                 transformed_image_mask, collocation, prefer_horizontal, bg_image=img,
                                                 bg_image_flag=use_contour_only)
        files_to_open.append(temp_output_file)
        # write an output txt file that can be used for internet wordclouds services
        if lemmatize or exclude_stopwords:
            with open(temp_output_file[:-8] + '.txt', 'w', encoding='utf-8', errors='ignore') as f:
                f.write(combined_text)
            n_docs_rewritten = 1
            if not do_not_list_individual_files:
                n_docs_rewritten = n_docs + 1
            mb.showwarning(title='txt files',
                           message='The Python 3 wordclouds algorithm has produced ' + str(
                               n_docs_rewritten) + ' txt file(s) without stopwords, punctuation, and with lemmatized '
                                                   'words, depending upon your selected filter options.\n\n'
                                                   'You will find the file(s) in your output directory.\n\n'
                                                   'You can use the file(s) to produce wordclouds using any of the '
                                                   'Internet wordcloud services.')

    if len(combined_text) < 1:
        print('All ' + str(num_empty_docs) + ' txt files in your input directory\n' + str(
            input_dir) + ' are empty.\n\nPlease, check your directory and try again.')
        mb.showerror(title='Files empty',
                     message='All ' + str(num_empty_docs) + ' txt files are empty in your input directory\n' + str(
                         input_dir) + '\n\nPlease, check your directory and try again.')
    if num_empty_docs > 0:
        mb.showerror(title='Empty file(s)',
                     message=str(num_empty_docs) + ' file(s) empty in the input directory\n' + str(input_dir) +
                             '\n\nFile(s) listed in command line. Please, make sure to check the file(s) content.')

    if open_output_files <= 6:
        IO_files_util.OpenOutputFiles(GUI_util.window, open_output_files, files_to_open)
    else:
        mb.showwarning(title='Too many wordclouds files to open',
                       message='The Python 3 wordclouds algorithm has produced ' + str(
                           open_output_files) + ' image files, too many to open automatically.\n\n'
                                                'Please, check your output directory for ' + str(
                           open_output_files) + ' wordclouds image files produced.')
    # plt.show()
