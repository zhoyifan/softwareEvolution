import numpy as np

from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly

from distutils.version import StrictVersion,LooseVersion

import pandas as pd
directory="/media/z19941225110/CD_ROM_POS/master/SoftwareEvolution/Assignment-2-2020-master"
cloc=pd.read_csv(f"{directory}/output/cloc.csv")
# print(cloc.columns)
cloc=cloc.set_index('version')
cloc = cloc.reindex(index=pd.Index(sorted(cloc.index, key=LooseVersion)))#,reverse=True
cloc.index.name='version'
cloc=cloc.reset_index()
# cloc=cloc.sort_values(by=['version'])



sum_line=cloc['blank']+cloc['comment']+cloc['code']
cloc['sum']=sum_line


fig = make_subplots(rows=4, cols=1)#, vertical_spacing=0.5/4
fig.add_trace(go.Bar(x=cloc['version'], y=cloc['sum'],name="sum"),row=1,col=1)
fig.add_trace(go.Bar(x=cloc['version'], y=cloc['blank'],name="blank"),row=2,col=1)
fig.add_trace(go.Bar(x=cloc['version'], y=cloc['comment'],name="comment"),row=3,col=1)
fig.add_trace(go.Bar(x=cloc['version'], y=cloc['code'],name="code"),row=4,col=1)
# fig.show()
fig.update_layout(height=1500, width=1500)#, title_text="Subplots"
plotly.offline.plot(fig, filename=f'{directory}/output/barChart.html')






