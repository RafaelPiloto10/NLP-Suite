import sys
# import GUI_util
# import IO_libraries_util
# if not IO_libraries_util.install_all_packages(GUI_util.window,"GUI_IO_util", ['tkinter', 'os']):
#     sys.exit(0)

import os
import tkinter as tk
import tkinter.messagebox as mb

import config_util
import IO_files_util

# HELP messages
text_msg=''

introduction_main = "Welcome to this Python 3 script.\nFor brief general information about this script, click on the \"Read Me\" button.\nFor brief information on specific lines click on any of the \"?HELP\" buttons.\nFor longer information on various aspects of the script, click on the \"Open TIPS files\" button and select the pdf help file to view.\nAfter selecting an option, click on \"RUN\" (the RUN button is disabled until all I/O information has been entered).   To exit the script, click on \"QUIT\"."
# msg_fileButtonDisabled="\n\nIf the Select INPUT file button is greyed out because you previously selected an INPUT directory but you now wish to use a file as input, click on the Select INPUT directory button and press ESCape to make all INPUT options available."
# msg_dirButtonDisabled="\n\nIf the Select INPUT directory button is greyed out because you previously selected an INPUT file but you now wish to use a directory as input, click on the Select INPUT file button and press ESCape to make all INPUT options available."
msg_openExplorer="\n\nA small button appears next to the select directory button. Click on the button to open Windows Explorer on the directory displayed, if one is displayed, or on the directory where the NLP script is saved." 
msg_openFile="\n\nA small button appears next to the select file button. Click on the button to open the file, if one has been selected, as a check that you selected the correct file." # + msg_fileButtonDisabled
msg_Esc="\n\nPress the ESCape button to clear any previously selected options and start fresh."

