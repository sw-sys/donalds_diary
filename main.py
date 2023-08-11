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
                [sg.Text('Status:'), sg.Combo(status_options, default_value=status_options[0], key='STATUS'), sg.Push(), sg.Push()],
                #[sg.Text('Status:'), sg.Push(), sg.Combo(status_options, default_value=status_options[0], key='STATUS'), sg.Push(), sg.Push()],
                [sg.Text('Enter Date DD-MM-YYYY'),sg.Input(key='DATE'), sg.Push(), sg.CalendarButton('Select', target='DATE', format='%d-%m-%Y')],
                [sg.Text('Enter a time HH:MM:SS'), sg.Push(), sg.Input(key='TIME', enable_events=False), sg.Push(), sg.Push(), sg.Push(), sg.Push()],
                [sg.Text('Location (co-ordinates)'), sg.Push(), sg.Input(default_text ='53.3924659, -2.0594862', key='LOCATION'), sg.Push(), sg.Push(), sg.Push(), sg.Push()],
                #[sg.Text('Upload an image'), sg.Push(), sg.Input(key='MEDIA'), sg.FileBrowse()],
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

# Header and tab holder

header_layout =[
    #[sg.Image(r'C:\Users\Sheldon\Documents\Coding\Donalds_Diary\Mallard_head.png')],
    [sg.Text('Where\'s Donald Today?                       ', font=('Arial',30), background_color='#69888D', text_color='white')], 
    [sg.Text('')],
]

window_layout = [
    header_layout,
    [tab_group]
]

# window event
window = sg.Window('Donald\'s Diary', window_layout, no_titlebar=True, grab_anywhere=True)

def clear_inputs():
    for key in values:
        window['TIME'].update('')
        window['DATE'].update('')
        window['STATUS'].update('')
        #window['MEDIA'].update('')
        window['LOCATION'].update('')
    return None

while True:
    event, values=window.read()
    if event in (sg.WIN_CLOSED or 'Exit'):
        break
    if event == 'Clear':
        clear_inputs()
    if event == 'Submit':
        status = values['STATUS']
        if status=='':
            sg.PopupError('QUACK ALERT! Please insert a status')
        date = values['DATE']
        if date =='':
            sg.PopupError('QUACK ALERT! Please insert a date')
        time = values['TIME']
        if time =='':
            sg.PopupError('QUACK ALERT! Please insert a time')
        location = values['LOCATION']
        if status == '':
            sg.PopupError('QUACK ALERT! Please insert a location')
        #media = values['MEDIA']
        else:
            try:
                summary_list = "The following bread crumbs have been added to the quackbase"
                choice = sg.PopupOKCancel(summary_list, 'Please confirm entry')
                if choice =='OK':
                    clear_inputs()
                    sg.PopupQuick('Saved to quackbase!')
                else:
                    sg.PopupOK('Edit entry')
            except:
                sg.Popup('MAJOR QUACK ALERT! Fetch the peas and try again.')

window.close()