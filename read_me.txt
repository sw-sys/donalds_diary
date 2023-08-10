Notes:

Activate env - conda activate donald
Docs - https://www.pysimplegui.org/en/latest/#pysimplegui-users-manual

Broken: tab_group_layout / tab1_layout 

- define the layout for each tab before you reference it in the 'tab' element 
OR 
- typo
OR
- tab1_layout variable not defined before referenced...or is out of scope

in relation to...
### WINDOW CONTENT BEGINS

# define layouts for tabs
# tabs for views
tab_group_layout = [[sg.Tab('Submit', tab1_layout), sg.Tab('Calender', tab2_layout), sg.Tab('Map', tab3_layout), sg.Tab('Media', tab4_layout)]]

# TAB 1 - data submission
# options for status
options = ['Seen', 'Not seen', 'Unknown'],
tab1_layout =