msg_CoreNLP="Please, select the directory where you downloaded the Stanford CoreNLP software.\n\nYou can download Stanford CoreNLP from https://stanfordnlp.github.io/CoreNLP/download.html\n\nYou can place the Stanford CoreNLP folder anywhere on your machine. But... on some machines CoreNLP will not run unless the folder is inside the NLP folder.\n\nIf you suspect that CoreNLP may have given faulty results for some sentences, you can test those sentences directly on the Stanford CoreNLP website at https://corenlp.run\n\nYOU MUST BE CONNECTED TO THE INTERNET TO RUN CoreNLP."
msg_WordNet="Please, select the directory where you downloaded the WordNet lexicon database.\n\nYou can download WordNet from https://wordnet.princeton.edu/download/current-version."
msg_Mallet="Please, select the directory where you downloaded the Mallet topic modeling software."
msg_CoNLL="Please, select a CoNLL table that you would like to analyze.\n\nA CoNLL table is a file generated by the Python script StanfordCoreNLP.py. The CoreNLP script parses a set of text documents using the Stanford CoreNLP parser, providing a dependency tree for each sentence of the documents. In a CoNLL table, each token is labeled with a part-of-speech tag (POSTAG), a Dependency Relation tag (DEPREL), its dependency relation within the corresponding dependency tree, and other useful information." + msg_openFile
msg_corpusData="Please, select the directory where you store your TXT corpus to be analyzed. ALL TXT FILES PRESENT IN THE DIRECTORY WILL BE PARSED. NON TXT FILES WILL BE IGNORED. MOVE ANY TXT FILES YOU DO NOT WISH TO PROCESS TO A DIFFERENT DIRECTORY."  + msg_openExplorer # + msg_dirButtonDisabled
msg_anyData="Please, select the directory where you store the files to be analyzed. ALL FILES OF A SELECTED EXTENSION TYPE (pdf, docx, txt, csv, conll), PRESENT IN THE DIRECTORY WILL BE PROCESSED. ALL OTHER FILE TYPES WILL BE IGNORED."  + msg_openExplorer # + msg_dirButtonDisabled
msg_anyFile="Please, select the file to be analyzed (of any type: pdf, docx, txt, csv, conll)."  + msg_openFile
msg_txtFile="Please, select the TXT file to be analyzed." + msg_openFile # + msg_fileButtonDisabled
msg_csvFile="Please, select the csv file to be analyzed." + msg_openFile # + msg_fileButtonDisabled
msg_csv_txtFile="Please, select either a CSV file or a TXT file to be analyzed." + msg_openFile # + msg_fileButtonDisabled
msg_outputDirectory="Please, select the directory where the script will save all output files of any type (txt, csv, png, html)."  + msg_openExplorer
msg_outputFilename="Please, enter the OUTPUT file name. THE SELECT OUTPUT BUTTON IS DISABLED UNTIL A SEARCHED TOKEN HAS BEEN ENTERED.\n\nThe search result will be saved as a separated csv file with the file path and name entered. \n\nThe same information will be displayed in the command line."
msg_openOutputFiles="Please, tick the checkbox to open automatically (or not open) output csv file(s), including any Excel charts.\n\nIn the NLP Suite, all CSV FILES that contain information on web links or files with their path will encode this information as hyperlinks. If you click on the hyperlink, it will automatically open the file or take you to a website. IF YOU ARE A MAC USER, YOU MUST OPEN ALL CSV FILES WITH EXCEL, RATHER THAN NUMBERS, OR THE HYPERLINK WILL BE BARRED AND DISPLAYED AS A RED TRIANGLE.\n\nEXCEL HOVER-OVER EFFECT.  Most Excel charts have been programmed for hover-over effects, whereby when you pass the cursor over a point on the chart (hover over) some releveant information will be displayed (e.g., the sentence at that particular point).\n\nEXCEL EMPTY CHART AREA.  If the hover-over chart area is empty, with no chart displayed, enlarge the chart area by dragging any of its corners or by moving the zoom slide bar on the bottomg right-hand corner of Excel.\n\nEXCEL ENABLE MACROS.  The hover-over effect is achieved using VBA macros (Virtual Basic for Applications, Windows programming language). If Excel warns you that you need to enable macros, while at the same time warning you that macros may contain viruses, do the following: open an Excel workbook; click on File; slide cursor all the way down on the left-hand banner to Options; click on Trust Center; then on Trust Center Settings; then Macro Settings; Click on Enable all macros, then OK. The message will never appear again."
msg_multipleDocsCoNLL="\n\nFOR CONLL FILES THAT INCLUDE MULTIPLE DOCUMENTS, THE EXCEL CHARTS PROVIDE OVERALL FREQUENCIES ACROSS ALL DOCUMENTS. FOR SPECIFIC DOCUMENT ANALYSES, PLEASE USE THE GENERAL EXCEL OUTPUT FILE."


# location of this src python file
#one folder UP, the NLP folder
#subdirectory of script directory where config files are saved
#subdirectory of script directory where lib files are saved
#subdirectory of script directory where Google maps lib files are saved
#subdirectory of script directory where Excel lib files are saved
#subdirectory of script directory where lib files are saved
#subdirectory of script directory where lib files are saved
#subdirectory of script directory where lib files are saved
#subdirectory of script directory where gender names are saved
#global TIPSPath
#subdirectory of script directory where reminders file is saved

scriptPath = os.path.dirname(os.path.abspath(__file__))
NLPPath=os.path.normpath(os.path.dirname(os.path.abspath(__file__)) + os.sep + os.pardir)
configPath = os.path.join(NLPPath,'config')
libPath = os.path.join(NLPPath,'lib')
image_libPath = os.path.join(NLPPath,'lib'+os.sep+'images')
Google_heatmaps_libPath = os.path.join(NLPPath,'lib'+os.sep+'sampleHeatmap')
Excel_charts_libPath = os.path.join(NLPPath,'lib'+os.sep+'sampleCharts')
sentiment_libPath = os.path.join(NLPPath,'lib'+os.sep+'sentimentLib')
concreteness_libPath = os.path.join(NLPPath,'lib'+os.sep+'concretenessLib')
wordLists_libPath = os.path.join(NLPPath,'lib'+os.sep+'wordLists')
namesGender_libPath = os.path.join(NLPPath, 'lib'+os.sep+'namesGender')
GISLocations_libPath = os.path.join(NLPPath,'lib'+os.sep+'GIS')
TIPSPath = os.path.join(NLPPath,'TIPS')
remindersPath = os.path.join(NLPPath, 'reminders')

