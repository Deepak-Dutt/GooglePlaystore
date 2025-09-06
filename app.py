import streamlit as st
import pandas as pd
import plotly.express as px

#Load Data
@st.cache_data
def load_data():
    df= pd.read_csv('D:\GooglePlaystore\data\googleplaystore_cleaned.csv')
    return df

df= load_data()

st.set_page_config(page_title= 'Google Play Store Dashboard', layout= 'wide')
st.title('Google Play Store Dashboard')

st.sidebar.header('filter')
selected_category= st.sidebar.multiselect('Select Category', options= df['Category'].unique())
selected_type= st.sidebar.multiselect('Select Type', options= df['Type'].unique())

filtered_df= df.copy()
if selected_category:
    filtered_df= filtered_df[filtered_df['Category'].isin(selected_category)]
if selected_type:
    filtered_df= filtered_df[filtered_df['Type'].isin(selected_type)]


tab1, tab2= st.tabs(['Market Overview', 'Used And Business Insights'])


#Tab 1 - Market Overview:
with tab1:
    st.subheader('Key Metrics')
    c1, c2, c3, c4= st.columns(4)
    c1.metric('Total Apps', len(filtered_df))
    c2.metric('Average Rating', round(filtered_df['Rating'].mean(), 2))
    c3.metric('Total Installs', f'{filtered_df['Installs'].sum():,.0f}')
    c4.metric('Free App %', f"{(filtered_df['Type'].eq('Free').mean()*100):.1f}%")

    #Distrubution of Ratings:
    fig1= px.histogram(filtered_df, x= 'Rating', nbins=20, title= 'Distribution of Ratings')
    st.plotly_chart(fig1, use_container_width= True)

    #Top Categories by App Count:
    top_categories= filtered_df['Category'].value_counts().reset_index()
    fig2= px.bar(top_categories.head(15), x= 'Category', y= 'count', title= 'Top 15 Categories by App count')
    st.plotly_chart(fig2, use_container_width= True)

    #Installs - Top 10 Apps:
    top_installs= filtered_df.sort_values('Installs', ascending= False).head(10)
    fig3= px.bar(top_installs, x= 'App', y='Installs', title= 'Top 10 most installes apps')
    st.plotly_chart(fig3, use_container_width= True)

    #Free vS Paid Apps:
    fig4= px.pie(filtered_df, names='Type', title= 'Free Vs Paid Apps')
    st.plotly_chart(fig4, use_container_width= True)


#Tab 2 - User & Business Insights:
with tab2:
    #Price Distribution:
    paid_apps= filtered_df[filtered_df['Type']=='Paid']
    if not paid_apps.empty:
        fig5= px.histogram(paid_apps, x='Price', nbins=50, title='Price Distribution of Paid Apps')
        st.plotly_chart(fig5, use_container_wigth= True)

    #Content Rating Analysis:
    fig6= px.bar(filtered_df['Content Rating'].value_counts().reset_index(),
                 x= 'Content Rating',
                 y= 'count',
                 title= 'Apps by Content Rating'
                 )
    st.plotly_chart(fig6, use_contaner_width= True)

    #Installs by Content Rating:
    fig7= px.box(filtered_df, x= 'Content Rating', y= 'Installs', title= 'Installs by Content Rating')
    st.plotly_chart(fig7, use_coiontainer_width= True)

    #Genres popularity:
    top_genres= filtered_df['Genres'].value_counts().reset_index()
    fig8= px.bar(top_genres.head(20), x= 'Genres', y= 'count', title= 'Top 20 Genres')
    st.plotly_chart(fig8, use_container_width= True)

    #App Size Vs Rating:
    fig9= px.scatter(filtered_df, x= 'Size', y= 'Rating', title= 'App Size Vs Rating', trendline= 'ols')
    st.plotly_chart(fig9, use_container_width=True)

    #Trends by Last Update:
    if 'Last Updated' in filtered_df.columns:
        fig10= px.histogram(filtered_df, x= 'Year', title= 'Number of Apps Undated pe Year')
        st.plotly_chart(fig10, use_container_width= True)