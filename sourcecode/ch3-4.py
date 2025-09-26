# %%
import plotly.express as px
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.io as pio
pio.renderers.default = 'notebook' # 또는 'plotly_mimetype' 또는 'plotly_mimetype+notebook'


df = pd.read_csv('../datasets/EV_charge/EV_charge.csv')

fig, ax = plt.subplots()
sns.boxplot(x='weekday', y='kwhTotal', data=df, ax=ax, order=weekday_order, palette="Set2")


# %%
