# %%
import plotly.express as px
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.io as pio
import numpy as np
import matplotlib as mpl

pio.renderers.default = 'notebook' # 또는 'plotly_mimetype' 또는 'plotly_mimetype+notebook'
df = sns.load_dataset('mpg')


fig, ax = plt.subplots()
sns.regplot(x='horsepower', y='weight', data=df, ax=ax)

# 선형 회귀식 구하기
from scipy.stats import linregress

s, i, r, p, se = linregress(df['horsepower'], df['weight'])
print("======================")
print('y={:.2f}x+{:.2f}, R^2={:.2f}'.format(s, i, r**2))
print("======================")

print(df)
# info 메서드
print(df.info())

# dropna 수행 후 선형회귀식 시각화
df = df.dropna()
s, i, r, p, se = linregress(df['horsepower'], df['weight'])
print("2222222")
print('y={:.2f}x+{:.2f}, R^2={:.2f}'.format(s, i, r**2))
print("======================")

fig, ax = plt.subplots()
sns.regplot(
    x='horsepower', y='weight', data=df, ax=ax,
    line_kws={'label':'y={:.2f}x+{:.2f}, R^2={:.2f}'.format(s, i, r**2)}
)
ax.legend()

# text 메서드를 이용한 선형회귀식 시각화
fig, ax = plt.subplots()
sns.regplot(x='horsepower', y='weight', data=df, ax=ax)
ax.text(
    x=0.05, y=0.9,
    s='#2 y={:.2f}x+{:.2f}, R^2={:.2f}'.format(s, i, r**2),
    transform=ax.transAxes
)
# Plotly trendline을 이용한 회귀식 표현
fig = px.scatter(
    df, x='horsepower', y='weight', width=500, height=400,
    trendline='ols'
)

results = px.get_trendline_results(fig)
results = results.iloc[0]["px_fit_results"]
print(results.summary())

# Plotly trendline을 이용한 회귀식 파라메터 확인
results.params

# Plotly add_annotation 메서드를 이용한 선형회귀식 시각화
fig = px.scatter(
    df, x='horsepower', y='weight', width=500, height=400,
    trendline='ols'
)

fig.add_annotation(
    text='#3 y= {:.1f}x + {:.1f}, R^2={:.2f}'.format(results.params[0], results.params[0], results.rsquared),
    x=0.05, y=0.95, xref='x domain', yref='y domain', showarrow=False
)

fig.show()
# %%
