""" This file contains the env variables
 (excluding the path env variable that can be found
 in the path.py file) """

# List of variable whose legend in the streamlit line plot want to be modified
LEGEND_TO_MODIFY = ["Weekday", "season"]
# Dictionnary allowing streamlit line plot legend modification
PLOT_LEGEND_DICT = {
     "Weekday" : ['Monday','Tuesday', 'Wednesday', 
                  'Thursday', 'Friday', 'Saturday', 'Sunday' ],
     "season" : ['Spring', 'Summer', 'Autumn', 'Winter'],
     "weather" : ['Clear to cloudy', 'Foggy', 'Light rain or snow',
                   'Heavy showers or snow']
}
#
LINE_PLOT_VARS = ['Weekday','season', 'holiday', 'workingday',
                  'weather']
