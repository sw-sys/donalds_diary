import PySimpleGUI as sg

# theme - colours for GUI
sg.theme('DarkGray5') # 5 best so far, 2, 6 is ok

### WINDOW CONTENT BEGINS

### TABS FOR VIEWS

# TAB 1 - data submission

# options for status
status_options = ['Seen', 'Not seen', 'Unknown']

tab1_layout = [#[[sg.Text('Record your daily dose of Donald', font=('Arial',20))],
                [sg.CalendarButton('Select Date:', target='date_input', format='%d-%m-%Y'), sg.InputText(key='DATE')],
                [sg.Text('Enter a time (HH:MM:SS):'), sg.Input(key='TIME', enable_events=True)],
                [sg.Text('Status (seen, not seen, unknown):'), sg.Combo(status_options, default_value=status_options[0], key='STATUS')],
                [sg.Text('Location (co-ords):'), sg.Input(key='LOCATION')],
                [sg.Text('Image:'), sg.Input(key='MEDIA'), sg.FileBrowse()],
                [sg.OK('Submit'), sg.Cancel()]]

# TAB 2 content
tab2_layout = [[sg.Text('Overview of when Donald was spotted this month')]]

# TAB 3 content
tab3_layout = [[sg.Text('Map of Donald\'s locations')]]

# TAB 4 content
tab4_layout = [[sg.Text('Photos of Donald')]]

# define layouts for tabs
tab_group_layout = [[sg.Tab('Submit', tab1_layout), sg.Tab('Calendar', tab2_layout), sg.Tab('Map', tab3_layout), sg.Tab('Media', tab4_layout)]]
tab_group = sg.TabGroup(tab_group_layout)

layout = [[[sg.Text('Record and View Donald Sightings', font=('Arial',20))],
           tab_group]]

# window event
window = sg.Window('Donald\'s Diary', layout)

while True:
    event, values=window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == sg.OK():
        time = values['TIME']
        date = values['DATE']
        status = values['STATUS']
        media = values['MEDIA']
        location = values['LOCATION']
window.close()