import PySimpleGUI as sg

# theme - colours for GUI
sg.theme('DarkGray5') # 2 best so far

# window content begins

# options for status
options = ['Seen', 'Not seen', 'Unknown']

layout = [
    [sg.Text('Record your daily dose of Donald', font=('Arial',20))],

    [sg.CalendarButton('Select Date:', target='date_input', format='%d-%m-%Y'), sg.InputText(key='DATE')],

    [sg.Text('Enter a time (HH:MM:SS):'), sg.Input(key='TIME', enable_events=True)],

    [sg.Text('Status (seen, not seen, unknown):'), sg.Combo(options, default_value=options[0], key='STATUS')],

    [sg.Text('Location (co-ords):')],

    [sg.Text('Image:'), sg.Input(), sg.FileBrowse()],

    [sg.OK(), sg.Cancel()]
        ]

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
window.close