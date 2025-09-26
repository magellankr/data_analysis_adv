# %%
import plotly.express as px
import pandas as pd

import plotly.io as pio
# pio.renderers.default = 'notebook' # 또는 'plotly_mimetype' 또는 'plotly_mimetype+notebook'
# 샘플 데이터프레임 생성
df = pd.DataFrame({
    "과일": ["사과", "바나나", "오렌지", "포도"],
    "수량": [10, 15, 7, 12]
})

# 막대 그래프 그리기
fig = px.bar(df, x="과일", y="수량", title="과일별 수량")
fig.show()

# %%
