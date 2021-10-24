# Written by Yuhang Feng November 2019# Edited by Roberto Franzosi import sysimport GUI_utilimport IO_libraries_utilif IO_libraries_util.install_all_packages(GUI_util.window,"Excel_charts.py",['os','tkinter'])==False:    sys.exit(0)import tkinter.messagebox as mbimport tkinter as tkimport GUI_utilimport GUI_IO_utilimport IO_files_utilimport IO_user_interface_utilimport Excel_utilimport IO_csv_util# RUN section ______________________________________________________________________________________________________________________________________________________def run(input_file_name,output_dir,openOutputFiles,selected_series,column_xAxis_label_var,column_yAxis_label_var,count_var,column_yAxis_field_list,second_y_var,second_y_var_list,second_yAxis_label_var,chart_type,chart_type_list,chart_title,hover_var_list,hover_info_column_list):    filesToOpen = []  # Store all files that are to be opened once finished    if len(chart_type)==0:        mb.showwarning(title='Chart type error', message="No chart type was specified (e.g., line, bubble). The chart cannot be created. Please, select a chart type and try again!")        return True    if hover_var_list and all(check == 1 for check in hover_var_list):        if second_y_var_list and all(var == 0 for var in second_y_var_list):            hover_var = 1            output_file_name=IO_files_util.generate_output_file_name(input_file_name, output_dir, '.xlsm', 'EC', 'chart')        else:            mb.showwarning(title='Hover var and Second Y-axis var error', message="Hovering feature is not available for chart with two Y-axes. The system indicates that you tick both the hover and the second Y-axis check boxes.\n\nPlease, check your input and try again!")            return True    elif hover_var_list and all(check == 0 for check in hover_var_list):        hover_var = 0        output_file_name=IO_files_util.generate_output_file_name(input_file_name, output_dir, '.xlsx', 'EC', 'chart')    else:        mb.showwarning(title='Hover var error', message="Hover feature applies to all the groups when multiple groups of data are selected. The system indicates that at least one of the groups seleted did not tick the hover checkbox.\n\nPlease, check your input and try again!")        return True    num_of_series = len(selected_series)    # # The 2 functions get_data_to_be_plotted check for data with/without headers    if count_var==1: # counting y axiss        if hover_var_list and all(check == 0 for check in hover_var_list):            data_to_be_plotted = Excel_util.prepare_data_to_be_plotted(input_file_name, selected_series, chart_type, 1, column_yAxis_field_list)        else:            mb.showwarning(title='Hover var and Count var error', message="Hovering feature is not available for chart with counting feature. The system indicates that you tick both the hover and the count check boxes.\n\nPlease, check your input and try again!")            return True    else: # NOT counting y axis        data_to_be_plotted = Excel_util.prepare_data_to_be_plotted(input_file_name, selected_series, chart_type, 0)    errorFound=IO_csv_util.list_to_csv(GUI_util.window,data_to_be_plotted,output_file_name)    if errorFound==True:        return    reverse_column_postion_for_series_label = False    series_label_list = []    for i in range(len(selected_series)):        series_label_list.append("")    print("series_label_list",series_label_list)    if Excel_util.create_excel_chart(GUI_util.window,data_to_be_plotted,output_file_name,chart_title,chart_type_list,column_xAxis_label_var,column_yAxis_label_var,hover_info_column_list, reverse_column_postion_for_series_label,series_label_list,second_y_var,second_yAxis_label_var) == True:        return    filesToOpen.append(output_file_name)    IO_user_interface_util.timed_alert(GUI_util.window, 3000, 'Analysis end', 'Finished running Excel charts at', True)    if openOutputFiles == 1:        IO_files_util.OpenOutputFiles(GUI_util.window, openOutputFiles, filesToOpen)#the values of the GUI widgets MUST be entered in the command otherwise they will not be updated# run_script_command=lambda: run(GUI_util.inputFilename.get(),GUI_util.output_dir_path.get(),GUI_util.open_csv_output_checkbox.get(),selected_series,column_xAxis_label_var.get(),column_yAxis_label_var.get(),count_var.get(),column_yAxis_field_list,second_yAxis_var.get(),second_yAxis_label_var.get(),chart_type.get(),chart_type_list,chart_title_var.get())run_script_command=lambda: run(GUI_util.inputFilename.get(),                               GUI_util.output_dir_path.get(),                               GUI_util.open_csv_output_checkbox.get(),                               selected_series,                               column_xAxis_label_var.get(),                               column_yAxis_label_var.get(),                               count_var.get(),                               column_yAxis_field_list,                               second_yAxis_var.get(),                               second_yAxis_var_list,                               second_yAxis_label_var.get(),                               chart_type.get(),                               chart_type_list,                               chart_title_var.get(),                               hover_var_list,                               column_hover_list)GUI_util.run_button.configure(command=run_script_command)# GUI section ______________________________________________________________________________________________________________________________________________________# the GUIs are all setup to run with a brief I/O display or full display (with filename, inputDir, outputDir)#   just change the next statement to True or False IO_setup_display_brief=TrueIO_setup_display_brief = TrueGUI_width=1200GUI_height = 600  # height of GUI with full I/O displayif IO_setup_display_brief:    GUI_height = GUI_height - 40    y_multiplier_integer = GUI_util.y_multiplier_integer  # IO BRIEF display    increment = 0  # used in the display of HELP messageselse:  # full display    # GUI CHANGES add following lines to every special GUI    # +3 is the number of lines starting at 1 of IO widgets    # y_multiplier_integer=GUI_util.y_multiplier_integer+2    y_multiplier_integer = GUI_util.y_multiplier_integer + 1  # IO FULL display    increment = 1GUI_size = str(GUI_width) + 'x' + str(GUI_height)GUI_label='Graphical User Interface (GUI) for Excel Charts'config_filename='Excel-config.txt'# The 6 values of config_option refer to: #   software directory#   input file        # 1 for CoNLL file         # 2 for TXT file         # 3 for csv file         # 4 for any type of file        # 5 for txt or html        # 6 for txt or csv#   input dir#   input secondary dir#   output file#   output dirconfig_option=[0,3,0,0,0,1]GUI_util.set_window(GUI_size, GUI_label, config_filename, config_option)window = GUI_util.windowconfig_input_output_options = GUI_util.config_input_output_optionsconfig_filename = GUI_util.config_filenameinputFilename = GUI_util.inputFilenameGUI_util.GUI_top(config_input_output_options, config_filename,IO_setup_display_brief)# GUI CHANGES cut/paste special GUI widgets from GUI_util # Yuhangcolumn_hover_list = []column_yAxis_label_list = []hover_var_list = []second_yAxis_var_list = []column_hover = tk.StringVar()hover_var = tk.IntVar()column_yAxis_lb = tk.Label()column_yAxis_field = tk.StringVar()count_var = tk.IntVar()second_yAxis_var = tk.IntVar()chart_type = tk.StringVar()chart_title_var = tk.StringVar()selected_series = []  # used by Excel_chartscolumn_yAxis_field_list = []  # used by Excel_chartschart_type_list = []  # used by Excel_chartsseries_number_var = tk.IntVar()column_xAxis = tk.StringVar()column_yAxis = tk.StringVar()# labels displayed on the chart instead of default X-Axis and Y-Axiscolumn_xAxis_label_var = tk.StringVar()column_yAxis_label_var = tk.StringVar()second_yAxis_label_var = tk.StringVar()series_number_var.set(1)series_lb = tk.Label(window, text='Series ')y_multiplier_integer = GUI_IO_util.placeWidget(GUI_IO_util.get_labels_x_coordinate(), y_multiplier_integer, series_lb,                                               True)series_number = tk.Entry(window, width=3, textvariable=series_number_var)y_multiplier_integer = GUI_IO_util.placeWidget(GUI_IO_util.get_labels_x_coordinate() + 50, y_multiplier_integer,                                               series_number, True)add_series_button = tk.Button(window, text='+', width=2, height=1, state='disabled', command=lambda: add_series())# IO_util.exit_window(window,config_filename,setup_IO_configArray(window,input_output_options)))y_multiplier_integer = GUI_IO_util.placeWidget(GUI_IO_util.get_labels_x_coordinate() + 100, y_multiplier_integer,                                               add_series_button, True)reset_series_button = tk.Button(window, text='Reset', width=5, height=1, state='normal',                                command=lambda: reset_all_values())y_multiplier_integer = GUI_IO_util.placeWidget(GUI_IO_util.get_labels_x_coordinate() + 130, y_multiplier_integer,                                               reset_series_button)column_xAxis_lb = tk.Label(window, text='Select X-Axis Column ')y_multiplier_integer = GUI_IO_util.placeWidget(GUI_IO_util.get_labels_x_indented_coordinate(), y_multiplier_integer,                                               column_xAxis_lb, True)if inputFilename.get() != '':    numColumns = IO_csv_util.get_csvfile_numberofColumns(inputFilename.get())else:    numColumns = 0if numColumns == -1:    passif inputFilename.get() != '':    if IO_csv_util.csvFile_has_header(inputFilename.get()) == False:        menu_values = range(1, numColumns + 1)    # column_xAxis.set(1)    # column_yAxis.set(1)    else:        data, headers = IO_csv_util.get_csv_data(inputFilename.get(), True)        menu_values = headers    # column_xAxis.set(menu_values[0])    # column_yAxis.set(menu_values[0])    # print("	menu_values",menu_values)    column_xAxis_menu = tk.OptionMenu(window, column_xAxis, *menu_values)else:    menu_values = " "    column_xAxis_menu = tk.OptionMenu(window, column_xAxis, *menu_values)y_multiplier_integer = GUI_IO_util.placeWidget(GUI_IO_util.get_entry_box_x_coordinate(), y_multiplier_integer,                                               column_xAxis_menu, True)column_xAxis_label = tk.Label(window, text='Enter X-Axis label ')y_multiplier_integer = GUI_IO_util.placeWidget(GUI_IO_util.get_entry_box_x_coordinate() + 150, y_multiplier_integer,                                               column_xAxis_label, True)column_xAxis_label_entry = tk.Entry(window, width=25, state='disabled', textvariable=column_xAxis_label_var)y_multiplier_integer = GUI_IO_util.placeWidget(GUI_IO_util.get_entry_box_x_coordinate() + 300, y_multiplier_integer,                                               column_xAxis_label_entry)# need to save the value because it will be updated several times after the check_columns functiony_multiplier_integer_save = y_multiplier_integer - 1# y-axis value from doropdown menucolumn_yAxis_lb = tk.Label(window, text='Select Y-Axis Column ')y_multiplier_integer = GUI_IO_util.placeWidget(GUI_IO_util.get_labels_x_indented_coordinate(), y_multiplier_integer,                                               column_yAxis_lb, True)column_yAxis_menu = tk.OptionMenu(window, column_yAxis, *menu_values)column_yAxis_menu.config(state="disabled")y_multiplier_integer = GUI_IO_util.placeWidget(GUI_IO_util.get_entry_box_x_coordinate(), y_multiplier_integer,                                               column_yAxis_menu, True)# y-axis label (e.g., Frequency)column_yAxis_label = tk.Label(window, text='Enter Y-Axis label')y_multiplier_integer = GUI_IO_util.placeWidget(GUI_IO_util.get_entry_box_x_coordinate() + 150, y_multiplier_integer,                                               column_yAxis_label, True)column_yAxis_label_entry = tk.Entry(window, width=25, state='disabled', textvariable=column_yAxis_label_var)y_multiplier_integer = GUI_IO_util.placeWidget(GUI_IO_util.get_entry_box_x_coordinate() + 300, y_multiplier_integer,                                               column_yAxis_label_entry)# Hoverhover_checkbox = tk.Checkbutton(window, text='Display hover over data', state='disabled', variable=hover_var, onvalue=1,                                offvalue=0)y_multiplier_integer = GUI_IO_util.placeWidget(GUI_IO_util.get_labels_x_indented_coordinate() + 20,                                               y_multiplier_integer, hover_checkbox, True)# TODO ROBERTO: update the menu when input file is changed# hover info from doropdown menucolumn_hover_lb = tk.Label(window, text='Select column containing hover over data')y_multiplier_integer = GUI_IO_util.placeWidget(GUI_IO_util.get_entry_box_x_coordinate(), y_multiplier_integer,                                               column_hover_lb, True)column_hover_menu = tk.OptionMenu(window, column_hover, *menu_values)column_hover_menu.config(state="disabled")y_multiplier_integer = GUI_IO_util.placeWidget(GUI_IO_util.get_entry_box_x_coordinate() + 300, y_multiplier_integer,                                               column_hover_menu)count_checkbox = tk.Checkbutton(window, text='Count the Y-Axis values ', state='disabled', variable=count_var,                                onvalue=1, offvalue=0)y_multiplier_integer = GUI_IO_util.placeWidget(GUI_IO_util.get_labels_x_indented_coordinate() + 20,                                               y_multiplier_integer, count_checkbox, True)# field where you enter a specific value to be countedcolumn_yAxis_field_lb = tk.Label(window, text='Enter Y-Axis column specific value ')y_multiplier_integer = GUI_IO_util.placeWidget(GUI_IO_util.get_entry_box_x_coordinate(), y_multiplier_integer,                                               column_yAxis_field_lb, True)column_yAxis_field_entry = tk.Entry(window, width=25, state='disabled', textvariable=column_yAxis_field)y_multiplier_integer = GUI_IO_util.placeWidget(GUI_IO_util.get_entry_box_x_coordinate() + 300, y_multiplier_integer,                                               column_yAxis_field_entry)second_yAxis_var.set(0)second_yAxis_var_checkbox = tk.Checkbutton(window, text='Plot chart with 2 Y-Axes ', state='disabled',                                           variable=second_yAxis_var, onvalue=1, offvalue=0)y_multiplier_integer = GUI_IO_util.placeWidget(GUI_IO_util.get_labels_x_indented_coordinate(), y_multiplier_integer,                                               second_yAxis_var_checkbox, True)# y-axis label (e.g., Population growth)second_yAxis_label = tk.Label(window, text='Enter second Y-Axis label ')y_multiplier_integer = GUI_IO_util.placeWidget(GUI_IO_util.get_entry_box_x_coordinate(), y_multiplier_integer,                                               second_yAxis_label, True)second_yAxis_label_entry = tk.Entry(window, width=25, state='disabled', textvariable=second_yAxis_label_var)y_multiplier_integer = GUI_IO_util.placeWidget(GUI_IO_util.get_entry_box_x_coordinate() + 300, y_multiplier_integer,                                               second_yAxis_label_entry)def activate_second_yAxis_label_entry(*args):    if second_yAxis_var.get() == 1:        second_yAxis_label_entry.config(state='normal')    else:        second_yAxis_label_entry.config(state='disabled')second_yAxis_var.trace('w', activate_second_yAxis_label_entry)chart_type_lb = tk.Label(window, text='Select Excel chart type ')y_multiplier_integer = GUI_IO_util.placeWidget(GUI_IO_util.get_labels_x_coordinate(), y_multiplier_integer,                                               chart_type_lb, True)chart_type_menu = tk.OptionMenu(window, chart_type, 'bar', 'bubble', 'line', 'pie', 'radar', 'scatter')chart_type_menu.config(state='disabled')y_multiplier_integer = GUI_IO_util.placeWidget(GUI_IO_util.get_entry_box_x_coordinate(), y_multiplier_integer,                                               chart_type_menu, False)# add_chart_type_button = tk.Button(window, text='+', width=2,height=1,state='disabled',command=lambda: add_chart_type())# y_multiplier_integer=GUI_IO_util.placeWidget(GUI_IO_util.get_labels_x_coordinate()++150,y_multiplier_integer,add_chart_type_button, True)# reset_chart_type_button = tk.Button(window, text='Reset', width=5,height=1,state='disabled',command=lambda: reset_chart_type_values())# y_multiplier_integer=GUI_IO_util.placeWidget(GUI_IO_util.get_labels_x_coordinate()++180,y_multiplier_integer,reset_chart_type_button)def add_series_to_list():    x = column_xAxis.get()    y = column_yAxis.get()    if len(selected_series) < int(series_number_var.get()):        # selected_series.append((x, y))        selected_series.append([x, y])    else:        selected_series.clear()        # selected_series.append((x, y))        selected_series.append([x, y])# chart_title_entry.config(state='disabled')def activate_count_checkbox_chart_type_options(*args):    column_yAxis_field_entry.config(state="disabled")    if column_yAxis.get() in selected_series:        mb.showwarning(title='Warning',                       message='The Y-axis series ' + column_yAxis.get() + ' is already in the series list: ' + str(                           selected_series) + '.\n\nPlease, select another Y-axis series and try again.')        return    else:        if len(column_yAxis.get()) > 0:            add_series_to_list()  # do not process series if the filename was just changed and the new yAxis value was not yet selected            if len(selected_series) <= 1:                column_xAxis_label_entry.config(state='normal')                column_xAxis_label_var.set('')        else:            column_xAxis_label_entry.config(state='disabled')    if len(column_xAxis.get()) > 0 and len(column_yAxis.get()) > 0:        hover_var.set(0)        count_var.set(0)        if len(selected_series) > 1:            column_yAxis_label_entry.config(state='disabled')            column_yAxis_label_var.set(column_yAxis_label_var.get())        else:            column_yAxis_label_entry.config(state='normal')            column_yAxis_label_var.set('Frequency')        hover_checkbox.config(state='normal')        count_checkbox.config(state='normal')        chart_type_menu.config(state='normal')        second_yAxis_var.set(0)        second_yAxis_var_checkbox.config(state='normal')    else:        hover_var.set(0)        count_var.set(0)        column_yAxis_label_var.set(column_yAxis_label_var.get())        # column_yAxis_label_var.set('Frequency')        column_yAxis_label_entry.config(state='disabled')        hover_checkbox.config(state='disabled')        count_checkbox.config(state='disabled')        chart_type_menu.config(state='disabled')        second_yAxis_var.set(0)        second_yAxis_var_checkbox.config(state='disabled')    if column_xAxis.get() == column_yAxis.get():        count_var.set(1)  # when the same column is selected you must count        count_checkbox.config(state='disabled')column_yAxis.trace('w', activate_count_checkbox_chart_type_options)def activate_hover_menu(*args):    if hover_var.get() == 1:        column_hover_menu.config(state="normal")    else:        column_hover_menu.config(state="disabled")hover_var.trace('w', activate_hover_menu)def add_hover_column(*args):    if len(column_hover_list) >= int(series_number_var.get()):        del column_hover_list[-1]  # delete the last selected if there is a new currently selected chart     # if len(column_hover.get()) > 0:    column_hover_list.append(column_hover.get())column_hover.trace('w', add_hover_column)def update_hover_var_list(*args):    if len(hover_var_list) >= int(series_number_var.get()):        del hover_var_list[-1]  # delete the last selected if there is a new currently selected chart     # if len(column_hover.get()) > 0:    hover_var_list.append(hover_var.get())# print("hover_var_list",hover_var_list)hover_var.trace('w', update_hover_var_list)def update_second_yAxis_var_list(*args):    if len(second_yAxis_var_list) >= int(series_number_var.get()):        del second_yAxis_var_list[-1]  # delete the last selected if there is a new currently selected chart     # if len(column_hover.get()) > 0:    second_yAxis_var_list.append(second_yAxis_var.get())# print("second_yAxis_var_list",second_yAxis_var_list)second_yAxis_var.trace('w', update_second_yAxis_var_list)# when counting, the x_Axis label will change to the frequency of y_Axis values as set up in stat_visuals.compute_column_frequenciesdef resetXaxisLabel(*args):    if count_var.get() == 1:        # we are counting the y-Axis values        if column_xAxis.get().isnumeric():            column_xAxis_label_var.set('column_' + column_yAxis.get() + ' values')        else:            column_xAxis_label_var.set(column_yAxis.get() + ' values')        column_yAxis_field_entry.config(state='normal')    else:        if int(series_number.get()) == 1:            if column_xAxis.get().isnumeric():                column_xAxis_label_var.set('')            else:                column_xAxis_label_var.set(column_xAxis.get())        else:            column_xAxis_label_var.set(column_xAxis_label_var.get())        column_yAxis_field_entry.config(state='disabled')count_var.trace('w', resetXaxisLabel)def column_yAxis_field_entry_list(*args):    column_yAxis_field_list[series_number_var.get() - 1:] = []    column_yAxis_field_list.append(column_yAxis_field.get())column_yAxis_field.trace('w', column_yAxis_field_entry_list)def add_series():    if (series_number_var.get() > len(selected_series)) or (series_number_var.get() > len(chart_type_list)):        mb.showwarning(title='Warning',                       message='You cannot add a new Y-axis series until you have selected all required information for the current series (i.e., X-Axis, Y-axis, Chart type).\n\nPlease, check and enter all the required information and try again.')        return    numColumns = IO_csv_util.get_csvfile_numberofColumns(inputFilename.get())    numColumns += 1    series_number_var.set(series_number_var.get() + 1)    if int(series_number_var.get()) > 1:        column_xAxis_menu.config(state='disabled')        column_xAxis_label_entry.config(state='disabled')    else:        column_xAxis_menu.config(state='normal')        if len(column_yAxis.get()) > 0:            column_xAxis_label_entry.config(state='normal')        else:            column_xAxis_label_entry.config(state='disabled')    column_yAxis_menu.config(state='normal')    column_yAxis_label_entry.config(state='disabled')    column_yAxis_label_var.set(column_yAxis_label_var.get())    hover_checkbox.config(state='disabled')    column_hover_menu.config(state='disabled')    count_checkbox.config(state='disabled')    count_var.set(0)    column_yAxis_field.set("")    column_yAxis_field_entry.config(state="disabled")    second_yAxis_var.set(0)    second_yAxis_var_checkbox.config(state='disabled')    chart_type_menu.config(state='disabled')    chart_title_entry.config(state='disabled')    column_yAxis.set('')    column_hover.set('')    hover_var.set(0)    chart_type.set('')def reset_all_values():    numColumns = IO_csv_util.get_csvfile_numberofColumns(inputFilename.get())    selected_series.clear()    chart_type_list.clear()    series_number_var.set(1)    column_xAxis_menu.config(state='normal')    column_xAxis_label_entry.config(state='disabled')    column_xAxis_label_var.set('')    column_yAxis_menu.config(state='disabled')    column_yAxis_label_entry.config(state='disabled')    column_yAxis_label_var.set('')    hover_checkbox.config(state='disabled')    column_hover_menu.config(state='disabled')    column_hover_list.clear()    count_checkbox.config(state='disabled')    column_yAxis_field_entry.config(state='disabled')    chart_type_menu.config(state='disabled')    chart_title_entry.config(state='disabled')    column_xAxis.set('')    column_yAxis.set('')    second_yAxis_var.set(0)    second_yAxis_label_entry.config(state='disabled')    column_hover.set('')    chart_type.set('')    chart_title_var.set('')    column_xAxis_label_var.set('')    column_yAxis_label_var.set('')    hover_var.set(0)    hover_var_list.clear()    count_var.set(0)    column_yAxis_field.set("")    second_yAxis_var.set(0)    second_yAxis_var_checkbox.config(state='disabled')# column_yAxis_field_entry.set('')def activate_series_options(*args):    if len(chart_type.get()) > 0:        add_series_button.config(state='normal')        reset_series_button.config(state='normal')        if len(chart_type_list) >= int(series_number_var.get()):            del chart_type_list[-1]  # delete the last selected chart type if there is a new currently selected chart         chart_type_list.append(chart_type.get())        if series_number_var.get() > 1:            chart_title_entry.config(state='disabled')        else:            chart_title_entry.config(state='normal')    else:        # disable the add and reset series button until a chart_type has been selected         add_series_button.config(state='disabled')        # reset_series_button.config(state='disabled')		         chart_title_entry.config(state='disabled')chart_type.trace('w', activate_series_options)def activate_yAxis(*args):    # chart_type_menu.config(state='disabled')    if len(column_xAxis.get()) > 0:        if column_xAxis.get().isnumeric():            column_xAxis_label_var.set('')        else:            column_xAxis_label_var.set(column_xAxis.get())        column_yAxis_menu.config(state='normal')    else:        column_yAxis_menu.config(state='disabled')    if len(column_yAxis.get()) > 0:        column_xAxis_label_entry.config(state='normal')        column_xAxis_label_var.set('')    else:        column_xAxis_label_entry.config(state='disabled')column_xAxis.trace('w', activate_yAxis)chart_title_lb = tk.Label(window, text='Enter the chart title to be displayed ')y_multiplier_integer = GUI_IO_util.placeWidget(GUI_IO_util.get_labels_x_coordinate(), y_multiplier_integer,                                               chart_title_lb, True)chart_title_entry = tk.Entry(window, width=25, state='disabled', textvariable=chart_title_var)y_multiplier_integer = GUI_IO_util.placeWidget(GUI_IO_util.get_entry_box_x_coordinate(), y_multiplier_integer,                                               chart_title_entry)def changed_Excel_filename(*args):    reset_all_values()    numColumns = IO_csv_util.get_csvfile_numberofColumns(inputFilename.get())    if numColumns == 0:        return    series_number_var.set(1)    if inputFilename.get() != '':        if IO_csv_util.csvFile_has_header(inputFilename.get()) == False:            menu_values = range(1, numColumns + 1)        else:            data, headers = IO_csv_util.get_csv_data(inputFilename.get(), True)            menu_values = headers    else:        menu_values.clear()    m = column_xAxis_menu["menu"]    m.delete(0, "end")    for s in menu_values:        m.add_command(label=s, command=lambda value=s: column_xAxis.set(value))    m = column_yAxis_menu["menu"]    m.delete(0, "end")    for s in menu_values:        m.add_command(label=s, command=lambda value=s: column_yAxis.set(value))    m = column_hover_menu["menu"]    m.delete(0, "end")    for s in menu_values:        m.add_command(label=s, command=lambda value=s: column_hover.set(value))    if int(series_number_var.get()) > 1:        column_xAxis_menu.configure(state="disabled")        column_yAxis_menu.configure(state="normal")    else:        column_xAxis_menu.configure(state="normal")        column_yAxis_menu.configure(state="disabled")    count_var.set(0)    series_number.config(state='normal')    add_series_button.config(state='normal')    reset_series_button.config(state='normal')inputFilename.trace('w', changed_Excel_filename)TIPS_lookup = {'Excel charts': 'TIPS_NLP_Excel Charts.pdf'}TIPS_options = 'Excel charts'# add all the lines lines to the end to every special GUI# change the last item (message displayed) of each line of the function help_buttons# any special message (e.g., msg_anyFile stored in GUI_IO_util) will have to be prefixed by GUI_IO_util. def help_buttons(window, help_button_x_coordinate, basic_y_coordinate, y_step):    if not IO_setup_display_brief:        GUI_IO_util.place_help_button(window, help_button_x_coordinate, basic_y_coordinate, "Help", GUI_IO_util.msg_csvFile)        GUI_IO_util.place_help_button(window, help_button_x_coordinate, basic_y_coordinate + y_step, "Help",                                      GUI_IO_util.msg_outputDirectory)    else:        GUI_IO_util.place_help_button(window, help_button_x_coordinate, basic_y_coordinate, "Help",                                      GUI_IO_util.msg_IO_setup)    GUI_IO_util.place_help_button(window, help_button_x_coordinate, basic_y_coordinate + y_step * (increment+1), "Help",                                  "Please, click on the + button if you wish to add another Y-axis series to your chart, after having entered all relevant information for the current series.\n\nClick on the Reset button to reset all values to initial default settings.")    GUI_IO_util.place_help_button(window, help_button_x_coordinate, basic_y_coordinate + y_step * (increment+2), "Help",                                  "Please, using the dropdown menu, select the column to be used as the X-Axis values of the chart. The option is disabled when multiple Y-series are selected.\n\nAfter selecting the column, the 'Enter X-Axis label' field will become available and you can enter the label that will be displayed on the chart. The default value is the column header for csv files with headers.")    GUI_IO_util.place_help_button(window, help_button_x_coordinate, basic_y_coordinate + y_step * (increment+3), "Help",                                  "Please, using the dropdown menu, select the column to be used as the Y-Axis values of the chart.\n\nThe selected column for the Y-axis can be the same column as the X-Axis column. In this case, you MUST have the Count option ON, to basically provide a chart of the frequency distribution of the selected column values.\n\nAfter selecting the column, the 'Enter Y-Axis label' field will become available and you can enter the label that will be displayed on the chart. The default value is 'Frequency'.")    GUI_IO_util.place_help_button(window, help_button_x_coordinate, basic_y_coordinate + y_step * (increment+4), "Help",                                  "Please, tick the 'Hover over info worksheet' checkbox if you want to display information contained in a specific column when hovering over data points on the chart. The checkbox is not available until a column has been selected as the Y-axis.\n\nIf the 'Display hover over data' has been ticked off, the 'Select column containing hover over data' menu becomes available. Please, select a specific column whose values will be displayed when hovering over specific data points on the chart.")    GUI_IO_util.place_help_button(window, help_button_x_coordinate, basic_y_coordinate + y_step * (increment+5), "Help",                                  "Please, tick the 'Count the Y-axis values' checkbox if you want to count the Y-Axis column values in case the values are NOT in numeric format. The checkbox is not available until a column has been selected as the Y-axis.\n\nIf the 'Count the Y-axis values' has been ticked off, the text field 'Enter Y-axis Column specific value' becomes available. Please, enter there a specific value from the Y-Axis column if you want to restrict the frequency counts to a specific value.")    GUI_IO_util.place_help_button(window, help_button_x_coordinate, basic_y_coordinate + y_step * (increment+6), "Help",                                  "Please, tick the 'Plot chart with 2 y-axes' checkbox if you want to plot the selected Y-Axis with a different set of scale values. the Python library openpyxl allows to have a maximum of 2 different y-axes.\n\nIf you select to have 2 sets of Y-Axes, you will also be able to enter a label for the second Y-Axis.")    GUI_IO_util.place_help_button(window, help_button_x_coordinate, basic_y_coordinate + y_step * (increment+7), "Help",                                  "Please, using the dropdown menu, select the type of Excel chart to be used.\n\nMultiple (compatible) chart types can be entered. Press + to add a new chart type when the option is available. Press the Reset button to clear selection and select new chart types.")    GUI_IO_util.place_help_button(window, help_button_x_coordinate, basic_y_coordinate + y_step * (increment+8), "Help",                                  "Please, enter the title that will be displayed in the chart.")    GUI_IO_util.place_help_button(window, help_button_x_coordinate, basic_y_coordinate + y_step * (increment+9), "Help",                                  GUI_IO_util.msg_openOutputFiles)help_buttons(window, GUI_IO_util.get_help_button_x_coordinate(), GUI_IO_util.get_basic_y_coordinate(),             GUI_IO_util.get_y_step())# change the value of the readMe_messagereadMe_message = "This Python 3 script allows a user to visualize data in Excel charts (bar/column, line, pie, scatter, radar, ...) from a selected csv file.\n\nGUI widgets are disabled (i.e., greyed out) when not currently available."readMe_command = lambda: GUI_IO_util.readme_button(window, GUI_IO_util.get_help_button_x_coordinate(),                                                   GUI_IO_util.get_basic_y_coordinate(), "Help", readMe_message)GUI_util.GUI_bottom(config_filename, config_input_output_options, y_multiplier_integer, readMe_command, TIPS_lookup, TIPS_options, IO_setup_display_brief)GUI_util.window.mainloop()