def placeWidget(x_coordinate,y_multiplier_integer,widget_name,sameY=False, centerX=False, basic_y_coordinate=90):
    #basic_y_coordinate = 90
    y_step = 40 #the line-by-line increment on the GUI
    if centerX:
        widget_name.place(relx=0.5, anchor=tk.CENTER, y=basic_y_coordinate + y_step*y_multiplier_integer)
    else:
        widget_name.place(x=x_coordinate, y=basic_y_coordinate + y_step*y_multiplier_integer)
    if sameY==False:
        y_multiplier_integer = y_multiplier_integer+1
    return y_multiplier_integer


if sys.platform == 'darwin': #Mac OS
    help_button_x_coordinate = 70
    labels_x_coordinate = 150  # start point of all labels in the second column (first column after ? HELP)
    labels_x_indented_coordinate = 160
    select_file_directory_button_width=23
    open_file_directory_button_width = 1
    open_file_directory_coordinate = 400
    entry_box_x_coordinate = 470 #start point of all labels in the third column (second column after ? HELP); where IO filename, dir, etc. are displayed
    read_button_x_coordinate = 70
    watch_videos_x_coordinate = 200
    open_TIPS_x_coordinate = 370
    open_reminders_x_coordinate = 570
    run_button_x_coordinate = 850
    quit_button_x_coordinate = 980

    # special internal GUI specific values
    SVO_2nd_column = 570

else: #windows and anything else
    help_button_x_coordinate = 50
    labels_x_coordinate = 120  # start point of all labels in the second column (first column after ? HELP)
    labels_x_indented_coordinate = 140
    select_file_directory_button_width=30
    open_file_directory_button_width = 3
    open_file_directory_coordinate = 350
    entry_box_x_coordinate = 400 #start point of all labels in the third column (second column after ? HELP)
    read_button_x_coordinate = 50
    watch_videos_x_coordinate = 170
    open_TIPS_x_coordinate = 350
    open_reminders_x_coordinate = 550
    run_button_x_coordinate = 840
    quit_button_x_coordinate = 960

    # special internal GUI specific values
    SVO_2nd_column = 520

basic_y_coordinate = 90
y_step = 40 #the line-by-line increment on the GUI

def get_basic_y_coordinate():
    return basic_y_coordinate
def get_y_step():
    return y_step
def get_help_button_x_coordinate():
    return help_button_x_coordinate

def get_labels_x_coordinate():
    return labels_x_coordinate

def get_labels_x_indented_coordinate():
    return labels_x_indented_coordinate

def get_entry_box_x_coordinate():
    return entry_box_x_coordinate

def get_open_file_directory_coordinate():
    return open_file_directory_coordinate

def about(Window, configFilename=''):
    mb.showinfo(title='About the NLP Suite', message='The NLP Suite is a package designed for text data analytics and visualization.\n\n\
The bulk of the package consists of over 120 (and growing) Python 3 scripts plus a handful of Java scripts.\n\n\
The target user of the NLP Suite is a humanist or social scientist with ZERO computer science background working with small data (from a single document to thousands of documents).\n\n\
Graphical User Interface (GUI) provide user friendly access to sophisticated computational tools.\n\n\
Each GUI comes with HELP? buttons with minimal explanation on each widget on the GUI, a ReadMe button with minimal explanation of the overall GUI and the tools invoked, short videos on the most important GUIs, on what they do and how they work, pdf TIPS files with more in-depth explanations of the computational tools behind the GUI, and Reminders that the user can turn ON and OFF.\n\n\
Over 100 (and growing) pdf TIPS files provide in-depth help to users on a large number of topics.\n\n\
The NLP Suite package relies on a large number of freeware, mostly open source, data analytics and visualization packages. The core text analytics (parsing and a variety of annotators - gender, quote, coreference, NER, sentiment, OpenIE - are carried out via Stanford CoreNLP. Frequencies are visualized in Excel charts with hover-over effects; netoworks are visualized via Gephi; GIS maps via Google Earth Pro and Google Maps. WordNet, Gensim, Mallet, NLTK are also used for a variety of specialized text analysis tasks.')

