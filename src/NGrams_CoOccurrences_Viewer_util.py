# written by Rafael Piloto October 2021
# re-written by Roberto Franzosi October 2021
# completed by Austin Cai October 2021

import pandas as pd
import csv
import numpy as np
import pprint
from nltk.tokenize import sent_tokenize, word_tokenize

import IO_files_util
import IO_csv_util

"""
NGramsCoOccurrences implements the ability to generate NGram and CoOccurrences data
"""


def run(inputDir="relative_path_here",
        outputDir="relative_path_here",
        n_grams_viewer=False,
        CoOcc_Viewer=True,
        search_wordsLists=None,
        dateOption=False,
        temporal_aggregation='year',
        number_of_years=0,
        datePos=2,
        dateFormat="mm-dd-yyyy",
        itemsDelimiter="_",
        temporalAggregation="",
        viewer_options_list=[]):

    if search_wordsLists is None:
        search_wordsLists = []
    checkCoOccList = False

    case_sensitive = False
    normalize = False
    scaleData = False
    useLemma = False
    fullInfo = False
    # print(str(viewer_options_list))
    if 'sensitive' in str(viewer_options_list):
        case_sensitive = True
    if 'insensitive' in str(viewer_options_list):
        case_sensitive = False
    if 'Normalize' in str(viewer_options_list):
        normalize = True
    if 'Scale' in str(viewer_options_list):
        scaleData = True
    if 'Lemmatize' in str(viewer_options_list):
        useLemma = True


    ################################## OPTIONS NEEDED TO BE ADD TO GUI #################################################
    byNumberOfYears = 0
    byYear = False
    byQuarter = False
    byMonth = False
    if temporal_aggregation=='group of years':
        byNumberOfYears = number_of_years  # number of years in one aggregated chunk
        byYear = True  # set to True if want to aggregate by years
        aggregateBy = 'year'
    elif temporal_aggregation=='year':
        byYear = True  # set to True if want to aggregate by years
        aggregateBy = 'year'
    elif temporal_aggregation=='quarter':
        byQuarter = True  # set to True if want to aggregate by years
        aggregateBy = 'quarter'
    elif temporal_aggregation=='month':
        byMonth = True  # set to True if want to aggregate by years
        aggregateBy = 'month'
    files = IO_files_util.getFileList('', inputDir, ".txt")  # get all input files
    original_search_word = search_wordsLists + ""
    search_word_list = search_wordsLists.split(',')
    ngram_results = {}
    for i in range(len(search_word_list)):
        if not case_sensitive:
            search_word_list[i] = search_word_list[i].lstrip().lower()
        else:
            search_word_list[i] = search_word_list[i].lstrip()

    if n_grams_viewer and byYear and dateOption:
        yearList = []
        for file in files:  # iterate over each file
            date, dateStr = IO_files_util.getDateFromFileName(file, itemsDelimiter, datePos, dateFormat)
            yearList.append(int(dateStr[-4:]))
        yearList = sorted(np.unique(yearList))
        for word in search_word_list:
            ngram_results[word] = {}
            for y in yearList:
                ngram_results[word][y] = {"Search Word(s)": word,
                                          "Frequency": 0}

        pprint.pprint(ngram_results)
        docIndex = 1
        for file in files:  # iterate over each file
            docIndex += 1
            # extract the date from the file name
            date, dateStr = IO_files_util.getDateFromFileName(file, itemsDelimiter, datePos, dateFormat)
            if date == '':
                continue  # TODO: Warn user this file has a bad date; done in getDate
            year = int(dateStr[-4:])
            f = open(file, "r", encoding='utf-8', errors='ignore')
            docText = f.read()
            f.close()
            if not case_sensitive:
                docText = docText.lower()
            tokens_ = word_tokenize(docText)
            for collocationIndex in range(len(tokens_)):
                token = tokens_[collocationIndex]
                for search_word in search_word_list:
                    iterations = search_word.count(' ')
                    split_search_word = search_word.split(' ')
                    # split_search_word=str(split_search_word).
                    length_of_search_list = len(split_search_word)
                    checker = False
                    if iterations > 0:
                        for i in range(length_of_search_list):
                            if i == 0:
                                if split_search_word[i] == token:
                                    # print("yes")
                                    checker = True
                            else:
                                if checker and (collocationIndex + i) < len(tokens_):
                                    if split_search_word[i] == tokens_[collocationIndex + i]:
                                        # print("yes")
                                        checker = True
                                    else:
                                        checker = False
                        if checker:
                            ngram_results[search_word][year]["Frequency"] += 1
                    else:
                        if search_word == token:
                            # print(search_word, 'FOUND!!!!!', file)
                            ngram_results[search_word][year]["Frequency"] += 1

        if byNumberOfYears > 1:
            pprint.pprint(ngram_results)
            curYear = yearList[0]
            newYear = curYear + byNumberOfYears - 1
            newYearStringList = []
            newYearIntList = []
            while curYear < yearList[-1]:
                yearChunk = str(curYear) + "-" + str(newYear)
                newYearStringList.append(yearChunk)
                newYearIntList.append((curYear, newYear))
                curYear = newYear + 1
                newYear = curYear + byNumberOfYears - 1
            aggregated_ngram_results = {}
            for word in search_word_list:
                aggregated_ngram_results[word] = {}
                for y in newYearStringList:
                    aggregated_ngram_results[word][y] = {"Search Word(s)": word,
                                                         "Frequency": 0}
                for year in yearList:
                    for i in range(len(newYearIntList)):
                        if newYearIntList[i][0] <= year <= newYearIntList[i][1]:
                            aggregated_ngram_results[word][newYearStringList[i]]["Frequency"] += \
                                ngram_results[word][year]["Frequency"]
            ngram_results = aggregated_ngram_results
            pprint.pprint(aggregated_ngram_results)

    if n_grams_viewer and dateOption and (byMonth or byQuarter):
        monthList = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
        yearList = []
        for file in files:  # iterate over each file
            date, dateStr = IO_files_util.getDateFromFileName(file, itemsDelimiter, datePos, dateFormat)
            yearList.append(int(dateStr[-4:]))
        yearList = sorted(np.unique(yearList))

        for word in search_word_list:
            ngram_results[word] = {}
            for y in yearList:
                ngram_results[word][str(y)] = {}
                for m in monthList:
                    ngram_results[word][str(y)][m] = {"Search Word(s)": word,
                                                      "Frequency": 0}
        docIndex = 1
        for file in files:  # iterate over each file
            docIndex += 1
            # extract the date from the file name
            date, dateStr = IO_files_util.getDateFromFileName(file, itemsDelimiter, datePos, dateFormat)
            if date == '':
                continue  # TODO: Warn user this file has a bad date; done in getDate
            year = dateStr[-4:]
            month = dateStr[0:2]
            f = open(file, "r", encoding='utf-8', errors='ignore')
            docText = f.read()
            f.close()
            if not case_sensitive:
                docText = docText.lower()
            tokens_ = word_tokenize(docText)
            for collocationIndex in range(len(tokens_)):
                token = tokens_[collocationIndex]
                for search_word in search_word_list:
                    iterations = search_word.count(' ')
                    split_search_word = search_word.split(' ')
                    # split_search_word=str(split_search_word).
                    length_of_search_list = len(split_search_word)
                    checker = False
                    if iterations > 0:
                        for i in range(length_of_search_list):
                            if i == 0:
                                if split_search_word[i] == token:
                                    # print("yes")
                                    checker = True
                            else:
                                if checker and (collocationIndex + i) < len(tokens_):
                                    if split_search_word[i] == tokens_[collocationIndex + i]:
                                        # print("yes")
                                        checker = True
                                    else:
                                        checker = False
                        if checker:
                            ngram_results[search_word][year][month]["Frequency"] += 1
                    else:
                        if search_word == token:
                            # print(search_word, 'FOUND!!!!!', file)
                            ngram_results[search_word][year][month]["Frequency"] += 1

        if byQuarter:
            quarter_ngram_results = {}
            for word, yearDict in ngram_results.items():
                quarter_ngram_results[word] = {}
                for year, monthDict in yearDict.items():
                    q1Sum, q2Sum, q3Sum, q4Sum = 0, 0, 0, 0
                    quarter_ngram_results[word][year] = {}
                    for month, freqDict in monthDict.items():
                        if 1 <= int(month) <= 3:
                            q1Sum += freqDict["Frequency"]
                        if 4 <= int(month) <= 6:
                            q2Sum += freqDict["Frequency"]
                        if 7 <= int(month) <= 9:
                            q3Sum += freqDict["Frequency"]
                        if 10 <= int(month) <= 12:
                            q4Sum += freqDict["Frequency"]
                    quarter_ngram_results[word][year]["quarter 1"] = {"Search Word(s)": word,
                                                                      "Frequency": q1Sum}
                    quarter_ngram_results[word][year]["quarter 2"] = {"Search Word(s)": word,
                                                                      "Frequency": q2Sum}
                    quarter_ngram_results[word][year]["quarter 3"] = {"Search Word(s)": word,
                                                                      "Frequency": q3Sum}
                    quarter_ngram_results[word][year]["quarter 4"] = {"Search Word(s)": word,
                                                                      "Frequency": q4Sum}
            pprint.pprint(quarter_ngram_results)
            ngram_results = quarter_ngram_results
    if not CoOcc_Viewer:
        # prepare co-occurrences results
        coOcc_results_binary = {}
    else:
        docIndex = 1
        coOcc_results_binary = {}
        for file in files:  # iterate over each file
            coOcc_results_binary[file] = {"Search Word(s)": original_search_word, "CO-Occurrence": "NO",
                                          "Document ID": docIndex,
                                          "Document": IO_csv_util.undressFilenameForCSVHyperlink(file)}
            docIndex += 1
            collocation = ''
            collocation_found = False
            index = 0
            # extract the date from the file name
            if dateOption:
                date, dateStr = IO_files_util.getDateFromFileName(file, itemsDelimiter, datePos, dateFormat)
                if date == '':
                    continue  # TODO: Warn user this file has a bad date; done in getDate
            else:
                date = ''
                f = open(file, "r", encoding='utf-8', errors='ignore')
                docText = f.read()
                f.close()
                if not case_sensitive:
                    docText = docText.lower()
                tokens_ = word_tokenize(docText)
                coOcc_results = {}
                for collocationIndex in range(len(tokens_)):
                    if coOcc_results_binary[file]["CO-Occurrence"] == "YES":
                        break
                    token = tokens_[collocationIndex]
                    if CoOcc_Viewer:

                        for search_word in search_word_list:
                            iterations = search_word.count(' ')
                            split_search_word = search_word.split(' ')
                            # split_search_word=str(split_search_word).
                            length_of_search_list = len(split_search_word)
                            checker = False
                            if iterations > 0:
                                for i in range(length_of_search_list):
                                    if i == 0:
                                        if split_search_word[i] == token:
                                            # print("yes")
                                            checker = True
                                    else:
                                        if checker and (collocationIndex + i) < len(tokens_):
                                            if split_search_word[i] == tokens_[collocationIndex + i]:
                                                # print("yes")
                                                checker = True
                                            else:
                                                checker = False
                                if checker:
                                    coOcc_results[search_word] = 2
                            else:
                                if search_word == token:
                                    # print(search_word, 'FOUND!!!!!', file)
                                    coOcc_results[search_word] = 1
                        co_occurrence_checker = True
                        for word in search_word_list:
                            if word not in list(coOcc_results.keys()):
                                co_occurrence_checker = False
                                break
                        if co_occurrence_checker:
                            coOcc_results_binary[file]["CO-Occurrence"] = "YES"
                            break

    NgramsFileName=''
    coOccFileName=''

    if n_grams_viewer:
        if 'group' in temporal_aggregation:
            label='group_'+str(byNumberOfYears)
        else:
            label=temporal_aggregation
        NgramsFileName = IO_files_util.generate_output_file_name('', inputDir, outputDir, '.csv',
                                                                 'N-grams_' + label)
    if CoOcc_Viewer:
        coOccFileName = IO_files_util.generate_output_file_name('', inputDir, outputDir, '.csv', 'Co-Occ')

    # pprint.pprint(coOcc_results_binary)
    NgramsFileName, coOccFileName = save(NgramsFileName, coOccFileName, ngram_results, coOcc_results_binary, aggregateBy, temporal_aggregation)
    return NgramsFileName, coOccFileName


