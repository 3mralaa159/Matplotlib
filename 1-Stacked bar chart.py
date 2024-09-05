import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

color_dict = {"Norway": "#2B314D", "Denmark": "#A54836", "Sweden": "#5375D4", }
xylabel_color, grand_totals_color, grid_color, datalabels_color ='#757C85',"#101628", "#C8C9C9", "w"

data = {
    "year": [2004, 2022, 2004, 2022, 2004, 2022],
    "countries" : ["Sweden", "Sweden", "Denmark", "Denmark", "Norway", "Norway"],
    "sites": [13,15,4,10,5,8]
}

df= pd.DataFrame(data)


df['sub_total'] = df.groupby('year')['sites'].transform('sum')
#custom sort
sort_order_dict = {"Denmark":2, "Sweden":3, "Norway":1, 2004:4, 2022:5}
df = df.sort_values(by=['year','countries',], key=lambda x: x.map(sort_order_dict))
#map the colors of a dict to a dataframe
df['color']= df.countries.map(color_dict)


unique_countries = df.countries.unique()
countries = df.countries

years = df.year.unique()
colors = df.color


fig, ax = plt.subplots(figsize=(7,10), facecolor = "#FFFFFF" )

# stacked bar char setup
# x-axis = years of DF 
#  , so if u pick just years figure will have all years even not included in DF and show bars at DF years values
#  , if u go for len(years) figure will have only 1 bar 
#  , range(len(years)) will pick DF years and show its values
# y-axis = sites values \ country 
# for stacked bar u will need bottom starting at zero for each bar of years values
bottom = np.zeros(len(years))
for country, color  in zip(unique_countries, colors):
    y = df[df["countries"] == country]["sites"].to_numpy()
    ax.bar(range(len(years)), y, bottom = bottom,  width= 0.6, color=color)
    bottom +=y

# Show sum on each stacked bar
for i, year in enumerate(years):
    total =df[df["year"] == year].sort_values("year")["sub_total"].values.max()
    ax.text(i, total+1 , total, ha='center', size = 20, color = grand_totals_color) #weight='bold')


#add data labels
for bar in ax.patches:
    ax.text(
        bar.get_x() + bar.get_width() / 2,            # Put the text in the middle of each bar. get_x returns the start, so we add half the width to get to the middle.
        bar.get_height()/2 + bar.get_y(),              # Vertically, add the height of the bar to the start of the bar,  along with the offset. (To be cumulative)  
        round(bar.get_height()),                          # This is actual value we'll show.
        ha='center', color=datalabels_color,  size=16  )

#add country legend at the end bar only 
offset_text = 1
for bar, country, color in zip(ax.patches[1::2], countries, colors):  #get every other element skip one
    ax.text(
        bar.get_x() + bar.get_width() + offset_text, 
        bar.get_height()/2 + bar.get_y(),
        country,
        ha='center', color=color,  size=16 )

# We change the fontsize of minor ticks label 
ax.tick_params(axis='both', which='major', length=0, labelsize=16,colors= xylabel_color,pad =15)
ax.xaxis.set_ticks(range(len(years)), labels =years)

#add vertical grid lines
ax.set_axisbelow(True) #set the grid lines in the BACK
ax.grid(True, axis='y', linestyle='solid',  linewidth=1, color = grid_color)
ax.set_xlim(-1,2)
ax.set_ylim(0,35)
ax.spines[['left', 'right', 'top', 'bottom']].set_visible(False)
plt.show()

![Alt text](stacked-bar-chart.png)
