""" """

import plotly.express as px
from src.env import LEGEND_TO_MODIFY, PLOT_LEGEND_DICT
var = "Day"
# ## Feature "Hour" for each day
# # For each day of the week plot average count as function of the hour
# def plot_hour_vs_var(var: str) :
#     f, ax = plt.subplots(figsize=(12, 8))
#     df_plot = pd.DataFrame(data.groupby(['Hour',var],sort=True)['count'].mean()).reset_index()
#     sns.pointplot(x=data['Hour'], y=data['count'],hue = data[var], data=data, join=True, legend_out = True)
#     ax.set(xlabel='Hour', ylabel='Number of users')
#     leg_handles = ax.get_legend_handles_labels()[0]
#     ax.legend(leg_handles,  ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'])
#     return f



def plot_hour_vs_var(data, var, agg_method = "median"):

   #     self = _self

    print("Creating plot 1...") # modify with spinner
    grouped_data = data.groupby(["Hour", var]).agg({
        "count": agg_method
    }).reset_index()   
    fig = px.line(grouped_data, x=grouped_data.Hour, y='count', color=var, 
                markers=True, labels={'count':f'{agg_method} hourly number of users'})
    if var in LEGEND_TO_MODIFY:
        for i, new_name in enumerate(PLOT_LEGEND_DICT[var]):
            fig.data[i].name = new_name

    return fig
    
