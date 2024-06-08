import pandas as pd
import json
import matplotlib.pyplot as plt
import numpy as np

file_path = 'result.json'
with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

messages = data['messages']
df = pd.DataFrame(messages)

df['date'] = pd.to_datetime(df['date'])

# Построение графиков
plt.figure(figsize=(9, 8))

# Количество сообщений за каждый год
plt.subplot(2,2,1)

df['year'] = df['date'].dt.year
messages_per_year = df['year'].value_counts().sort_index()

plt.grid(alpha=0.2)
plt.bar(messages_per_year.index, messages_per_year.values, 
        color='grey', alpha=0.5)
plt.plot(messages_per_year.index, messages_per_year.values, 
         color='grey', markersize=3, marker='o')

plt.title('Динамика количества сообщений по годам', 
          fontsize=10, fontfamily='serif', fontweight='bold')
plt.ylabel('Количество сообщений в год', fontsize=9, fontfamily='serif')
plt.xticks(fontsize=7, fontfamily='serif')
plt.yticks(fontsize=8, fontfamily='serif')

# Активность по месяцам и годам - тепловая карта
plt.subplot(2,2,2)

df['month'] = df['date'].dt.strftime('%B')
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
               'July', 'August', 'September', 'October', 'November', 'December'][::-1]
df_pcolor = df.groupby('year')['month'].value_counts().unstack().fillna(0)[month_order].T

plt.pcolor(df_pcolor, cmap='bone_r', edgecolors='white', linewidths=2) # heatmap
plt.xticks(np.arange(0.5, len(df_pcolor.columns), 1), df_pcolor.columns, 
           fontsize=7, fontfamily='serif')
plt.yticks(np.arange(0.5, len(df_pcolor.index), 1), df_pcolor.index, 
           fontsize=7, fontfamily='serif')

plt.title('Распределение активности по месяцам и годам', 
          fontsize=10, fontfamily='serif', fontweight='bold')
cbar = plt.colorbar()
cbar.ax.tick_params(labelsize=8) 
cbar.ax.minorticks_on()

# Активность в течение суток в 2024 году
plt.subplot(2,1,2)

messages_2024 = df.loc[df['year']==2024].copy()
messages_2024['hour'] = messages_2024['date'].dt.hour
messages_2024_per_hour = messages_2024['hour'].value_counts().sort_index()

plt.grid(alpha=0.2)
plt.plot(messages_2024_per_hour.index, messages_2024_per_hour.values, color='grey')

plt.title('Динамика активности в течение суток в 2024 году', 
          fontsize=10, fontfamily='serif', fontweight='bold')
plt.xlabel('Час', fontsize=9, fontfamily='serif')
plt.ylabel('Количество сообщений в час', fontsize=9, fontfamily='serif')
plt.xticks(range(0, 24), fontsize=7, fontfamily='serif')
plt.yticks(fontsize=8, fontfamily='serif')

plt.tight_layout()
plt.show()
