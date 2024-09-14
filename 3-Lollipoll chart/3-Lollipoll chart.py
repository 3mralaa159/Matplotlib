import matplotlib.pyplot as plt
import pandas as pd

color_dict = {(2004,"Norway"): "#9194A3", (2022,"Norway"): "#2B314D",
              (2004,"Denmark"): "#E2AFA5", (2022,"Denmark"): "#A54836",
              (2004,"Sweden"): "#C4D6F8", (2022,"Sweden"): "#5375D4",
              }

xy_ticklabel_color, xlabel_color, grand_totals_color, grid_color, datalabels_color ='#C8C9C9',"#101628","#101628", "#C8C9C9", "#2B314D"

data = {
    "year": [2004, 2022, 2004, 2022, 2004, 2022],
    "countries" : ["Sweden", "Sweden", "Denmark", "Denmark", "Norway", "Norway"],
    "sites": [13,15,4,10,5,8]
}
df= pd.DataFrame(data)

#custom sort
sort_order_dict = {"Denmark":2, "Sweden":3, "Norway":1, 2004:4, 2022:5}
df = df.sort_values(by=['year','countries',], key=lambda x: x.map(sort_order_dict))

# Add the x-axis labels
df['year_lbl'] ="'"+df['year'].astype(str).str[-2:].astype(str)
df['pct_change'] = df.groupby('countries', sort=False)['sites'].apply(
     lambda x: x.pct_change()).to_numpy()

#Add the color based on the color dictionary
df['color'] = df.set_index(['year', 'countries']).index.map(color_dict.get)
#number of countries to loop over
countries = df.countries.unique()

fig, axes = plt.subplots(ncols=len(countries), nrows=1, figsize=(8,6), sharex=True, sharey=True, facecolor= "white")
fig.tight_layout(pad=3.0)

#loop over the countries
for ctry , ax in zip(countries, axes.ravel()):
    temp_df = df[df.countries==ctry]
    pct = temp_df['pct_change'].max()
    
    #format the plots
    ax.set_ylim(0,df.sites.max()+5)
    ax.set_xlim(-0.5,len(countries)-1.5)
    ax.set_yticks([])
    ax.tick_params(axis='both', which='both',length=0, labelsize=12,colors =xy_ticklabel_color)
    ax.spines[['top', 'left', 'right']].set_visible(False)
    ax.spines['bottom'].set_color(grid_color)
    
    #add the circles at the end of the lolipoll bars
    ax.scatter(temp_df.year_lbl, temp_df.sites, s=150, c= temp_df.color , edgecolors="w", zorder=2)
    
    #add the vertical lines of the lolipoll
    ax.vlines(list(range(len(countries)-1)), 0,temp_df.sites, color = temp_df.color, lw=4,zorder=1)
    
    #add the data labels
    for i,lb in enumerate(temp_df.sites):
        ax.annotate(lb, xy=(i,lb+1), size=13,color =datalabels_color, weight= "bold", ha="center", va="center")
        
    #add the x-axis titles
    ax.set_xlabel(f'\u25B2\n{pct:.0%}\n\n{ctry}',  color = xlabel_color, size = 12, weight= "bold")
    ax.xaxis.set_label_coords(0.5, -0.1)
