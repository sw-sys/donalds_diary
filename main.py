import csv
import re
import sqlite3
import PySimpleGUI as sg


### DATABASE

conn = sqlite3.connect('donalds_data.db')
c = conn.cursor() # cursor allows interigation of data
c.execute("""CREATE TABLE IF NOT EXISTS sightings
          (status text,
          date text,
          time text,
          location real)
          """)

conn.commit()
conn.close()

### GUI VISUAL DESIGN
sg.theme('DarkGray6')
sg.set_options(font=('Arial 12'), text_color='white')

### WINDOW CONTENT BEGINS

### data submission
# options for status
STATUS_OPTIONS = ['Seen', 'Not seen', 'Unknown']

layout_l = [
        [sg.Text('Where\'s Donald Today?', font=('Arial',30), background_color='#69888D', text_color='white')],
            ]

layout_r = [
        [sg.Button('Exit')],
            ]

frame_layout = [
                    [sg.Text(' ')],
                    [sg.Text('Status '), sg.Push(), sg.Combo(STATUS_OPTIONS, default_value=STATUS_OPTIONS[0], key='STATUS'), sg.Push(), sg.Push(), sg.Push()],
                    [sg.Text('Enter Date YYYY-MM-DD'),sg.Input(key='DATE'), sg.Push(), sg.CalendarButton('Select', target='DATE', format='%Y-%m-%d')],
                    [sg.Text('Enter a time HH:MM'), sg.Push(), sg.Push(), sg.Input(key='TIME', enable_events=False), sg.Push(), sg.Push(), sg.Push(), sg.Push()],
                    [sg.Text('Location '), sg.Push(), sg.Push(), sg.Push(), sg.Input(key='LOCATION'), sg.Push(), sg.Push()],
                    [sg.Text(' ')],
                    [sg.Push(), sg.Push(), sg.Button('Submit'), sg.Button('Clear')],
                ]

layout = [
            [sg.Col(layout_l), sg.Push(), sg.Col(layout_r)],
            [sg.Text(' ')],
            [sg.Frame('', frame_layout, title_color='white')],
            [sg.Text(' ')],
            [sg.Push(), sg.Button('Show records'), sg.Button('Save to CSV', key='save_button')],
        ]

# window event
window = sg.Window('Donald\'s Diary', layout, no_titlebar=True, grab_anywhere=True)

### DATABASE

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

# func holds sightings
def get_sightings():
    sightings_records = retrieve_records()
    return sightings_records

# func populates 'Records'
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

def save_to_csv():
    data = get_sightings()
    with open('sightings_records.csv', 'a', encoding='UTF8', newline='') as file:
        writer = csv.writer(file)
        for row in data:
            row = [item.strip("[]").replace("'", "") for item in row]
            writer.writerow(row)

while True:
    #close programm
    event, values=window.read()
    if event in (sg.WIN_CLOSED or 'Exit'):
        conn.close()
        break
    # condition for buttons
    if event == 'Clear':
        clear_inputs()
    if event == 'Show records':
        create_records()
    if event == 'save_button':
        #save_data_to_database()
        data = get_sightings()
        save_to_csv()
        sg.PopupQuick('Data saved to CSV file')
    # ensure no blank submissions
    if event == 'Submit':
        status = values['STATUS']
        if status == '':
            sg.PopupError('QUACK! \n Please insert a status')
            break
        date = values['DATE']
        if date =='':
            sg.PopupError('QUACK! \n Please insert a date')
            break
        else:
            # date input format validation
            if not re.match(r'^(2023-(0[1-9]|1[0-2])-(0[1-9]|1[0-9]|2[0-9])|3[0-1])', date):
                sg.PopupError(f'QUACK! \n Date should be realistic, numerical \nand formatted as YYYY-MM-DD')
        time = values['TIME']
        if time =='':
            sg.PopupError('QUACK! \n Please insert a time')
            break
        else:
            # time input format validation
            if not re.match(r'^(0[1-9]|1[0-9]|2[0-3]):([0-5][0-9])$', time):
                sg.PopupError(f'QUACK! \n Time should be numerical \n and formatted as HH:MM')
        location = values['LOCATION']
        if location == '':
            sg.PopupError('QUACK! \n Please insert a location')
            break
        if status and date and time and location != '':
        #else:
            try:
                SUMMARY_LIST = "The following bread crumbs have been added to the quackbase"
                CHOICE = sg.PopupOKCancel(SUMMARY_LIST, 'Please confirm entry')
                if CHOICE =='OK':
                    clear_inputs()
                    save_data_to_database()
                    sg.PopupQuick('Saved to quackbase and exported to csv!')
                else:
                    sg.PopupOK('Edit entry')
            except:
                sg.Popup('MAJOR QUACK! \n Something went very wrong. \nFetch the peas and try again.')

window.close()