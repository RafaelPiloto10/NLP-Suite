import sys
# import GUI_util
# import IO_libraries_util
# if not IO_libraries_util.install_all_packages(GUI_util.window,"GUI_IO_util", ['tkinter', 'os']):
#     sys.exit(0)

import os
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb

import config_util
import IO_internet_util
import webbrowser

# HELP messages
text_msg=''

introduction_main = "Welcome to this Python 3 script.\nFor brief general information about this script, click on the \"Read Me\" button.\nFor brief information on specific lines click on any of the \"?HELP\" buttons.\nFor longer information on various aspects of the script, click on the \"Open TIPS files\" button and select the pdf help file to view.\nAfter selecting an option, click on \"RUN\" (the RUN button is disabled until all I/O information has been entered).   Click on \"CLOSE\" to exit."
# msg_fileButtonDisabled="\n\nIf the Select INPUT file button is greyed out because you previously selected an INPUT directory but you now wish to use a file as input, click on the Select INPUT directory button and press ESCape to make all INPUT options available."
# msg_dirButtonDisabled="\n\nIf the Select INPUT directory button is greyed out because you previously selected an INPUT file but you now wish to use a directory as input, click on the Select INPUT file button and press ESCape to make all INPUT options available."
msg_openExplorer="\n\nA small button appears next to the select directory button. Click on the button to open Windows Explorer on the directory displayed, if one is displayed, or on the directory where the NLP script is saved." 
msg_openFile="\n\nA small button appears next to the select file button. Click on the button to open the file, if one has been selected, as a check that you selected the correct file." # + msg_fileButtonDisabled
msg_Esc="\n\nPress the ESCape button to clear any previously selected options and start fresh."

msg_IO_config="The default or GUI-specific config files are 2-columns csv files with the 4 I/O labels - Input filename with path, Input files directory, Input files secondary directory, Output files directory - in the first column and the file or directory path in the second column.\n\nThe fields Input filename with path and Input files directory are MUTUALLY EXCLUSIVE. YOU CAN ONLY HAVE ONE OR THE OTHER BUT NOT BOTH.\n\nA couple of scripts in the NLP Suite require two input directories (e.g., for source and target files, as in social_science_researh_main and file_classifier_main)."

