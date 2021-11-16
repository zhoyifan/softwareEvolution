import pandas as pd
# import math

import seaborn as sb
import matplotlib.pyplot as plt


import matplotlib
from matplotlib import cm
import plotly.graph_objects as go
import plotly

from distutils.version import StrictVersion,LooseVersion

directory="/media/z19941225110/CD_ROM_POS/master/SoftwareEvolution/Assignment-2-2020-master"
similarity=pd.read_csv(f"{directory}/output/similarity.csv")
similarity=similarity.rename(columns={"Unnamed: 0":"versions"})
similarity=similarity.set_index('versions')

similarity = similarity.reindex(index=pd.Index(sorted(similarity.index, key=LooseVersion,reverse=True)))
similarity=similarity[sorted(similarity.columns, key=LooseVersion)]

# heatmap=sb.heatmap(similarity, annot=False, fmt="g", cmap='viridis')
# plt.show()
# figure = heatmap.get_figure()
# figure.savefig(f'{directory}/output/heatmapPlt.png', dpi=400)

# import matplotlib
# from matplotlib import cm
# import numpy as np

# cool_cmap = matplotlib.cm.get_cmap('cool')
# cool_rgb = []
# norm = matplotlib.colors.Normalize(vmin=0, vmax=255)
# for i in range(0, 255):
#        k = matplotlib.colors.colorConverter.to_rgb(cool_cmap(norm(i)))
#        cool_rgb.append(k)
# def matplotlib_to_plotly(cmap, pl_entries):
#     h = 1.0/(pl_entries-1)
#     pl_colorscale = []

#     for k in range(pl_entries):
#         C = list(map(np.uint8, np.array(cmap(k*h)[:3])*255))
#         print(C)
#         pl_colorscale.append([k*h, 'rgb'+str((C[0], C[1], C[2]))])
    
#     return pl_colorscale
# cool = matplotlib_to_plotly(cool_cmap, 255)






figWidth=2000
figHeight=2000
cloc=pd.read_csv(f"{directory}/output/cloc.csv")
cloc=cloc.set_index('version')
total=cloc['sum'].sum()


tickPosY=[]
blockPosY=[0]
axisLast=0
for version in similarity.index:
    lengthNow=figHeight*cloc.loc[version,'sum']/total 
    axisNow=axisLast+lengthNow/2
    tickPosY.append(axisNow)
    axisLast=axisLast+lengthNow
    blockPosY.append(axisLast)

tickPosX=[]
blockPosX=[0]
axisLast=0
for version in similarity.columns:
    lengthNow=figWidth*cloc.loc[version,'sum']/total 
    axisNow=axisLast+lengthNow/2
    tickPosX.append(axisNow)
    axisLast=axisLast+lengthNow
    blockPosX.append(axisLast)


heatmap=go.Heatmap(
                x=blockPosX
                ,y=blockPosY
                ,z=similarity
                ,colorscale=['#1ff4ff','#16f100','#fffb0e','#fc0800']
                )
lines=[]
for blockPosXNow in blockPosX:
    line=go.Scatter(x=[blockPosXNow, blockPosXNow]
                    ,y=[0, figHeight]
                    ,mode='lines'
                   ,line_color='black'
                   , line_width=2.5
                   ,showlegend=False
                   ,hoverinfo='skip'
                #    ,name=None
                #    ,hovertemplatesrc='<extra></extra>'
                    ,hoverlabel=dict(namelength=0) 
                    # ,hoveron=""   
                   )
    lines.append(line)
for blockPosYNow in blockPosY:
    line=go.Scatter(x=[0, figWidth]
                   ,y=[blockPosYNow, blockPosYNow]
                   ,mode='lines'
                   ,line_color='black'
                   , line_width=2.5
                   ,showlegend=False 
                    ,hoverinfo='skip'
                    # ,name=None
                    # ,hovertemplatesrc='<extra></extra>'  
                    ,hoverlabel=dict(namelength=0)
                    # ,hoveron=""   
                   )
    lines.append(line)
fig = go.Figure(data=[heatmap]+lines
,layout=dict(
    xaxis = dict(
        tickmode = 'array'
        ,tickvals=tickPosX
        ,ticktext=list(similarity.columns)
        ,tickfont=dict(size=9)
    ),
    yaxis = dict(
        tickmode = 'array'
        ,tickvals=tickPosY
        ,ticktext=list(similarity.index)
        ,tickfont=dict(size=9)
    )
    ,autosize=False
    ,width=figWidth
    ,height=figHeight
    ,xaxis_showgrid=False
    ,yaxis_showgrid=False
    ,margin=dict(
        # l=0
        # ,r=0
        # ,
        b=0
        ,t=0
        # ,pad=0
    )
)
)


fig.update_layout(
    xaxis = dict(
        tickmode = 'array'
        ,tickvals=tickPosX
        ,ticktext=list(similarity.columns)
        ,tickfont=dict(size=9)
    ),
    yaxis = dict(
        tickmode = 'array'
        ,tickvals=tickPosY
        ,ticktext=list(similarity.index)
        ,tickfont=dict(size=9)
    )
    ,autosize=False
    ,width=figWidth
    ,height=figHeight
    ,xaxis_showgrid=False
    ,yaxis_showgrid=False
    ,margin=dict(
        # l=0
        # ,r=0
        # ,
        b=0
        ,t=0
        # ,pad=0
    )
)
# fig.show()
plotly.offline.plot(fig, filename=f'{directory}/output/heatmapPlotly.html')
