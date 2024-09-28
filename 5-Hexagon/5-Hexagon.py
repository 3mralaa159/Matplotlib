import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.lines import Line2D
import numpy as np

# make a color map of fixed colors
cmap_den = colors.ListedColormap(["#E2AFA5","#CC5A43"])
cmap_nor = colors.ListedColormap(["#9194A3","#2B314D"])
cmap_swe = colors.ListedColormap(["#C4D6F8","#5475D6"])

x_den = np.array([2,1,3,2,2,1,1,2,2,3,3,1,2,3])
y_den = np.array([1,2,2,3,3,4,4,5,5,4,4,6,7,6])

x_nor = np.array([1,2,2,3,3,1,1,2,2,1,1,2,3])
y_nor = np.array([1,2,2,3,3,3,3,4,4,5,5,6,5])

x_swe = np.array([1,1,1,2,2,2,2,2,2,2,2,3,3,3,3,3,3,4,4,4,4,4,4,4,4,5,5,5,])
y_swe = np.array([4,4,6,1,1,3,3,5,5,7,7,2,2,4,4,6,6,1,1,3,3,5,5,7,7,2,4,4])


def hex_plot(x, y, gx, gy, cmap, ax):
    hex = ax.hexbin(y, x, gridsize=(gx,gy), cmap=cmap,
                  ec='white', lw=2, 
                 mincnt=1,#dont show values=0
                 )

    # exchange x and y
    hexagon = hex.get_paths()[0]
    hexagon.vertices = hexagon.vertices[:, ::-1]  # exchange the x and y coordinates of the basic hexagon
    offsets = hex.get_offsets()
    hex.set_offsets(offsets[:, ::-1])
    ax.set_ylim(y.min()-2,y.max()+2)  # apply the original ylim to xlim
    ax.set_xlim(x.min()-2,x.max()+2)
    ax.set_axis_off()


fig, (ax1, ax2, ax3) = plt.subplots(ncols=3,figsize=(16, 6))

#plot the hexagons
hex_plot(x_den, y_den, 4,1, cmap_den, ax3)
hex_plot(x_nor, y_nor, 3,1,cmap_nor, ax2)
hex_plot(x_swe, y_swe, 4,2,cmap_swe, ax1)

#add the plot titles
ax1.text(2.5, 8, "Sweden", size = 12, weight = "bold" )
ax2.text(1.6, 7, "Norway", size = 12, weight = "bold" )
ax3.text(1.6, 8, "Denmark", size = 12, weight = "bold" )

#add legends
labels = ['2004','2022']
colors = ["#5475D6","#C4D6F8",]
lines = [Line2D([0], [0], color=c,  marker='h',linestyle='', markersize=20,) for c in colors]
plt.figlegend( lines,labels,
           bbox_to_anchor=(0.5, -0.05), loc="lower center",
            ncols = 2,frameon=False, fontsize= 14)
