import PySimpleGUI as sg

# Design
sg.theme('DarkGray6')
sg.set_options(font=('Arial 12'), text_color='white')

### WINDOW CONTENT BEGINS

### TABS FOR VIEWS

# TAB 1 - data submission

# options for status
status_options = ['Seen', 'Not seen', 'Unknown']

tab1_layout = [
                [sg.Text(' ')],
                [sg.Text('Status:'), sg.Push(), sg.Combo(status_options, default_value=status_options[0], key='STATUS'), sg.Push(), sg.Push(), sg.Push()],
                [sg.Text('Enter Date: DD-MM-YYYY'),sg.Input(key='DATE'), sg.Push(), sg.CalendarButton('Select', target='DATE', format='%d-%m-%Y')],
                [sg.Text('Enter a time (HH:MM:SS):'), sg.Input(key='TIME', enable_events=True)],
                [sg.Text('Location (53.3924659, -2.0594862):'), sg.Push(), sg.Input(key='LOCATION'), sg.Push()],
                [sg.Text('Image:'), sg.Push(), sg.Input(key='MEDIA'), sg.FileBrowse()],
                [sg.Text(' ')],
                [sg.OK('Submit'), sg.Cancel('Clear'), sg.Push(), sg.Button('Exit')]]

# TAB 2 content
tab2_layout = [[sg.Text('Overview of when Donald was spotted this month')]]

# TAB 3 content
tab3_layout = [[sg.Text('Map of Donald\'s locations')]]

# TAB 4 content
tab4_layout = [[sg.Text('Photos of Donald')]]

# TAB 5 content
tab5_layout = [[sg.Text('All Records here and feature to export to .csv')]]

# define layouts for tabs
tab_group_layout = [[sg.Tab('Submit', tab1_layout), sg.Tab('Calendar', tab2_layout), sg.Tab('Map', tab3_layout), sg.Tab('Media', tab4_layout), sg.Tab('Records', tab5_layout)]]
tab_group = sg.TabGroup(tab_group_layout)

layout = [[[sg.Text('Where\'s Donald Today?', font=('Arial',20))], 
           [sg.Text(' ')],
           tab_group]]

# window event
window = sg.Window('Donald\'s Diary', layout, no_titlebar=True, grab_anywhere=True)

while True:
    event, values=window.read()
    if event == sg.WIN_CLOSED or 'Exit':
        break
    elif event == sg.OK():
        time = values['TIME']
        date = values['DATE']
        status = values['STATUS']
        media = values['MEDIA']
        location = values['LOCATION']
window.close()