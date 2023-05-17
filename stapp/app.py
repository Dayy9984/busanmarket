import io
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import matplotlib.font_manager as fm
from pathlib import Path
import matplotlib.patches as mpatches
font_path = Path('stapp/NanumBarunGothicLight.ttf')
fontprop = fm.FontProperties(fname=font_path, size=10)

st.title("부산 구/동별 상권 시각화")

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

changemap = st.checkbox('지도로 보기')
if changemap:
    gu = list(sorted(set(df_count['시군구명'])))
    select = st.selectbox('시군구명을 선택하세요',gu)
    df_count = df_count.sort_values(by='count', ascending=True)
    df_gu = df_count[df_count['시군구명'] == select]
    
    dong = list(sorted(set(df_gu['행정동명'])))
    select_dong = st.selectbox('행정동명을 선택하세요',dong)
    
    
    
    df_xy = df_sorted_by_values[['시군구명','행정동명','경도','위도']]
    df_gu_xy = df_xy[df_xy['시군구명'] == select]
    
    df_dong_xy = df_gu_xy[df_gu_xy['행정동명'] == select_dong]
    df_dong_xy = df_dong_xy[['경도','위도']]
    df_dong_xy = pd.DataFrame(df_dong_xy)
    df_dong_xy.columns = ['lat', 'lon']
    st.map(df_dong_xy)
    
    
else:
    gu = list(sorted(set(df_count['시군구명'])))
    select = st.selectbox('시군구명을 선택하세요',gu)
    df_count = df_count.sort_values(by='count', ascending=True)
    df_gu = df_count[df_count['시군구명'] == select]

    c = st.color_picker('차트색상선택', '#1f77b4')


    fig, ax = plt.subplots(figsize=(12, 8)) 
    bars = df_gu.plot(kind='bar',legend=False, color=c,ax=ax)  
    ax.set_ylabel("Count",fontproperties=fontprop)   
    ax.set_title(select,fontproperties=fontprop,size=20)  
    for bar in bars.patches:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 0.01, yval, ha='center', va='bottom') 
    ax.set_xticklabels(df_gu['행정동명'], rotation=0,fontproperties=fontprop) 
    st.pyplot(fig)

    fn = select+'_chart.png'
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
       select+"_data.csv",
       "text/csv",
       key='download-csv'
    )



  
       

