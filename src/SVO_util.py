import pandas as pd
from nltk.stem import WordNetLemmatizer
# import stanza
# stanza.download('en')
# stannlp = stanza.Pipeline(lang='en', processors='tokenize,ner,mwt,pos,lemma')

import IO_files_util
import IO_user_interface_util
import Excel_util
import IO_csv_util

def count_frequency_two_svo(CoreNLP_csv, senna_csv, inputFilename, inputDir, outputDir) -> list:
    """
    Only triggered when both SENNA and CoreNLP ++ options are chosen.
    Counts the frequency of same and different SVOs and SVs in the SENNA and CoreNLP ++ results and lists them
    :param CoreNLP_csv: the path of the stanford core CoreNLP ++ csv file
    :param senna_csv: the path of the Senna csv file
    :param inputFilename: the input file name; used for generating output file name
    :param inputDir: the input directory name; used for generating output file name
    :param outputDir: the output directory name; used for generating output file name
    :return: [Freq table, Comparison table], where Freq table counts the frequency of same/different SVOs, and
        Comparison table lists all the same/different SVOs
    """

    def generate_key(S, V, O):
        """
        Converts strings S, V, O to a key with the format "{S}, {V}, {O}".
        If it is a S-V combination, the key would be "{S}, {V}"
        If it is a V-O combination, the key would be "{V}, {O}"
        :return:
        """
        key = ''
        if S:
            key += S.strip().lower() + ','

        key += V.strip().lower()

        if O:
            key += ',' + O.strip().lower()

        return key

    df = pd.DataFrame(columns=['Same SVO', 'Same SV', 'Different SVO', 'Different SV', 'Total SVO', 'Total SV'])
    CoreNLP_df = pd.read_csv(CoreNLP_csv)
    senna_df = pd.read_csv(senna_csv)
    open_ie_svo, open_ie_sv, senna_svo, senna_sv = set(), set(), set(), set()

    # Adding each row of SVO into the corresponding sets
    for i in range(len(CoreNLP_df)):
        if pd.notnull(CoreNLP_df.iloc[i, 4]):
            if not pd.isnull(CoreNLP_df.iloc[i, 5]) and not pd.isnull(CoreNLP_df.iloc[i, 3]):
                open_ie_svo.add(generate_key(S=CoreNLP_df.iloc[i, 3], V=CoreNLP_df.iloc[i, 4], O=CoreNLP_df.iloc[i, 5]))
            elif not pd.isnull(CoreNLP_df.iloc[i, 3]):
                open_ie_sv.add(generate_key(S=CoreNLP_df.iloc[i, 3], V=CoreNLP_df.iloc[i, 4], O=''))
            # elif not pd.isnull(CoreNLP_df.iloc[i, 5]):
            #     open_ie_sv.add(generate_key(S='', V=CoreNLP_df.iloc[i, 4], O=CoreNLP_df.iloc[i, 5]))
            # else:
            #     open_ie_sv.add(generate_key(S='', V=CoreNLP_df.iloc[i, 4], O=''))

    for i in range(len(senna_df)):
        if pd.notnull(senna_df.iloc[i, 4]):
            if not pd.isnull(senna_df.iloc[i, 3]) and not pd.isnull(senna_df.iloc[i, 5]):  # Has S, V, O
                senna_svo.add(generate_key(S=senna_df.iloc[i, 3], V=senna_df.iloc[i, 4], O=senna_df.iloc[i, 5]))
            elif not pd.isnull(senna_df.iloc[i, 3]):  # Has S, V
                senna_sv.add(generate_key(S=senna_df.iloc[i, 3], V=senna_df.iloc[i, 4], O=''))
            # elif not pd.isnull(senna_df.iloc[i, 5]):  # Has V, O
            #     senna_sv.add(generate_key(S='', V=senna_df.iloc[i, 4], O=senna_df.iloc[i, 5]))
            # else:  # Has V
            #     senna_sv.add(generate_key(S='', V=senna_df.iloc[i, 4], O=''))

    # Generating the stats
    same_svo = open_ie_svo.intersection(senna_svo)
    same_sv = open_ie_sv.intersection(senna_sv)
    diff_svo = open_ie_svo.symmetric_difference(senna_svo)
    diff_sv = open_ie_sv.symmetric_difference(senna_sv)
    total_svo = len(same_svo) + len(diff_svo)
    total_sv = len(same_sv) + len(diff_sv)

    df = df.append(pd.DataFrame([[len(same_svo), len(same_sv), len(diff_svo), len(diff_sv), total_svo, total_sv]],
                                columns=['Same SVO', 'Same SV', 'Different SVO', 'Different SV', 'Total SVO',
                                         'Total SV']), ignore_index=True)
    freq_output_name = IO_files_util.generate_output_file_name(inputFilename, inputDir, outputDir, '.csv',
                                                               'SENNA_CoreNLP_SVO_FREQ')
    df.to_csv(freq_output_name, index=False)

    # Listing all same and diff SV and SVOs
    compare_df = pd.DataFrame(columns=['Same', 'S', 'V', 'O', 'Different', 'S', 'V', 'O'])

    same_svo.update(same_sv)
    diff_svo.update(diff_sv)
    same, diff = [], []

    for svo in same_svo:
        splitted_svo = svo.split(',')
        s, v = splitted_svo[0], splitted_svo[1]
        o = splitted_svo[2] if len(splitted_svo) >= 3 else ''
        same.append((s, v, o))

    for svo in diff_svo:
        splitted_svo = svo.split(',')
        s, v = splitted_svo[0], splitted_svo[1]
        o = splitted_svo[2] if len(splitted_svo) >= 3 else ''
        tool = 'SENNA' if svo in senna_svo or svo in senna_sv else 'CoreNLP ++'
        diff.append((s, v, o, tool))

    if len(same) < max(len(same), len(diff)):
        same.extend([('', '', '')] * (len(diff) - len(same)))
    elif len(diff) < max(len(same), len(diff)):
        diff.extend([('', '', '')] * (len(same) - len(diff)))

    for svo1, svo2 in zip(same, diff):
        compare_df = compare_df.append(pd.DataFrame([['', svo1[0], svo1[1], svo1[2], svo2[3], svo2[0], svo2[1], svo2[2]]],
                                                    columns=['Same', 'S', 'V', 'O', 'Different', 'S', 'V', 'O']), ignore_index=True)

    # Outputting the file
    compare_outout_name = IO_files_util.generate_output_file_name(inputFilename, inputDir, outputDir, '.csv',
                                                                  'SENNA_CoreNLP_SVO_COMPARE')
    compare_df.to_csv(compare_outout_name, index=False)

    return [freq_output_name, compare_outout_name]