msg_IO_setup="Please, using the dropdown menu, select the type of INPUT/OUTPUT configuration you wish to use in this GUI: Default I/O configuration or GUI-specific I/O configuration.\n\nEach option will allow you to select and INPUT file or directory where the files(s) to be used in input are stored and an OUTPUT directory where files produced by the NLP tools will be saved (csv, txt, html, kml, jpg).\n\n   The default configuration is the I/O option used for all GUIs as default;\n   the GUI-specific I/O configuration is an alternative I/O option only used in a specific GUI.\n\nYou can click on the display area and scroll to visualize the current configuration. You can also click on the 'Setup INPUT/OUTPUT configuration' button to get a better view of the available options.\n\nClick on the small buttons to the right of the I/O display area to open the input file, the input directory, the output directory displayed, and the config file where these options are saved. "+msg_IO_config
msg_CoreNLP="Please, select the directory where you downloaded the Stanford CoreNLP software.\n\nYou can download Stanford CoreNLP from https://stanfordnlp.github.io/CoreNLP/download.html\n\nYou can place the Stanford CoreNLP folder anywhere on your machine. But... on some machines CoreNLP will not run unless the folder is inside the NLP folder.\n\nIf you suspect that CoreNLP may have given faulty results for some sentences, you can test those sentences directly on the Stanford CoreNLP website at https://corenlp.run\n\nYOU MUST BE CONNECTED TO THE INTERNET TO RUN CoreNLP."
msg_WordNet="Please, select the directory where you downloaded the WordNet lexicon database.\n\nYou can download WordNet from https://wordnet.princeton.edu/download/current-version."
msg_Mallet="Please, select the directory where you downloaded the MALLET topic modeling software."
msg_CoNLL="Please, select a csv CoNLL table that you would like to analyze.\n\nA CoNLL table is a file generated by the Python script StanfordCoreNLP.py. The CoreNLP script parses a set of text documents using the Stanford CoreNLP parser, providing a dependency tree for each sentence of the documents. In a CoNLL table, each token is labeled with a part-of-speech tag (POSTAG), a Dependency Relation tag (DEPREL), its dependency relation within the corresponding dependency tree, and other useful information." + msg_openFile
msg_corpusData="Please, select the directory where you store your TXT corpus to be analyzed. ALL TXT FILES PRESENT IN THE DIRECTORY WILL BE PARSED. NON TXT FILES WILL BE IGNORED. MOVE ANY TXT FILES YOU DO NOT WISH TO PROCESS TO A DIFFERENT DIRECTORY."  + msg_openExplorer # + msg_dirButtonDisabled
msg_anyData="Please, select the directory where you store the files to be analyzed. ALL FILES OF A SELECTED EXTENSION TYPE (pdf, docx, txt, csv, conll), PRESENT IN THE DIRECTORY WILL BE PROCESSED. ALL OTHER FILE TYPES WILL BE IGNORED."  + msg_openExplorer # + msg_dirButtonDisabled
msg_anyFile="Please, select the file to be analyzed (of any type: pdf, docx, txt, csv, conll)."  + msg_openFile
msg_txtFile="Please, select the TXT file to be analyzed." + msg_openFile # + msg_fileButtonDisabled
msg_csvFile="Please, select the csv file to be analyzed." + msg_openFile # + msg_fileButtonDisabled
msg_csv_txtFile="Please, select either a CSV file or a TXT file to be analyzed." + msg_openFile # + msg_fileButtonDisabled
msg_txt_htmlFile="Please, select either a TXT file or an html file to be analyzed." + msg_openFile # + msg_fileButtonDisabled
msg_outputDirectory="Please, select the directory where the script will save all OUTPUT files of any type (txt, csv, png, html)."  + msg_openExplorer
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
sampleData_libPath = os.path.join(NLPPath,'lib'+os.sep+'sampleData')
sentiment_libPath = os.path.join(NLPPath,'lib'+os.sep+'sentimentLib')
concreteness_libPath = os.path.join(NLPPath,'lib'+os.sep+'concretenessLib')
CoreNLP_enhanced_dependencies_libPath = os.path.join(NLPPath,'lib'+os.sep+'CoreNLP_enhanced_dependencies')
wordLists_libPath = os.path.join(NLPPath,'lib'+os.sep+'wordLists')
namesGender_libPath = os.path.join(NLPPath, 'lib'+os.sep+'namesGender')
GISLocations_libPath = os.path.join(NLPPath,'lib'+os.sep+'GIS')
TIPSPath = os.path.join(NLPPath,'TIPS')
videosPath = os.path.join(NLPPath,'videos')
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
    about_button_x_coordinate = 330 # get_labels_x_coordinate() + 100
    release_history_button_x_coordinate = 510 # get_labels_x_coordinate() + 100
    team_button_x_coordinate = 690 # get_labels_x_coordinate() + 100
    cite_button_x_coordinate = 870 # get_labels_x_coordinate() + 100

    help_button_x_coordinate = 70
    labels_x_coordinate = 150  # start point of all labels in the second column (first column after ? HELP)
    labels_x_indented_coordinate = 160
    select_file_directory_button_width=23
    open_file_directory_button_width = 1
    IO_button_name_width=1
    open_file_directory_coordinate = 400
    entry_box_x_coordinate = 470 #start point of all labels in the third column (second column after ? HELP); where IO filename, dir, etc. are displayed
    read_button_x_coordinate = 70
    watch_videos_x_coordinate = 200
    open_TIPS_x_coordinate = 370
    open_reminders_x_coordinate = 570
    run_button_x_coordinate = 850
    close_button_x_coordinate = 980

    open_IO_config_button = 650
    open_setup_software_button = 650

    open_file_button_brief = 700
    open_inputDir_button_brief = 740
    open_outputDir_button_brief = 780
    open_config_file_button_brief = 820

    # special internal GUI specific values MAC
    # SVO_main
    SVO_2nd_column = 570
    SVO_2nd_column_top = 450
    SVO_3rd_column_top = 850

    # CoNLL_table_analyzer_main
    combobox_position = 210
    combobox_width = 40