# The function displays the contributors to the development of the NLP Suite
def list_team(Window, configFilename=''):
    mb.showinfo(title='NLP Suite Contributors', message='The NLP Suite was conceived and designed by Roberto Franzosi at Emory University.\n\n\
Several Emory undergraduate students have contributed over the years to the development of NLP algorithms:\n\n\
        Matthew Chau\n\
        Jian Chen\n\
        Wei Dai\n\
        Wenqin Dong\n\
        Yilin Dong\n\
        Yuhang Feng\n\
        Jack Hester\n\
        Ziyang Hu\n\
        Hang Jiang\n\
        Josh Karol\n\
        Brett Landau\n\
        Rafael Piloto\n\
        Ishan Saran\n\
        Gabriel Wang\n\
        Yi Wang\n\
        Angel Xie\n\
        Catherine Xie\n\
        Doris Zhou\n\n\
JOIN THE TEAM: If you want to contribute to the continued development of the NLP Suite, please write to Roberto Franzosi at rfranzo@emory.edu or join directly via GitHub at https://github.com/NLP-Suite/NLP-Suite\n\n\
LICENSE: The NLP Suite is freely distributed under a GNU License Agreement.\n\n\
ACKNOWLEDGMENT: Acknowledgment of the use of the package in the form of citation would be greatly appreciated (click on the button How to cite).\n\n\
BUGS: If you find and fix bugs, keeping us informed would also be greatly appreciated.')

def cite_NLP(Window, configFilename=''):
    mb.showinfo(title='How to cite NLP Suite', message='Franzosi, Roberto. 2020. NLP Suite: A collection of natural language processing tools.\n\nGitHub: https://github.com/NLP-Suite/NLP-Suite\n\n\
The following papers are based on the NLP Suite tools:\n\n\
Franzosi, Roberto. 2020. "What’s in a Text? Bridging the Gap Between Quality and Quantity in the Digital Era." Quality & Quantity. DOI: https://doi.org/10.1007/s11135-020-01067-6\n\n\
Unpublished papers:\n\n\
Franzosi, Roberto, Wenqin Dong, Yilin Dong, Yi Wang. 2020. "Social Movements Research: How Natural Language Processing (NLP) Can Help." Unpublished manuscript.\n\n\
Franzosi, Roberto, Wenqin Dong, Yuhang Feng, Gabriel Wang. 2020. "Automatic Information Extraction of the Narrative Elements Who, What, When, and Where." Unpublished manuscript.\n\n\
Franzosi, Roberto, Wenqin Dong, Alberto Purpura. 2020. "The Shape of Stories." Unpublished manuscript.')

#configFilename with no path;
#configArray contains all the IO files and paths
#configArray is computed by setup_IO_configArray in config_util 
def exit_window(window,configFilename, configArray):
    if configFilename!="NLP-config.txt":
        # check whether the current IO configuration
        #	is different from the saved configuration
        #	if changed you want to ask the question
        config_util.saveConfig(window,configFilename, configArray)
        # if config_util.checkSavedConfig(configFilename, configArray)==False:
        # 	msgbox_save = tk.messagebox.askyesnocancel("Save Input/Output Configuration", "Since the paths configuration has changed (i.e., input and output paths), would you like to save the paths configuration? \n\nIf you save the paths configuration you will not need to enter them again next time you run this Python script.")
        # 	if msgbox_save == True: #yes
        # 		config_util.saveConfig(window,configFilename, configArray)
        # 	elif msgbox_save is None: #cancel
        # 		window.focus_force()
        # 		return
    window.destroy()
    exit(0)


