from method.getCreditBalance import getCreditBalance
import pandas as pd

df_1, _ = getCreditBalance()

df_1['div'] = df_1['buyBalance']/df_1['sellBalance']
df_1 = df_1[df_1['div'] < 0.5]

print(df_1)

# 株価が上がってて、信用倍率が1未満で下落している銘柄一覧
