import os
import re
import IO_files_util
import csv

"""
NGramsCoOccurrences implements the ability to generate NGram and CoOccurrences data
"""
class NGramsCoOccurrences():
    outputFileName = "N-Grams_CoOccurrences_Statistics.csv";
    fileToPlotName = "Searched_N-Grams.csv";
    WCOFileName = "Searched_CoOccurrences.csv";
    docPCIDCouplesFilePath = "";
    scaleData = False;
    normalizeByPCID = False;
    lemma = False;
    fullInfo = False;
    considerAsSeparateGroups = True;
    normalize = True;

    """
        Creates an NGramsCoOccurrences class which can be used to generate the queried data and/or save it
        
        outputFolder: str
            The folder in which to save the output data to
        inputFolder: str
            The input folder in which to find the input data
        dateFormat: str
            The format to extract the date from the file name
        datePos: str
            The position in which the date can be extracted split by the itemsDelimiter
        wordsLists: list
            The input list to generate NGrams or CoOccurrences
        checkCoOccList: bool
            Should we check for co-occurrences
        groupingOption: bool
            TODO: Implement this
        itemsDelimiter: str
            The delimiter for file names used to extract the date
        docPCIDCouplesFilePath: str
            TODO: Implement this
        scaleData: bool
            TODO: Implement this
        normalizeByPCID: bool
            TODO: Implement this
        lemma: bool
            TODO: Implement this
        fullInfo: bool
            TODO: Implement this
        considerAsSeparateGroups: bool
            TODO: Implement this
        normalize: bool
            TODO: Implement this
    """
    def __init__(self, outputFolder, inputFolder, dateFormat, datePos, wordsLists, checkCoOccList,
                 groupingOption, itemsDelimiter, docPCIDCouplesFilePath, scaleData, normalizeByPCID,
                 lemma, fullInfo, considerAsSeparateGroups, normalize):

        self.outputFolder = outputFolder
        self.inputFolder = inputFolder
        self.dateFormat = dateFormat
        self.datePos = datePos
        self.wordsLists = wordsLists
        self.checkCoOccList = checkCoOccList
        self.groupingOption = groupingOption
        self.itemsDelimiter = itemsDelimiter
        self.docPCIDCouplesFilePath = docPCIDCouplesFilePath
        self.scaleData = scaleData
        self.normalizeByPCID = normalizeByPCID
        self.lemma = lemma
        self.fullInfo = fullInfo
        self.considerAsSeparateGroups = considerAsSeparateGroups
        self.normalize = normalize

    """
        Finds all NGrams and/or CoOccurrences using the specified data at the time of construction
        
        Returns:
            ngrams_results: dict
                The ngram results in the following format: {word : [word, date, file] }
            coOcc_results: dict
                The co-occurrence results in the following format: {combination : [combination, date, file] }
                TODO: support multi-co-occurrence combinations; only 2 word combinations supported
    """
    def run(self):
        files = IO_files_util.getFileList('', self.inputFolder, ".txt")  # get all input files
        word_list = [word.lower() for word in self.wordsLists]  # generate word list
        ngram_results = {}  # prepare ngram results, TODO: set to none if only checking co-occurrences
        coOcc_results = {} if self.checkCoOccList else None  # prepare co-occurrences results

        # preparation
        for word in word_list:
            ngram_results[word] = []

        for file in files:  # iterate over each file
            # extract the date from the file name
            date, dateStr = IO_files_util.getDateFromFileName(file, self.itemsDelimiter, self.datePos, self.dateFormat)
            if date == '':
                continue # TODO: Warn user this file has a bad date

            # read the file
            with open(os.path.join(self.inputFolder, file), 'r') as f:
                lines = f.readlines() # read input
                words = re.split("\W+", "\n".join(lines))  # split on punctuation to avoid trailing punctuation
                # iterate over each word
                for index, w in enumerate(words):
                    word = w.lower()  # TODO: lemmatize here if appropriate

                    # TODO: add check if generating ngrams
                    if word in word_list:  # add word if in search list
                            ngram_results[word].append([word, date, os.path.join(self.inputFolder, file)])
                    # check if generating co-occurrences
                    if self.checkCoOccList:
                        for co in word_list:
                            coOcc = co.lower()
                            if coOcc != word:
                                # generate 2 word combinations for difference occurrence arrangements
                                comb1 = [word, coOcc].join(" ")
                                comb2 = [coOcc, word].join(" ")
                                if comb1 in words:  # found co-occurrence
                                    if coOcc_results[comb1] is None:  # instantiate empty list if not yet seen
                                        coOcc_results[comb1] = []
                                    coOcc_results[comb1].append(
                                        [comb1, date, os.path.join(self.inputFolder, file)])

                                if comb2 in words:  # found co-occurrence
                                    if coOcc_results[comb2] is None:  # instantiate empty list if not yet seen
                                        coOcc_results[comb2] = []
                                    coOcc_results[comb2].append(
                                        [comb2, date, os.path.join(self.inputFolder, file)])

        return ngram_results, coOcc_results  # return results

    """
        Saves the data passed in the expected format of `NGramsCoOccurrences.run()`
        
        ngrams_results: dict
                The ngram results in the following format: {word : [word, date, file] }
            coOcc_results: dict
                The co-occurrence results in the following format: {combination : [combination, date, file] }
    """
    def save(self, ngram_results, coOcc_results):
        if coOcc_results is not None:
            with open(os.path.join(self.outputFolder, self.WCOFileName), 'w', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow(["combination", "date", "file"])
                for label, res in coOcc_results.items():
                    writer.writerows(res)

        if ngram_results is not None:
            with open(os.path.join(self.outputFolder, self.outputFileName), 'w', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow(["word", "date", "file"])
                for label, res in ngram_results.items():
                    writer.writerows(res)


# Test NGramsCoOccurrences logic
if __name__ == "__main__":
    outputFolder = "./../../Output/ngram-test/"
    inputFolder = "/Users/apollo/emory/fall-2021/QTM446W/NLP-Suite/lib/sampleData/newspaperArticles/"
    dateFormat = "mm-dd-yyyy"
    datePos = 4
    wordsLists = ["man", "woman"]
    checkCoOccList = False
    groupingOption = ""
    itemsDelimiter = "_"
    docPCIDCouplesFilePath = ""
    scaleData = False
    normalizeByPCID = False
    lemma = False
    fullInfo = False
    considerAsSeparateGroups = True
    normalize = True

    ng = NGramsCoOccurrences(outputFolder, inputFolder, dateFormat, datePos, wordsLists, checkCoOccList,
                 groupingOption, itemsDelimiter, docPCIDCouplesFilePath, scaleData, normalizeByPCID,
                 lemma, fullInfo, considerAsSeparateGroups, normalize)
    ngr, cor = ng.run()