else: #windows and anything else
    about_button_x_coordinate = 230 # get_labels_x_coordinate() + 100
    release_history_button_x_coordinate = 400 # get_labels_x_coordinate() + 100
    team_button_x_coordinate = 570 # get_labels_x_coordinate() + 100
    cite_button_x_coordinate = 740 # get_labels_x_coordinate() + 100
    help_button_x_coordinate = 70
    help_button_x_coordinate = 50
    labels_x_coordinate = 120  # start point of all labels in the second column (first column after ? HELP)
    labels_x_indented_coordinate = 140
    select_file_directory_button_width=30
    IO_button_name_width=30
    open_file_directory_button_width = 3
    open_file_directory_coordinate = 350
    entry_box_x_coordinate = 400 #start point of all labels in the third column (second column after ? HELP)
    read_button_x_coordinate = 50
    watch_videos_x_coordinate = 170
    open_TIPS_x_coordinate = 350
    open_reminders_x_coordinate = 550
    run_button_x_coordinate = 840
    close_button_x_coordinate = 960

    open_IO_config_button = 820
    open_setup_software_button = 820

    open_file_button_brief = 760
    open_inputDir_button_brief = 800
    open_outputDir_button_brief = 840
    open_config_file_button_brief = 880

    # special internal GUI specific values WINDOWS
    # SVO_main
    SVO_2nd_column = 520
    SVO_2nd_column_top = 400
    SVO_3rd_column_top = 800

    # CoNLL_table_analyzer_main
    combobox_position = 200
    combobox_width = 50

basic_y_coordinate = 90
y_step = 40 #the line-by-line increment on the GUI

def get_GUI_width(size_type=1):
    if sys.platform == 'darwin':  # Mac OS
        if size_type == 1: # for now we have one basic size
            return 1400
        if size_type == 2:
            return 1400
        if size_type == 3:
            return 1400
        if size_type == 4:
            return 1400
    elif sys.platform == 'win32': # for now we have two basic sizes
        if size_type == 1:
            return 1100
        if size_type == 2:
                return 1200
        elif size_type==3:
            return 1300
        elif size_type==4:
            return 1300

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

def about():
    # check internet connection
    if not IO_internet_util.check_internet_availability_warning("Check on GitHub what the NLP Suite is all about"):
        return
    webbrowser.open_new("https://github.com/NLP-Suite/NLP-Suite/wiki/About")

def release_history():
    # check internet connection
    if not IO_internet_util.check_internet_availability_warning("Check on GitHub the NLP Suite release history"):
        return
    webbrowser.open_new("https://github.com/NLP-Suite/NLP-Suite/wiki/NLP-Suite-Release-History")

# The function displays the contributors to the development of the NLP Suite
def list_team():
    # check internet connection
    if not IO_internet_util.check_internet_availability_warning("Check on GitHub the NLP Suite team"):
        return
    webbrowser.open_new("https://github.com/NLP-Suite/NLP-Suite/wiki/The-NLP-Suite-Team")

def cite_NLP():
    # check internet connection
    if not IO_internet_util.check_internet_availability_warning("Check on GitHub the NLP Suite newest release version"):
        return
    webbrowser.open_new("https://github.com/NLP-Suite/NLP-Suite/wiki/About#How-to-Cite-the-NLP-Suite")

