""" This file contains the env variables
 (excluding the path env variable that can be found
 in the path.py file) """

# List of variable whose legend in the streamlit line plot want to be modified
LEGEND_TO_MODIFY = ["Weekday", "season", "weather"]
# Dictionnary allowing streamlit line plot legend modification
PLOT_LEGEND_DICT = {
     "Weekday" : ['Monday','Tuesday', 'Wednesday', 
                  'Thursday', 'Friday', 'Saturday', 'Sunday' ],
     "season" : ['Winter','Spring', 'Summer', 'Autumn'],
     "weather" : ['Clear to cloudy', 'Foggy', 'Light rain or snow',
                   'Heavy showers or snow']
}
#
LINE_PLOT_VARS = ['Weekday','season', 'holiday', 'workingday',
                  'weather', 'Year', 'Month']

LABEL_MAP = {
     "Weekday" : {0 :'Monday', 1 :'Tuesday', 2: 'Wednesday', 
                 3: 'Thursday', 4: 'Friday', 5:'Saturday', 6:'Sunday' },
     "season" : {2:'Spring', 3:'Summer', 4:'Autumn', 1:'Winter'},
     "weather" : {1:'Clear to cloudy', 2:'Foggy', 3:'Light rain or snow',
                   4:'Heavy showers or snow'}
}