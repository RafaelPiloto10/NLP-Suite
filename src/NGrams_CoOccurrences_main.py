import os
import re
import IO_files_util
import IO_csv_util

class NGramsCoOcurrences():

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

    def run(self):
        files = IO_files_util.getFileList('', self.inputFolder, ".txt")
        word_list = [word.lower() for word in self.wordsLists]
        results = {}
        for word in word_list:
            results[word] = []

        for file in files:
            date, dateStr = IO_files_util.getDateFromFileName(file, self.itemsDelimiter, self.datePos, self.dateFormat)

            if date == '':
                continue # TODO: Warn user this file has a bad date

            with open(os.path.join(self.inputFolder, file), 'r') as f:
                lines = f.readlines()
                words = re.split("\W+", "\n".join(lines)) # Split on punctuation to avoid trailing punctuation
                for word in words:
                    if word.lower() in word_list:
                            results[word.lower()].append([word.lower(), date, os.path.join(self.inputFolder, file)])
        return results


if __name__ == "__main__":
    outputFolder = "./../../Output/ngram-test/";
    inputFolder = "/Users/apollo/emory/fall-2021/QTM446W/NLP-Suite/lib/sampleData/newspaperArticles/";
    dateFormat = "mm-dd-yyyy";
    datePos = 4;
    wordsLists = ["man", "woman"];
    checkCoOccList = "";
    groupingOption = "";
    itemsDelimiter = "_";
    docPCIDCouplesFilePath = "";
    scaleData = False;
    normalizeByPCID = False;
    lemma = False;
    fullInfo = False;
    considerAsSeparateGroups = True;
    normalize = True;

    ng = NGramsCoOcurrences(outputFolder, inputFolder, dateFormat, datePos, wordsLists, checkCoOccList,
                 groupingOption, itemsDelimiter, docPCIDCouplesFilePath, scaleData, normalizeByPCID,
                 lemma, fullInfo, considerAsSeparateGroups, normalize)
    ng.run()