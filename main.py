import PySimpleGUI as sg
import sqlite3
import csv

### DATABASE

conn = sqlite3.connect('donalds_data.db')
c = conn.cursor() # cursor allows interigation of data
c.execute("""CREATE TABLE IF NOT EXISTS sightings (
          status text,
          date text,
          time text,
          location real
          )""")

conn.commit()
conn.close()

### DESIGN
sg.theme('DarkGray6')
sg.set_options(font=('Arial 12'), text_color='white')

### WINDOW CONTENT BEGINS

### TABS FOR VIEWS

# TAB 1 - data submission

# options for status
status_options = ['Seen', 'Not seen', 'Unknown']

layout = [
    [sg.Text('Where\'s Donald Today?                       ', font=('Arial',30), background_color='#69888D', text_color='white')], 
    [sg.Text(' ')],
    [sg.Text('Status:'), sg.Combo(status_options, default_value=status_options[0], key='STATUS'), sg.Push(), sg.Push()],
    [sg.Text('Enter Date YYYY-MM-DD'),sg.Input(key='DATE'), sg.Push(), sg.CalendarButton('Select', target='DATE', format='%Y-%m-%d')],
    [sg.Text('Enter a time HH:MM:SS'), sg.Push(), sg.Input(key='TIME', enable_events=False), sg.Push(), sg.Push(), sg.Push(), sg.Push()],
    [sg.Text('Location (co-ordinates)'), sg.Push(), sg.Input(key='LOCATION'), sg.Push(), sg.Push(), sg.Push(), sg.Push()],
    [sg.Text(' ')],
    [sg.Button('Submit'), sg.Button('Clear'), sg.Push(), sg.Button('Show records'), sg.Button('Save to CSV'), sg.Push(), sg.Button('Exit')]
]

# window event
window = sg.Window('Donald\'s Diary', layout, no_titlebar=True, grab_anywhere=True)

### FUNCs for views
# Records tab

# func gets records from db
def retrieve_records():
    results = []
    conn = sqlite3.connect('donalds_data.db')
    c = conn.cursor()
    query = "SELECT status, date, time, location FROM sightings"
    c.execute(query)
    for row in c:
        results.append(list(row))
    return results

# func has sightings
def get_sightings():
    sightings_records = retrieve_records()
    return sightings_records

# func populates tab 5 content 'Records'
def create_records():
    sightings_array = get_sightings()
    headings = ['SEEN STATUS', 'SIGHTING DATE', 'SIGHTING TIME', 'SIGHTING LOCATION']

    layout_for_display = [
        [sg.Table(values=sightings_array,
                  headings=headings,
                  max_col_width=35,
                  auto_size_columns=True,
                  display_row_numbers=True,
                  justification='left',
                  num_rows=10,
                  key='SIGHTINGSTBL',
                  row_height=60,
                  enable_events=True,
                  )]
    ]
    windowr=sg.Window('Summary results', layout_for_display, modal = True)

    while True:
        event, values = windowr.read()
        if event == sg.WIN_CLOSED:
            break

def clear_inputs():
    for key in values:
        window['TIME'].update('')
        window['DATE'].update('')
        window['STATUS'].update('')
        #window['MEDIA'].update('')
        window['LOCATION'].update('')
    return None

def save_data_to_database():
    conn=sqlite3.connect('donalds_data.db')
    c = conn.cursor() # cursor allows interigation of data
    c.execute("INSERT INTO sightings VALUES (:status, :date, :time, :location)",
              {
                  'status': values['STATUS'],
                  'date': values['DATE'],
                  'time': values['TIME'],
                  'location': values['LOCATION'],
              })

    conn.commit()
    conn.close()

# def export_to_csv():
#     conn = sqlite3.connect('donalds_date.db')
#     c = conn.cursor()
#     query = "SELECT * FROM sightings"
#     c.execute(query)
#     with open('sightings.csv', 'w', newline='') as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerow(['Status', 'Date', 'Time', 'Location'])
#         for row in c:
#             writer.writerow(row)
#     conn.close()

while True:
    event, values=window.read()
    if event in (sg.WIN_CLOSED or 'Exit'):
        break
    if event == 'Clear':
        clear_inputs()
    if event == 'Show records':
        create_records()
    # if event == 'Save to CSV':
    #     export_to_csv()
    if event == 'Submit':
        status = values['STATUS']
        if status == '':
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
        else:
            try:
                summary_list = "The following bread crumbs have been added to the quackbase"
                choice = sg.PopupOKCancel(summary_list, 'Please confirm entry')
                if choice =='OK':
                    clear_inputs()
                    save_data_to_database()
                    sg.PopupQuick('Saved to quackbase and exported to csv!')
                else:
                    sg.PopupOK('Edit entry')
            except:
                sg.Popup('MAJOR QUACK ALERT! Fetch the peas and try again.')

window.close()