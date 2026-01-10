import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit import dataframe

st.set_page_config(layout='wide', page_title='Startup&Funding Analysis')

df = pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'], errors='coerce')


def load_overall_analysis():
    st.title('Overall Analysis')
    # total invested amount
    total = round(df['amount'].sum())
    #max amount infused in a startup
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    #avg ticket size
    avg_funding = df.groupby('startup')['amount'].sum().mean()
    #total funded startups
    num_startup = df['startup'].nunique()

    col1,col2,col3,col4 = st.columns(4)
    with col1:
        st.metric('Total', str(total) + ' Cr')
    with col2:
        st.metric('Maximum Funding', str(max_funding) + ' Cr')
    with col3:
        st.metric('Average Funding', str(round(avg_funding)) + ' Cr')
    with col4:
        st.metric('Number of Startups', str(num_startup))

    st.header('MoM graph')
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df.dropna(subset=['year'], inplace=True)


    temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()



    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
    fig3, ax3 = plt.subplots()
    ax3.plot(temp_df['x_axis'],temp_df['amount'])
    st.pyplot(fig3)



def load_investor_details(investor):
    st.title(investor)
    #load the recent 5 investment of the investor
    last_5df = df[df['investor'].str.contains(investor)].head()[['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.subheader('most recent investment ')
    st.dataframe(last_5df)

    col1, col2 = st.columns(2)
    with col1:
        # biggest investment
        big_series = df[df['investor'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(
            ascending=False).head()
        if big_series.empty:
            st.warning('No Investor Found')
        else:
            st.subheader('Biggest investment ')
            fig, ax = plt.subplots()
            ax.bar(big_series.index, big_series.values)
            st.pyplot(fig)

    with col2:
        vertical_series= df[df['investor'].str.contains(investor)].groupby('vertical')['amount'].sum()
        vertical_series= vertical_series[vertical_series>0]
        if vertical_series.empty:
            st.warning('No Sector investment Found')
        else:
            st.subheader('Sectors invested in')
            fig1, ax1 = plt.subplots()
            ax1.pie(vertical_series.values, labels=vertical_series.index, autopct='%1.1f%%')
            st.pyplot(fig1)


    col3, col4 = st.columns(2)
    with col3:
        round_series=df[df['investor'].str.contains(investor)].groupby('round')['amount'].sum()
        round_series= round_series[round_series>0]
        if round_series.empty:
            st.warning('No round-wise investment found')
        else:
            st.subheader('Round investment ')
            fig2, ax2 = plt.subplots()
            ax2.pie(round_series.values, labels=round_series.index, autopct='%1.1f%%')
            st.pyplot(fig2)

    with col4:
        city_series =df[df['investor'].str.contains(investor)].groupby('city')['amount'].sum()
        city_series= city_series[city_series>0]
        if city_series.empty:
            st.warning('No city-wise data found')
        else:
            st.subheader('City investment ')
            fig3, ax3 = plt.subplots()
            ax3.pie(city_series.values, labels=city_series.index, autopct='%1.1f%%')
            st.pyplot(fig3)

    df['date'] = pd.to_datetime(df['date'],errors='coerce')
    df['year'] = df['date'].dt.year
    col5, col6 = st.columns(2)
    with col5:
        year_series=df[df['investor'].str.contains(investor)].groupby('year')['amount'].sum()
        year_series= year_series[year_series>0]
        if year_series.empty:
            st.warning('No year-wise data found')
        else:
            st.subheader('Year-wise investment ')
            fig4, ax4 = plt.subplots()
            ax4.plot( year_series.values, label=year_series.index)
            st.pyplot(fig4)

    inv_df = df[df['investor'].str.contains(investor, case=False)]
    top_verticals = inv_df['vertical'].value_counts().head().index
    top_rounds = inv_df['round'].value_counts().head().index
    year_min = inv_df['year'].min()
    year_max = inv_df['year'].max()
    with col6:
        similar_df = df[
            (df['vertical'].isin(top_verticals)) &
            (df['round'].isin(top_rounds)) &
            (df['year'].between(year_min, year_max)) &
            (~df['investor'].str.contains(investor, case=False))
            ]
        if similar_df.empty:
            st.warning('No similar investment found')
        else:
            st.subheader('Similar investment ')
            st.dataframe(similar_df.head())


st.sidebar.title('Startup funding analysis')
option = st.sidebar.selectbox('Select One',['Overall Analysis', 'Startup', 'Investors'])


if option == 'Overall Analysis':
    btn0 = st.sidebar.button('Show Overall Analysis')
    if btn0:
        load_overall_analysis()
elif option == 'Startup':
    st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find startup Details')
    st.title('Startup Analysis')
else:
    selected_investor = st.sidebar.selectbox('Select Startup',sorted(set(df['investor'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)







