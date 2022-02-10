Code Refactoring
----
Scroll to bottom to see notes.
### What is this?
* A tracker that records efforts to refactor code to maintain PEP-8 standards.
* Read more about PEP-8 [here](https://www.python.org/dev/peps/pep-0008/).

## Tracker

|                                   File Name | Cleaned? |   Date   |
|--------------------------------------------:|:--------:|:--------:|
| `            concreteness_analysis_util.py` |    No    |   N/A    |
| `                           config_util.py` |    No    |   N/A    |
| `            CoNLL_clause_analysis_util.py` |    No    |   N/A    |
| `    CoNLL_function_words_analysis_util.py` |    No    |   N/A    |
| `                CoNLL_k_sentences_util.py` |    No    |   N/A    |
| `              CoNLL_noun_analysis_util.py` |    No    |   N/A    |
| `             CoNLL_table_analyzer_main.py` |    No    |   N/A    |
| `       CoNLL_table_search_main_WEI_DAI.py` |    No    |   N/A    |
| `               CoNLL_table_search_util.py` |   Yes    | 2/6/2022 |
| `                            CoNLL_util.py` |    No    |   N/A    |
| `              CoNLL_verb_analysis_util.py` |   Yes    | 2/9/2022 |
| `                        constants_util.py` |    No    |   N/A    |
| `                     data_manager_main.py` |    No    |   N/A    |
| `                     data_manager_util.py` |    No    |   N/A    |
| `                           DB_SQL_main.py` |    No    |   N/A    |
| `      dictionary_items_sentenceID_util.py` |    No    |   N/A    |
| `                         download_jars.py` |    No    |   N/A    |
| `                  download_nltk_stanza.py` |    No    |   N/A    |
| `                     Excel_charts_main.py` |    No    |   N/A    |
| `                            Excel_util.py` |    No    |   N/A    |
| `   file_checker_converter_cleaner_main.py` |    No    |   N/A    |
| `                     file_checker_util.py` |    No    |   N/A    |
| `             file_classifier_date_util.py` |    No    |   N/A    |
| `                  file_classifier_main.py` |    No    |   N/A    |
| `              file_classifier_NER_util.py` |    No    |   N/A    |
| `                     file_cleaner_util.py` |    No    |   N/A    |
| `                    file_filename_util.py` |    No    |   N/A    |
| `  file_find_non_related_documents_util.py` |   Yes    | 2/6/2022 |
| `                     file_manager_main.py` |    No    |   N/A    |
| `                     file_matcher_main.py` |    No    |   N/A    |
| `                     file_matcher_util.py` |    No    |   N/A    |
| `                      file_merger_main.py` |    No    |   N/A    |
| `                      file_merger_util.py` |    No    |   N/A    |
| `               file_search_byWord_main.py` |    No    |   N/A    |
| `               file_search_byWord_util.py` |    No    |   N/A    |
| `               file_spell_checker_main.py` |    No    |   N/A    |
| `               file_spell_checker_util.py` |    No    |   N/A    |
| `            file_spell_checker_util_RF.py` |    No    |   N/A    |
| `    file_splitter_ByKeyword_conll_util.py` |    No    |   N/A    |
| `      file_splitter_ByKeyword_txt_util.py` |    No    |   N/A    |
| `           file_splitter_ByLength_util.py` |    No    |   N/A    |
| `           file_splitter_ByNumber_util.py` |    No    |   N/A    |
| `           file_splitter_ByString_util.py` |    No    |   N/A    |
| `              file_splitter_ByTOC_util.py` |    No    |   N/A    |
| `                    file_splitter_main.py` |    No    |   N/A    |
| `             file_splitter_merged_util.py` |    No    |   N/A    |
| `             file_summary_checker_util.py` |    No    |   N/A    |
| `              file_type_converter_util.py` |    No    |   N/A    |
| `                            Gephi_util.py` |    No    |   N/A    |
| `                     GIS_distance_main.py` |    No    |   N/A    |
| `                     GIS_distance_util.py` |    No    |   N/A    |
| `                      gis_distanceplot.py` |    No    |   N/A    |
| `                   GIS_file_check_util.py` |    No    |   N/A    |
| `                         GIS_foliumMap.py` |    No    |   N/A    |
| `                      GIS_geocode_util.py` |    No    |   N/A    |
| `                 GIS_Google_Earth_main.py` |    No    |   N/A    |
| `                  GIS_Google_Maps_util.py` |    No    |   N/A    |
| `                   GIS_Google_pin_util.py` |    No    |   N/A    |
| `                GIS_heatMapIntegration.py` |    No    |   N/A    |
| `           GIS_heatMapintegration_ver2.py` |    No    |   N/A    |
| `                          GIS_KML_util.py` |    No    |   N/A    |
| `                     GIS_location_util.py` |    No    |   N/A    |
| `                              GIS_main.py` |    No    |   N/A    |
| `                     GIS_pipeline_util.py` |    No    |   N/A    |
| `                            gis_simple.py` |    No    |   N/A    |
| `                           GUI_IO_util.py` |    No    |   N/A    |
| `                              GUI_util.py` |    No    |   N/A    |
| `        html_annotator_dictionary_util.py` |    No    |   N/A    |
| `         html_annotator_extractor_util.py` |    No    |   N/A    |
| `     html_annotator_extractor_util_NEW.py` |    No    |   N/A    |
| ` html_annotator_gender_dictionary_util.py` |    No    |   N/A    |
| `            html_annotator_gender_main.py` |    No    |   N/A    |
| `                   html_annotator_main.py` |    No    |   N/A    |
| `                           IO_csv_util.py` |    No    |   N/A    |
| `                         IO_files_util.py` |    No    |   N/A    |
| `                      IO_internet_util.py` |    No    |   N/A    |
| `                     IO_libraries_util.py` |    No    |   N/A    |
| `                         IO_setup_main.py` |    No    |   N/A    |
| `                        IO_string_util.py` |    No    |   N/A    |
| `                IO_user_interface_util.py` |    No    |   N/A    |
| `         knowledge_graphs_DBpedia_util.py` |    No    |   N/A    |
| `    knowledge_graphs_DBpedia_YAGO_main.py` |    No    |   N/A    |
| `         knowledge_graphs_WordNet_main.py` |    No    |   N/A    |
| `         knowledge_graphs_WordNet_util.py` |    No    |   N/A    |
| `            knowledge_graphs_YAGO_util.py` |    No    |   N/A    |
| `                             KWIC_main.py` |    No    |   N/A    |
| `                              lib_util.py` |    No    |   N/A    |
| `                           license_GUI.py` |    No    |   N/A    |
| `                               Lucene.jar` |    -     |    -     |
| `               narrative_analysis_main.py` |    No    |   N/A    |
| `      NGrams_CoOccurrences_Viewer_main.py` |    No    |   N/A    |
| `      NGrams_CoOccurrences_Viewer_util.py` |    No    |   N/A    |
| `                         NLP_menu_main.py` |    No    |   N/A    |
| `                      NLP_welcome_main.py` |    No    |   N/A    |
| `                   nominalization_main.py` |    No    |   N/A    |
| `                          nyt_api_call.py` |    No    |   N/A    |
| `                              refactor.md` |    No    |   N/A    |
| `                        reminders_util.py` |    No    |   N/A    |
| `          semantic_role_labeling_senna.py` |    No    |   N/A    |
| `                sentence_analysis_main.py` |    No    |   N/A    |
| `                sentence_analysis_util.py` |    No    |   N/A    |
| `          sentiment_analysis_ANEW_util.py` |    No    |   N/A    |
| `   sentiment_analysis_hedonometer_util.py` |    No    |   N/A    |
| `               sentiment_analysis_main.py` |    No    |   N/A    |
| `  sentiment_analysis_SentiWordNet_util.py` |    No    |   N/A    |
| `         sentiment_analysis_VADER_util.py` |    No    |   N/A    |
| `      shape_of_stories_clustering_util.py` |    No    |   N/A    |
| `                 shape_of_stories_main.py` |    No    |   N/A    |
| `      shape_of_stories_vectorizer_util.py` |    No    |   N/A    |
| `   shape_of_stories_visualization_util.py` |    No    |   N/A    |
| `                          shortcut_add.py` |    No    |   N/A    |
| `                       shortcut_remove.py` |    No    |   N/A    |
| `          social_science_research_main.py` |    No    |   N/A    |
| `       Stanford_CoreNLP_annotator_util.py` |    No    |   N/A    |
| `          Stanford_CoreNLP_clause_util.py` |    No    |   N/A    |
| `     Stanford_CoreNLP_coreference_main.py` |    No    |   N/A    |
| `     Stanford_CoreNLP_coreference_util.py` |    No    |   N/A    |
| `                 Stanford_CoreNLP_main.py` |    No    |   N/A    |
| `             Stanford_CoreNLP_NER_main.py` |    No    |   N/A    |
| `            Stanford_CoreNLP_port_util.py` |    No    |   N/A    |
| `            Stanford_CoreNLP_tags_util.py` |    No    |   N/A    |
| `                   statistics_csv_util.py` |    No    |   N/A    |
| `                   statistics_NLP_main.py` |    No    |   N/A    |
| `                   statistics_txt_util.py` |    No    |   N/A    |
| `                           string_util.py` |    No    |   N/A    |
| `                   style_analysis_main.py` |    No    |   N/A    |
| `        SVO_enhanced_dependencies_util.py` |    No    |   N/A    |
| `                              SVO_main.py` |    No    |   N/A    |
| `                              SVO_util.py` |    No    |   N/A    |
| `          TensorFlow_semantic_analysis.py` |    No    |   N/A    |
| `                             TIPS_util.py` |   Yes    | 2/6/2022 |
| `            topic_modeling_gensim_main.py` |    No    |   N/A    |
| `            topic_modeling_gensim_util.py` |    No    |   N/A    |
| `            topic_modeling_mallet_main.py` |   Yes    | 2/5/2022 |
| `            topic_modeling_mallet_util.py` |   Yes    | 2/5/2022 |
| `                           update_util.py` |    No    |   N/A    |
| `                           videos_util.py` |    No    |   N/A    |
| `                    visualization_main.py` |    No    |   N/A    |
| `             whats_in_your_corpus_main.py` |    No    |   N/A    |
| `                         word2vec_main.py` |    No    |   N/A    |
| `                         word2vec_util.py` |    No    |   N/A    |
| `                       wordclouds_main.py` |    No    |   N/A    |
| `                       wordclouds_util.py` |   Yes    | 2/6/2022 |
| `                  WordNet_Search_DOWN.jar` |    -     |    -     |
| `                    WordNet_Search_UP.jar` |    -     |    -     |

Notes
----
### 2/6/2022
* Fixed critical error on `topic_modeling_mallet_main.py` with lambda functions from refactoring
* Committed 3 files to refactor

### 2/5/2022
* Began refactoring efforts
* Committed 2 files `topic_modeling_mallet_*` to `current_stable` directly
* Established refactor branch.