# missingIO is called from GUI_util
def check_missingIO(window,missingIO,config_filename,silent=False):
    Run_Button_Off=False
    #do not check IO requirements for NLP.py; too many IO options available depending pon the sript run
    if config_filename=="NLP-config.txt" or config_filename=="social-science-research-config.txt":
        # RUN button always active since several options are available and IO gets checked in the respective scripts
        Run_Button_Off=False
        missingIO=''
    if len(missingIO)>0:
        if not silent:
            mb.showwarning(title='Warning', message='The required information in the input/output fields listed below is missing:\n\n' + missingIO + '\n\nThe RUN button is disabled until the required information for all Input/Output fields is entered.\n\nPlease, enter the required I/O information.')
        Run_Button_Off=True
    if Run_Button_Off==True:
        run_button_state="disabled"
    else:
        run_button_state="normal"
    window.focus_force()
    return run_button_state

# set input/output file name based on IO_util selectFile
#changeVar is the name of the IO FIELD (.get()) that needs to be displayed (e.g., filename) 
#changeVar1 is the name of the IO BUTTON that needs to be disabled in the case of mutuallyexclusive options
# def selectFile_set_options(window, config_input_output_options,IsInputFile,checkCoNLL,changeVar,changeVar1,title,fileType,extension,input_main_dir_path):
#     currentFilename=changeVar.get()
#     if len(changeVar.get())>0:
#         initialFolder=os.path.dirname(changeVar.get())
#     else:
#         initialFolder=''
#     #get the file
#     if IsInputFile==True:
#         filename= IO_files_util.selectFile(window, IsInputFile, checkCoNLL, changeVar, changeVar1, title, fileType, extension, None, initialFolder)
#     else:
#         filename= IO_files_util.selectFile(window, IsInputFile, checkCoNLL, changeVar, changeVar1, title, fileType, extension, outputFilename, None, initialFolder)
#     if len(filename)==0:
#         changeVar.set(currentFilename)
#     else:
#         input_main_dir_path.set('')

# #changeVar is the name of the IO FIELD (.get()) that needs to be displayed (e.g., softwareDir)
# #changeVar1 is the name of the IO BUTTON that needs to be disabled in the case of mutuallyexclusive options
# #title is the name that will appear when selecting the directory, e.g., "Select Stanford CoreNLP directory"
# def selectDirectory_set_options(window, changeVar,changeVar1,title,config_input_output_options,inputFilename,inputMainDir=False):
#     currentDirectory=changeVar.get()
#     if len(changeVar.get())>0:
#         initialFolder=os.path.dirname(changeVar.get())
#     else:
#         initialFolder=''
#     #get the directory
#     directoryName=IO_files_util.selectDirectory(window, changeVar, changeVar1, title, initialFolder)
#     # try:  # if the inputFilename button is not present this would throw an error
#     # 	changeVar1.config(state="normal")
#     # except:
#     # 	pass
#     if directoryName=='':
#         changeVar.set(currentDirectory)
#         print(changeVar.get())
#     else:
#         if inputMainDir==True:
#             try:
#                 changeVar1.set('') # inputFilename
#             except:
#                 pass
#             print('changeVar1',changeVar1.get())
#             try:
#                 changeVar.set('testa di cazzo') # input_main_dir_path
#             except:
#                 pass
#             print('changeVar',changeVar.get())
#     return directoryName

from tkinter import Toplevel
def Dialog2Display(title: str):
    Dialog2 = Toplevel(height=1000, width=1000)

