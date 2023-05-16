import io
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import matplotlib.font_manager as fm
from pathlib import Path
import matplotlib.patches as mpatches
font_path = Path('stapp/NanumBarunGothicLight.ttf')
fontprop = fm.FontProperties(fname=font_path, size=10)

st.title("부산 구/동별 상권 그래프")

df = pd.read_csv('stapp/busan.csv')
df_sorted_by_values = df.sort_values(by='시군구명')
df_sorted_by_values = df_sorted_by_values.sort_values(by='행정동명')
df_s = df_sorted_by_values[['시군구명','행정동명']]
df_s = df_s[['시군구명','행정동명']]
df_s = df_s.groupby(['시군구명','행정동명'])
df_count = df_s['행정동명'].value_counts()

df_count = df_count.reset_index()
df_count.columns = ['시군구명','행정동명', 'count']
df_count = pd.DataFrame(df_count)

gu = list(sorted(set(df_count['시군구명'])))
select = st.selectbox('시군구명을 선택하세요',gu)
df_count = df_count.sort_values(by='count', ascending=True)
df_gu = df_count[df_count['시군구명'] == select]

c = st.color_picker('차트색상선택', '#1f77b4')


fig, ax = plt.subplots(figsize=(10, 6)) 
bars = df_gu.plot(kind='bar',legend=False, color=c,ax=ax)  
ax.set_ylabel("Count")   
ax.set_title(select,fontproperties=fontprop)  
for bar in bars.patches:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 0.01, yval, ha='center', va='bottom') 
ax.set_xticklabels(df_gu['행정동명'], rotation=0,fontproperties=fontprop) 
st.pyplot(fig)

fn = select+'chart.png'
img = io.BytesIO()
plt.savefig(img, format='png')
 
btn = st.download_button(
   label="차트 image 다운로드",
   data=img,
   file_name=fn,
   mime="image/png"
)

def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')
csv = convert_df(df_gu)
st.download_button(
   "현재 data.csv 다운로드",
   csv,
   select+"data.csv",
   "text/csv",
   key='download-csv'
)


  
       

