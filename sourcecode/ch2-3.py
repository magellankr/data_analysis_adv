# %%
import pandas as pd
import numpy as np

s = pd.Series([0, 0, 1, 1, 0, 1, 1, 1, 1, 0])
s

#
sc = s.cumsum()
sc

#
s.mul(sc)

#
s.mul(sc).diff()

#
s.mul(sc).diff().where(lambda x: x<0)

#
s.mul(sc).diff().where(lambda x: x<0).ffill()

#
print("책:", s.mul(sc).diff().where(lambda x: x<0).ffill().add(sc, fill_value=0))

# by chatbot
out = s.groupby((s != s.shift()).cumsum()).cumcount().add(1).where(s.eq(1), 0)
print("ChatBot : ", out.tolist())
# 실전 데이터에 적용
df = pd.read_csv('../datasets/APPL_price/APPL_price.csv')
s = df['Close'] > 175
print("종가 > 175 : ", s.sum())
print(s)

# 실전 데이터에 적용
sc = s.cumsum()
print("책:", s.mul(sc).diff().where(lambda x: x<0).ffill().add(sc, fill_value=0).max())
print("chatbot:", s.groupby((s != s.shift()).cumsum()).cumcount().add(1).where(s.eq(1), 0).max())
# print(out.tolist())
#ChatBot

# %%