def GUI_settings(IO_setup_display_brief,GUI_width,GUI_height_brief,GUI_height_full,y_multiplier_integer,y_multiplier_integer_add,increment):
    # the GUIs are all setup to run with a brief I/O display or full display (with filename, inputDir, outputDir)
    #   just change the next statement to True or False IO_setup_display_brief=True
    # GUI_height height of GUI with full I/O display

    if IO_setup_display_brief:
        GUI_height = GUI_height_brief # - 40
        y_multiplier_integer = y_multiplier_integer  # IO BRIEF display
        increment = 0  # used in the display of HELP messages
    else:  # full display
        # GUI CHANGES add following lines to every special GUI
        # +3 is the number of lines starting at 1 of IO widgets
        # y_multiplier_integer=GUI_util.y_multiplier_integer+2
        GUI_height = GUI_height_full
        y_multiplier_integer = y_multiplier_integer + y_multiplier_integer_add  # IO FULL display
        increment = increment
    GUI_size = str(GUI_width) + 'x' + str(GUI_height)
    return GUI_size, y_multiplier_integer, increment

#config_filename has no path;
# config_input_output_numeric_options is set to [0 0,0,0] for GUIs that are placeholders for more specialized GUIs
#   in these cases (e.g., narrative_analysis_main, there are no I/O options to save
def exit_window(window,config_filename, scriptName, config_input_output_numeric_options,current_config_input_output_alphabetic_options):
    if not 'NLP_menu_main' in scriptName:
        saved_config_input_output_alphabetic_options, config_input_output_full_options, missingIO=config_util.read_config_file(config_filename, config_input_output_numeric_options)
        if saved_config_input_output_alphabetic_options!=current_config_input_output_alphabetic_options:
            if current_config_input_output_alphabetic_options==['','','',''] or current_config_input_output_alphabetic_options==['', '', '', '']:
                saveGUIconfig = False
            else:
                if saved_config_input_output_alphabetic_options==['','','',''] or saved_config_input_output_alphabetic_options==['', '', '', '']:
                    saveGUIconfig = True
                else:
                    if 'default' in config_filename:
                        saveGUIconfig = mb.askyesno("Save I/O values to 'Default I/O configuration': " + config_filename,
                                                    'The selected Input/Output options are different from the I/O values previously saved in "' + config_filename + '"' + ' listed below in succinct form for readability:\n\n' + str(config_input_output_full_options) + '\n\nDo you want to replace the previously saved I/O values with the current ones?')
                    else:
                        saveGUIconfig = mb.askyesno("Save I/O values to 'GUI-specific I/O configuration': " + config_filename,
                                                        'The selected Input/Output options are different from the I/O values previously saved in "' + config_filename + '"' + ' listed below in succinct form for readability:\n\n' + str(config_input_output_full_options) + '\n\nDo you want to replace the previously saved I/O values with the current ones?')
            if saveGUIconfig == True:
                config_util.write_config_file(window,config_filename, config_input_output_numeric_options, current_config_input_output_alphabetic_options)
    window.destroy()
    sys.exit(0)

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


# creating popup menu in tkinter

def dropdown_menu_widget(window,textCaption, menu_values, default_value, callback):

    class App():
        def __init__(self,master):
            top = self.top = Toplevel()
            top.wm_title(textCaption)
            self.menuButton = ttk.Combobox(top, width=len(textCaption)+30)
            self.menuButton['values'] = menu_values
            self.menuButton.pack()

            self.menuButton.grid(row=0, column=1) # , sticky=W)
            self.callback = callback

            ok_button = tk.Button(self.top, text='OK', command=self.get_value)
            ok_button.grid(row=0, column=1)

        def get_value(self):
            val = self.menuButton.get()
            self.top.destroy()
            callback(val)

    App(window)

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
# return a list; see comment at end of function
def enter_value_widget(masterTitle,textCaption,numberOfWidgets=1,defaultValue='',textCaption2='',defaultValue2=''):
    value1=defaultValue
    value2=defaultValue2

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
    e1.focus_force()

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
