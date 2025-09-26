# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import linregress

print(pd.__version__)
s = pd.Series([1, 2, 3, np.nan, np.nan, 6, 7, np.nan, np.nan])
print(s)

# interpolation 메서드를 이용한 결측치 내삽
print(s.interpolate(
    method="spline", order=1, limit_direction="forward", limit=2
))

s.interpolate(method="linear", limit_direction="forward", limit=3)

# %%