def combine_two_svo(CoreNLP_svo, senna_svo, inputFilename, inputDir, outputDir) -> str:
    """
    Combine the CoreNLP ++ results and Senna SVO results into one table; sorted by document ID then sentence ID
    :param CoreNLP ++_svo: the path of the stanford core CoreNLP ++ csv file
    :param senna_svo: the path of the Senna csv file
    :param inputFilename: the input file name; used for generating output file name
    :param inputDir: the input directory name; used for generating output file name
    :param outputDir: the output directory name; used for generating output file name
    :return: the name of the output csv file
    """
    columns = ['Tool', 'Document ID', 'Sentence ID', 'Document', 'S', 'V', 'O', 'LOCATION', 'TIME', 'Sentence']
    combined_df = pd.DataFrame(columns=columns)
    dfs = [(pd.read_csv(CoreNLP_svo), 'CoreNLP ++'), (pd.read_csv(senna_svo), 'Senna')]

    for df, df_name in dfs:
        for i in range(len(df)):
            new_row = [df_name, df.loc[i, 'Document ID'], df.loc[i, 'Sentence ID'], df.loc[i, 'Document'],
                       df.loc[i, 'S'],
                       df.loc[i, 'V'], df.loc[i, 'O'], df.loc[i, 'LOCATION'],
                       df.loc[i, 'TIME'], df.loc[i, 'Sentence']]
            combined_df = combined_df.append(pd.DataFrame([new_row], columns=columns), ignore_index=True)

    combined_df.sort_values(by=['Document ID', 'Sentence ID'], inplace=True)
    output_name = IO_files_util.generate_output_file_name(inputFilename, inputDir, outputDir, '.csv',
                                                          'SENNA_CoreNLP_SVO_COMBINE')
    combined_df.to_csv(output_name, index=False)

    return output_name

def visualize_Excel_chart(createExcelCharts, inputFilename, outputDir, filesToOpen, columns_to_be_plotted,
                              chartType, chartTitle, count_var, hover_label, outputFileNameType, column_xAxis_label):
        Excel_outputFilename = Excel_util.run_all(columns_to_be_plotted, inputFilename, outputDir,
                                                  outputFileLabel=outputFileNameType,
                                                  chart_type_list=[chartType],
                                                  chart_title=chartTitle,
                                                  column_xAxis_label_var=column_xAxis_label,
                                                  hover_info_column_list=hover_label,
                                                  count_var=count_var)
        return Excel_outputFilename

