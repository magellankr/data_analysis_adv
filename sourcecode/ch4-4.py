# %%
import plotly.express as px
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.io as pio
import numpy as np
import matplotlib as mpl

pio.renderers.default = 'notebook' # 또는 'plotly_mimetype' 또는 'plotly_mimetype+notebook'

df = pd.read_csv('../datasets/CO2_emissions/CO2_emissions.csv')

# Matplotlib 테두리 강조하기
fig, ax = plt.subplots()
sns.boxplot(
    x='Cylinders', y='CO2 Emissions(g/km)',
    data=df, ax=ax
)

spines = ['left','right','top','bottom']
for spine in spines:
    ax.spines[spine].set_color('blue')
    ax.spines[spine].set_linewidth(3)
    
# Plotly 테두리 강조하기
fig = px.box(df, x='Cylinders', y='CO2 Emissions(g/km)', width=500, height=400)
fig.update_xaxes(showline=True, linecolor='skyblue', linewidth=3, mirror=True)
fig.update_yaxes(showline=True, linecolor='skyblue', linewidth=3, mirror=True)
fig.show()
# %%
