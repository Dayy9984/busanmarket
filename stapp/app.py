
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from matplotlib import rc
import matplotlib.font_manager as fm
fm._rebuild()
fm.get_fontconfig_fonts()
font_location = 'stapp/NanumBarunGothicLight.ttf' 
font_name = fm.FontProperties(fname=font_location).get_name()
matplotlib.rc('font', family=font_name)

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

gu = list(set(df_count['시군구명']))
select = st.selectbox('시군구명을 선택하세요',gu)
df_count = df_count.sort_values(by='count', ascending=True)
df_gu = df_count[df_count['시군구명'] == select]

fig, ax = plt.subplots(figsize=(10, 6)) 
bars = df_gu.plot(kind='bar',legend=False, ax=ax)  
ax.set_ylabel("Count")   
ax.set_title("강서구청")  
for bar in bars.patches:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 0.01, yval, ha='center', va='bottom') 
ax.set_xticklabels(df_gu['행정동명'], rotation=0) 
st.pyplot(fig)



  
       

