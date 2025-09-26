# %%
import pandas as pd
import numpy as np

# booking 데이터셋을 불러와 total review 열의 값 수정
df = pd.read_csv('./datasets/bookings/bookings.csv')
print(df.head())

print("VC")
print(df['Total_Review'].value_counts())
print("Uniq")
print(df['Total_Review'].unique())