# The function places and displays a message for each ? HELP button in the GUIs
def place_help_button(window,x_coordinate,y_coordinate,text_title,text_msg):
    if text_title=='Help':
        text_title='NLP Suite Help'
    def msg_box():
        mb.showinfo(title=text_title, message=text_msg)
    tk.Button(window, text='? HELP', command=msg_box).place(x=x_coordinate,y=y_coordinate)

# The function displays the info for the ReadMe button in the GUIs
def readme_button(Window, xCoord, yCoord, text_title,text_msg):
    if text_title=='Help':
        text_title='NLP Suite Help'
    mb.showinfo(title=text_title, message=text_msg)

# http://effbot.org/tkinterbook/menu.htm
def menu_widget(window,textCaption, lower_bound, upper_bound, default_value):
    master = tk.Tk()
    master.focus_force()

    tk.Label(master,width=len(textCaption),text=textCaption).grid(row=0)
    master.title(masterTitle)

    def get_value():
        global val
        val = s.get()
        top.destroy()
        top.update()

    def _delete_window():
        mb.showwarning(title = "Invalid Operation", message = "Please click OK to save your choice of parameter.")

    tk.Button(top, text='OK', command=lambda: get_value()).pack()
    return val

def slider_widget(window,textCaption, lower_bound, upper_bound, default_value):
    top = tk.Toplevel(window)
    l = tk.Label(top, text= textCaption)
    l.pack()
    s = tk.Scale(top, from_= lower_bound, to=upper_bound, orient=tk.HORIZONTAL)
    s.set(default_value)
    s.pack()

    def get_value():
        global val
        val = s.get()
        top.destroy()
        top.update()

    def _delete_window():
        mb.showwarning(title = "Invalid Operation", message = "Please click OK to save your choice of parameter.")

    top.protocol("WM_DELETE_WINDOW", _delete_window)

    tk.Button(top, text='OK', command=lambda: get_value()).pack()
    window.wait_window(top)
    return val

# TODO
# 2 widgets max for now; should allow more, dynamically
# called by
def enter_value_widget(masterTitle,textCaption,numberOfWidgets=1,defaultValue='',textCaption2='',defaultValue2=''):
    value1=defaultValue

    # TODO should not restrict to 2; should have a loop
    if numberOfWidgets==2:
        # TODO should have a list and break it up assigning values in a loop
        value2=defaultValue2
    master = tk.Tk()
    master.focus_force()

    tk.Label(master,width=len(textCaption),text=textCaption).grid(row=0)
    # TODO should not restrict to 2; should have a loop
    if numberOfWidgets==2:
        tk.Label(master, width=len(textCaption2),text=textCaption2).grid(row=1)

    master.title(masterTitle)
    # the width in tk.Entry determines the overall width of the widget;
    #   MUST be entered
    #   + 30 to add room for - [] and X in a widget window
    e1 = tk.Entry(master,width=len(masterTitle)+30)
    # TODO 2 could be a larger number; should have a loop
    if numberOfWidgets==2:
        e2 = tk.Entry(master,width=len(masterTitle)+30)

    e1.grid(row=0, column=1)
    # TODO 2 could be a larger number; should have a loop
    if numberOfWidgets==2:
        e2.grid(row=1, column=1)

    e1.insert(len(textCaption), defaultValue) # display a default value
    # TODO 2 could be a larger number; should have a loop
    if numberOfWidgets==2:
        e2.insert(len(textCaption2), defaultValue2) # display a default value

    tk.Button(master,
              text='OK',
              command=master.quit).grid(row=3,
                                        column=0,
                                        sticky=tk.W,
                                        pady=4)
    master.mainloop()
    value1=str(e1.get())
    # TODO 2 could be a larger number; should have a loop
    if numberOfWidgets==2:
        value2=str(e2.get())
    master.destroy()
    # convert to list; value1 is checked for length in calling function
    #   so do not convert if empty or its length will be the length of ['']
    # if value1!='':
    #     value1=list(value1.split(" "))
    return value1, value2
