import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime

st.set_page_config(layout = "wide",page_title= "Startup Analysis")
df = pd.read_csv("startup_cleaned.csv")
df["date"]= pd.to_datetime(df["date"],errors= "coerce")
df["year"]= df["date"].dt.year
df["month"]= df["date"].dt.month

def load_overal_analysis():
    st.title("Overal Analysis")
    total= round(df["amount"].sum())
    max_funding= round(df.groupby("startup")["amount"].max().sort_values(ascending= False).head(1).values[0])
    average= round(df.groupby("startup")["amount"].sum().mean())
    total_startup= df["startup"].nunique()

    col1, col2, col3, col4= st.columns(4)
    with col1 :
        st.metric("Total",str(total)+"Cr")
    with col2 :
        st.metric("Max",str(max_funding)+"Cr")
    with col3 :
        st.metric("Average",str(average)+"Cr")
    with col4 :
        st.metric("Total_Startup",str(total_startup))

    st.header("Month On Month Graph")
    selected_option= st.selectbox("Select Type",["Total","Count"])
    if selected_option == "Total" :
        tem_df= df.groupby(["year","month"])["amount"].sum().reset_index()
        tem_df["x-axis"]= tem_df["month"].astype("str")+ "-" + tem_df["year"].astype("str")
        fig6, ax6= plt.subplots()
        ax6.plot(tem_df["x-axis"],tem_df["amount"])
        st.pyplot(fig6)
    else :
        tem_df= df.groupby(["year","month"])["startup"].count().reset_index()
        tem_df["x-axis"]= tem_df["month"].astype("str")+ "-" + tem_df["year"].astype("str")
        fig7, ax7= plt.subplots()
        ax7.plot(tem_df["x-axis"],tem_df["startup"])
        st.pyplot(fig7)

    st.header("Courses Offered")
    st.subheader("Data Science and Machine Learning")
    st.subheader('Data Analysis')
    st.subheader("Python")
    st.subheader("I Love You")
    st.subheader("I Will Complete Many Things in Dashain Vacation Holiday")
    st.subheader("This is commited in hi hello how are you 1st")
    st.subheader("This is commited in master 2nd")
    
    st.subheader("This is the 1st commit in sidebar")
    st.subheader("This is the 2nd commit in sidebar")
    st.subheader("This is the  i love you commit in sidebar")
   


def load_investor_details(investor):
    st.title(investor)
    # Most Recent 5 investment of the investors
    last_5_df= df[df["investors"].str.contains(investor)].head(5)[["date","startup","vertical","city","round","amount"]]
    st.subheader("Most Recent Invesment")
    st.dataframe(last_5_df)
    
    # Biggest investment 
    st.subheader("Top 5 Biggest Investment")
    big_investment_series= df[df["investors"].str.contains(investor)].groupby("startup")["amount"].sum().sort_values(ascending= False).head()
    fig,ax = plt.subplots()
    ax.bar(big_investment_series.index,big_investment_series.values)
    st.pyplot(fig)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Stages Invested In")
        vertical_series= df[df["investors"].str.contains(investor)].groupby("round")["amount"].sum()
        fig1, ax1= plt.subplots()
        ax1.pie(vertical_series, labels= vertical_series.index, autopct= "%0.01f%%")
        st.pyplot(fig1)
        

    with col2 :
        st.subheader("Sectors Invested In")
        vertical_series= df[df["investors"].str.contains(investor)].groupby("vertical")["amount"].sum()
        fig1, ax1= plt.subplots()
        ax1.pie(vertical_series, labels= vertical_series.index, autopct= "%0.01f%%")
        st.pyplot(fig1)

    with col3 :
        st.subheader("Cities Invested In")
        vertical_series= df[df["investors"].str.contains(investor)].groupby("city")["amount"].sum()
        fig1, ax1= plt.subplots()
        ax1.pie(vertical_series, labels= vertical_series.index, autopct= "%0.01f%%")
        st.pyplot(fig1)

    # YOY investment graph
    st.subheader("Year On Year Investment Graph")
    # df1= df.dropna(subset=["date"])
    
    YOY_series= df[df["investors"].str.contains(investor)].groupby("year")["amount"].sum()
    fig3,ax3= plt.subplots()
    ax3.plot(YOY_series.index,YOY_series.values)
    st.pyplot(fig3)
        


st.sidebar.title("Startup Funding Analysis")
option = st.sidebar.selectbox("Select One",["Overal Analysis","StartUp","Investor"])

if option == "Overal Analysis" :
   load_overal_analysis()
elif option == "StartUp" :
    st.sidebar.selectbox("Select StartUp",sorted(df["startup"].unique().tolist()))
    st.title("StartUp Analysis")
    btn1 = st.sidebar.button("Find StartUp Details")
else :
    selected_investor = st.sidebar.selectbox("Select Investor",sorted(set(df["investors"].str.split(",").sum())))
    
    btn2 = st.sidebar.button("Find Investor Details")
    if btn2 :
        load_investor_details(selected_investor)


