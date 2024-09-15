import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd

color_dict = {"Norway": "#2B314D", "Denmark": "#A54836", "Sweden": "#5375D4", }

xy_ticklabel_color, xlabel_color, grand_totals_color, legend_color, grid_color, datalabels_color ='#101628',"#101628","#101628","#101628", "#C8C9C9", "#757C85"

data = {
    "year": [2004, 2022, 2004, 2022, 2004, 2022],
    "countries" : ["Sweden", "Sweden", "Denmark", "Denmark", "Norway", "Norway"],
    "sites": [13,15,4,10,5,8,]
}
df= pd.DataFrame(data)
df['sub_total'] = df.groupby('year')['sites'].transform('sum')

#custom sort
sort_order_dict = {"Denmark":3, "Sweden":1, "Norway":2, 2004:4, 2022:5}
df = df.sort_values(by=['year','countries',], key=lambda x: x.map(sort_order_dict))

#map colors
df['colors']= df.countries.map(color_dict)
years = df.year.unique()
countries = df.countries.unique()
nr_countries = len(countries)
sub_totals = df.sub_total.unique()
colors = df.colors

# width/depth of bars
dx = 2 ; dy = 2 ; dz = df.sites.to_list()
# Positions 
xs = np.repeat(np.arange(0, len(countries)-1)*8,len(countries)).tolist()
ys = np.repeat(np.arange(0, len(countries)-1)*4,len(countries)).tolist()

# add position of each dz values in stacked bar 
# equals to botton in bar chart , changing the start point for each value 
zs = np.array(df.groupby('year', sort= False).sites.apply(list).tolist()) #convert to a numpy 2d array
zs = np.cumsum(zs, axis =1)[:,:nr_countries-1] #accumulate sum, remove last item
zs = np.insert(zs, 0, 0, axis=1).flatten().tolist() #add a zero at the beginning, flatten and convert to list


fig = plt.figure(figsize=(15,10))
ax = fig.add_subplot(1, 1, 1, projection="3d")

ax.bar3d(xs, ys, zs, dx, dy, dz, color=colors , label = countries)
#give the labels to each point
for x, y, z, site in zip(xs, ys,zs, dz ):
    ax.text(x-1.5, y, z+site/2,site, size=14, ha= "right", color = datalabels_color)

#add legend
lines = [Line2D([0], [0], color=c,  marker='s',linestyle='', markersize=10,) for c in reversed(colors.unique())]
labels = df.countries.unique()
plt.legend(lines, reversed(labels), labelcolor = legend_color,
           prop=dict(weight='bold', size=12), 
           bbox_to_anchor=(0.5, -0.05), loc="lower center",
            ncols = 3,frameon=False, fontsize= 14)

for i, (year,sub_total) in enumerate(zip(years,sub_totals)):
    # add year tick labels
    ax.text(xs[i * nr_countries], ys[i * nr_countries], z= -3 , s=f"{year}", color = xy_ticklabel_color, weight= "bold", fontsize=12)

    ax.text(xs[i * nr_countries]+0.5, ys[i * nr_countries], z=zs[i * nr_countries]+sub_total +2 ,
             s=f"{sub_total}",  fontsize=12, weight="bold", color= grand_totals_color,
             bbox=dict(facecolor='none', edgecolor='#EBEDEE', boxstyle='round,pad=0.3'))


ax.set_aspect("equal")
ax.set_axis_off()