def filter_svo(window,svo_file_name, filter_s_fileName, filter_v_fileName, filter_o_fileName, lemmatize_s, lemmatize_v,lemmatize_o, outputDir, createExcelCharts=True):
    """
    Filters a svo csv file based on the dictionaries given, and replaces the original output csv file
    :param svo_file_name: the name of the svo csv file
    :param filter_s_fileName: the subject dict file path
    :param filter_v_fileName: the verb dict file path
    :param filter_o_fileName: the object dict file path
    """

    startTime = IO_user_interface_util.timed_alert(window, 2000, 'Analysis start',
                                                   'Started running the SVO filter algorithm at',
                                                   True, '', True)

    df = pd.read_csv(svo_file_name)
    filtered_df = pd.DataFrame(columns=df.columns)
    lemmatizer = WordNetLemmatizer()

    # Generating filter dicts
    if filter_s_fileName:
        s_set = open(filter_s_fileName, 'r', encoding='utf-8-sig', errors='ignore').read().split('\n')
        s_set = set(s_set)
    if filter_v_fileName:
        v_set = open(filter_v_fileName, 'r', encoding='utf-8-sig', errors='ignore').read().split('\n')
        v_set = set(v_set)
    if filter_o_fileName:
        o_set = open(filter_o_fileName, 'r', encoding='utf-8-sig', errors='ignore').read().split('\n')
        o_set = set(o_set)

    # Adding rows to filtered df
    for i in range(len(df)):
        subject, verb, object = '', '', ''
        if pd.notnull(df.loc[i, 'S']):
            # words = stannlp(df.loc[i, 'S'])
            # ((word.pos == "VERB") or (word.pos == "NN") or (word.pos == "NNS")):
            # subject = words.lemma
            subject = lemmatizer.lemmatize(df.loc[i, 'S'], 'n')
        if pd.notnull(df.loc[i, 'V']):
            verb = lemmatizer.lemmatize(df.loc[i, 'V'], 'v')
        if pd.notnull(df.loc[i, 'O']):
            object = lemmatizer.lemmatize(df.loc[i, 'O'], 'n')

        # The s_set, v_set, and o_set are sets. The “in” in set is equivalent to “==” in string.
        if subject and filter_s_fileName and subject not in s_set:
            continue
        if verb and filter_v_fileName and verb not in v_set:
            continue
        if object and filter_o_fileName and object not in o_set:
            continue

        # the next line does NOT replace the original SVO;
        #   must replace SVO with the values computed above: subject, verb, object
        if lemmatize_s:
            df.loc[i, 'S'] = subject
        if lemmatize_v:
            df.loc[i, 'V'] = verb
        if lemmatize_o:
            df.loc[i, 'O'] = object

        filtered_df = filtered_df.append(df.loc[i, :], ignore_index=True)

    IO_user_interface_util.timed_alert(window, 3000, 'Analysis end', 'Finished running SVO filter algorithm at', True, '', True,
                                       startTime, True)

    # Replacing the original csv file
    filtered_df.to_csv(svo_file_name, index=False)

    filesToOpen = []

    if IO_csv_util.GetNumberOfRecordInCSVFile(svo_file_name,encodingValue='utf-8')>1:

        Excel_outputFilename = visualize_Excel_chart(createExcelCharts, svo_file_name, outputDir, filesToOpen, [[3, 3]], 'bar',
                                            'Frequency Distribution of Subjects (filtered)', 1, [], 'S_bar',
                                            'Subjects (filtered)')
        if len(Excel_outputFilename) > 0:
            filesToOpen.append(Excel_outputFilename)

        Excel_outputFilename = visualize_Excel_chart(createExcelCharts, svo_file_name, outputDir, filesToOpen, [[4, 4]], 'bar',
                                            'Frequency Distribution of Verbs (filtered)', 1, [], 'V_bar',
                                            'Verbs (filtered)')
        if len(Excel_outputFilename) > 0:
            filesToOpen.append(Excel_outputFilename)

        Excel_outputFilename = visualize_Excel_chart(createExcelCharts, svo_file_name, outputDir, filesToOpen, [[5, 5]], 'bar',
                                            'Frequency Distribution of Objects (filtered)', 1, [], 'O_bar',
                                            'Objects (filtered)')
        if len(Excel_outputFilename) > 0:
            filesToOpen.append(Excel_outputFilename)

    return filesToOpen

if __name__ == '__main__':
    senna_csv = '/Users/admin/Desktop/EMORY/Academics/Spring_2021/SOC497R/test_output/SVO_Result/NLP_SENNA_SVO_Dir_test.csv'
    CoreNLP_csv = '/Users/admin/Desktop/EMORY/Academics/Spring_2021/SOC497R/test_output/SVO_Result/test-merge-svo.csv'
    count_frequency_two_svo(CoreNLP_csv, senna_csv)