"""
    Saves the data passed in the expected format of `NGramsCoOccurrences.run()`
    
    ngrams_results: dict
            The ngram results in the following format: {word : [word, date, file] }
        coOcc_results: dict
            The co-occurrence results in the following format: {combination : [combination, date, file] }
"""

def save(NgramsFileName, coOccFileName, ngram_results, coOcc_results, aggregateBy, temporal_aggregation):
    if len(ngram_results)>0:
        dfList = []  # create a list of dataframes: one df for one search word
        if aggregateBy == 'year':
            for word, yearDict in ngram_results.items():
                df = pd.DataFrame(columns=[word, temporal_aggregation])
                for year, freqDict in yearDict.items():
                    df = df.append({word: freqDict["Frequency"], temporal_aggregation: year}, ignore_index=True)
                dfList.append(df)
            newdfCur = dfList[0].copy()  # let newdfCur be the first df in the dfList
            newdf = newdfCur.copy()
            for i in range(1, len(dfList)):  # one by one join next search word's dataframe with the current dataframe
                newdfNext = dfList[i].copy()  # get the next dataframe
                newdf = newdfCur.merge(newdfNext, on=temporal_aggregation, how="left")  # join on year
                newdfCur = newdf.copy()

            # these 3 lines will move the 'year' column to position 0, which is the left most position
            # inserting headers
            newdf.insert(0, 'year_temp', newdf[temporal_aggregation])
            newdf.drop(temporal_aggregation, axis=1, inplace=True)
            newdf.rename(columns={'year_temp': temporal_aggregation}, inplace=True)
        else:
            # aggregating by quarter or month
            for word, yearDict in ngram_results.items():
                df = pd.DataFrame(columns=[word, 'year', temporal_aggregation, "year-" + temporal_aggregation])
                for year, monthDict in yearDict.items():
                    for month, freqDict in monthDict.items():
                        if temporal_aggregation == 'quarter':
                            df = df.append({word: freqDict["Frequency"], "year": year, temporal_aggregation: month, "year-" + temporal_aggregation: year + "-Q" + month[-1]}, ignore_index=True)
                        else:
                            df = df.append({word: freqDict["Frequency"], "year": year, temporal_aggregation: month, "year-" + temporal_aggregation: year + "-" + month}, ignore_index=True)
                dfList.append(df)
            newdfCur = dfList[0].copy()
            newdf = newdfCur.copy()
            for i in range(1, len(dfList)):
                newdfNext = dfList[i].copy()
                newdf = newdfCur.merge(newdfNext, on=['year', temporal_aggregation, "year-" + temporal_aggregation],
                                       how="left")
                newdfCur = newdf.copy()
            # these 9 lines will move the 'year', 'month' or 'quarter', and 'year-month' column to the left most position
            newdf.insert(0, 'month_temp', newdf[temporal_aggregation])
            newdf.insert(0, 'year_temp', newdf['year'])
            newdf.insert(0, 'yearMonth_temp', newdf["year-" + temporal_aggregation])
            newdf.drop(temporal_aggregation, axis=1, inplace=True)
            newdf.drop('year', axis=1, inplace=True)
            newdf.drop("year-" + temporal_aggregation, axis=1, inplace=True)
            newdf.rename(columns={'month_temp': temporal_aggregation}, inplace=True)
            newdf.rename(columns={'year_temp': 'year'}, inplace=True)
            newdf.rename(columns={'yearMonth_temp': 'year-' + temporal_aggregation}, inplace=True)

        print(newdf)
        newdf.to_csv(NgramsFileName, encoding='utf-8', index=False)
    if len(coOcc_results)>0:
        # with open(os.path.join(WCOFileName, outputDir), 'w', encoding='utf-8') as f:
        with open(coOccFileName, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Search Word(s)", "CO-Occurrence", "Document ID", "Document"])
            for label, res in coOcc_results.items():
                writer.writerow([res["Search Word(s)"], res["CO-Occurrence"], res["Document ID"],
                                 IO_csv_util.dressFilenameForCSVHyperlink(res["Document"])])

    return NgramsFileName, coOccFileName
