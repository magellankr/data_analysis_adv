# %%
import plotly.express as px
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.io as pio
pio.renderers.default = 'notebook' # 또는 'plotly_mimetype' 또는 'plotly_mimetype+notebook'

df = sns.load_dataset('tips')

fig, ax = plt.subplots()
sns.histplot(df, x='total_bill', ax=ax)
plt.title("#1")
plt.show()

# Seaborn histplot의 bin size 수정
fig, ax = plt.subplots()
sns.histplot(df, x='total_bill', ax=ax, bins=30)
plt.title("#2")
plt.show()

# Seaborn histplot의 bin size 수정2
fig, ax = plt.subplots()
sns.histplot(df, x='total_bill', ax=ax, binwidth=2)
plt.title("#3")
plt.show()

# Seaborn histplot의 특정 변수 그룹별 막대 나누기
fig, ax = plt.subplots()
sns.histplot(df, x='total_bill', ax=ax, hue='time')
plt.title("#4")
plt.show()

# Seaborn histplot의 multiple 인자 활용
fig, ax = plt.subplots()
sns.histplot(df, x='total_bill', ax=ax, hue='time', multiple='stack')
plt.title("#5")
plt.show()

# Ploty histogram
df = sns.load_dataset('tips')

fig = px.histogram(data_frame=df, x='total_bill', width=450)
fig.show()

# Plotly histplot의 bin size 수정
fig = px.histogram(
    data_frame=df, x='total_bill', width=450, nbins=20
)
fig.show()

# Plotly histplot의 특정 변수 그룹별 막대 나누기
fig = px.histogram(
    data_frame=df, x='total_bill', width=450,
    color='time', barmode='overlay', title='With overlay'
)
fig.show()
fig = px.histogram(
    data_frame=df, x='total_bill', width=450,
    color='time', barmode='relative', title='With relative'
)
fig.show()
fig = px.histogram(
    data_frame=df, x='total_bill', width=450,
    color='time', barmode='group', title='With Group'
)
fig.show()
# Plotly histplot의 특정 변수 그룹별 막대 나누기2
fig = px.histogram(
    data_frame=df, x='total_bill', width=450, color='time'
)
fig.show()
# %%
