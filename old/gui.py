from tkinter import Button, E, END, Label, \
    OptionMenu, StringVar, Text, \
    Toplevel, W, filedialog, mainloop, messagebox

from activity_tracker import *


root.title('Activity Tracker [Inactive]')
root.maxsize(width=400, height=170)
root.minsize(width=400, height=170)

# Textbox config (child window)
textbox = Toplevel(root)
textbox.title('Grouped Data Output')

filename_read = ''
filename_write = ''


def for_start_button():
    # Removes start button, adds write-file prompt button.
    global filename_read
    start_button.grid_forget()
    filename_write_popup.grid(row=0, column=0, columnspan=1, sticky=W + E)


def for_stop_button():
    # Stops logging if active.
    root.title('Stopping Logging')
    filename_write_popup.grid_forget()
    start_button.grid(row=0, column=0)
    root.after(1000, lambda: root.title('Activity Tracker [Inactive]'))


def for_filename_write_popup():
    # Opens file prompt for writing.
    global filename_write
    filename_write = filedialog.askopenfilename(initialdir=getcwd())
    if filename_write:
        root.title('Activity Tracker [Active]')
        filename_write_popup.grid_forget()
        start_button.grid(row=0, column=0)
        start_button.config(text='Running...')
        log_to(output_db=get_activity(), file=filename_write)
        start_button.config(text='Start Logging')


def for_read_button():
    # Removes read button, adds read-file prompt button.
    global filename_read
    read_button.grid_forget()
    filename_read_popup.grid(row=1, column=0, columnspan=2, sticky=W + E)


def for_filename_read_popup():
    # Opens file prompt for reading.
    global filename_read
    filename_read = filedialog.askopenfilename(initialdir=getcwd())
    if filename_read:
        filename_read_popup.grid_forget()
        read_options.grid(row=1, column=0, columnspan=1, sticky=W + E)
        finalize_option.grid(row=1, column=1, columnspan=1, sticky=W + E)
        reset_read_button.grid(row=2, column=0, columnspan=2, sticky=W + E)


def for_finalize_option():
    # Gets user choice from drop-down menu, returns processed output.
    global filename_read
    label_output = '''
    -------------------------
    Full logs in other window
    -------------------------\n
    '''
    textbox_output = ''
    initial_label_len = len(label_output)
    grouped_data = group(file=filename_read)
    option = selected_option.get()
    if option == 'By Process':
        for i, j in grouped_data[0].items():
            label_output += f'{i}: {j}\n'
        textbox_output = label_output[initial_label_len:]
        final_data_label.config(text=label_output)
    elif option == 'By Window Name':
        for i, j in grouped_data[1].items():
            textbox_output += f'{i}: {j}\n'
            if len(i) >= 42:
                label_output += f'{"".join((i[:18], "...", i[-18:]))}: {j}\n'
            else:
                label_output += f'{i}: {j}\n'
        final_data_label.config(text=label_output)
    root.maxsize(width=400, height=450)
    root.minsize(width=400, height=450)
    for_textbox(textbox_output=textbox_output)
    final_data_label.grid(row=3, column=0, columnspan=2, sticky=W + E)


def for_reset_read_button():
    # Makes reset button to change read file.
    global textbox, final_data_textbox
    read_options.grid_forget()
    finalize_option.grid_forget()
    reset_read_button.grid_forget()
    final_data_label.config(text='')
    try:
        final_data_textbox.delete(1.0, END)
    except TclError:
        textbox = Toplevel(root)
        textbox.title('Grouped Data Output')
        final_data_textbox = Text(textbox, width=120)
        final_data_textbox.pack()
    root.maxsize(width=400, height=170)
    root.minsize(width=400, height=170)
    read_button.grid(row=1, column=0, columnspan=2, sticky=W + E)


def for_textbox(textbox_output):
    # Inserts processed data to textbox (child window).
    global textbox, final_data_textbox
    try:
        final_data_textbox.delete(1.0, END)
        final_data_textbox.insert(1.0, textbox_output)
        final_data_textbox.pack()
    except TclError:
        textbox = Toplevel(root)
        textbox.title('Grouped Data Output')
        final_data_textbox = Text(textbox, width=120)
        final_data_textbox.insert(1.0, textbox_output)
        final_data_textbox.pack()


# Start Logging Button
start_button = Button(text='Start Logging', command=for_start_button, height=5, width=28)
start_button.grid(row=0, column=0)

# Stop Logging Button
stop_button = Button(text='Stop Logging', command=for_stop_button, height=5, width=28)
stop_button.grid(row=0, column=1)

# Read Logs Button
read_button = Button(text='Read Logs', command=for_read_button, height=5, width=57)
read_button.grid(row=1, column=0, columnspan=2, sticky=W + E)

# Read Logs Options
selected_option = StringVar(root)
read_options = OptionMenu(root, selected_option, 'By Process', 'By Window Name')
read_options.config(height=2)
finalize_option = Button(text='Go', command=for_finalize_option, height=2)
reset_read_button = Button(text='Reset', command=for_reset_read_button, height=2)

# Get Filename
filename_read_popup = Button(text='Select File', command=for_filename_read_popup, height=5, width=28)
filename_write_popup = Button(text='Select File', command=for_filename_write_popup, height=5, width=28)

# Read Logs Output
final_data_label = Label(text='')
final_data_textbox = Text(textbox, width=120)
final_data_textbox.pack()

mainloop()
