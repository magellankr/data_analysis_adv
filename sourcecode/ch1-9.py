import seaborn as sns

df = sns.load_dataset('penguins')
df.head()
print(df.head())

# query 메서드를 이용한 부등호 필터링
x = df.query('bill_length_mm > 55')
print(x.head())
