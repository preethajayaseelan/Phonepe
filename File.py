# Importing Libraries
import pandas as pd
import mysql.connector as mysql
import streamlit as st
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu
from PIL import Image
import streamlit as st
import seaborn as sns



st.set_page_config(page_title= "Phonepe Pulse Data Visualization ",
                   page_icon= "random",
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This dashboard app is created by *Preetha*!
                                        Data has been cloned from Phonepe Pulse Github Repo"""})
mydb = mysql.connect(
  host = "localhost",
  user = "root",
  password = "!Charupree1329",
  database = "phonepey"
)

# Create a new database and use
cursor = mydb.cursor()

SELECT = option_menu(
    menu_title=None,
    options=["Promotion", "Basic insights", "Contact"],
    icons=["bar-chart", "toggles", "at"],
    default_index=2,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "white", "size": "cover"},
        "icon": {"color": "black", "font-size": "20px"},
        "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#6F36AD"},
        "nav-link-selected": {"background-color": "#6F36AD"}
    }

)
video_url = 'https://www.phonepe.com/webstatic/5988/videos/page/home-fast-secure-v3.mp4'

if SELECT == "Promotion":
    st.markdown("[PhonePe Website](https://www.phonepe.com/)", unsafe_allow_html=True)
    # Display the video
    st.video(video_url,format='video/mp4')



        # Replace the following details with your own
name = "Preetha"
mail = "preethajayaseelan@gmail.com"
profile_picture_url = "https://media.licdn.com/dms/image/D5603AQH70XsGiVP9mg/profile-displayphoto-shrink_400_400/0/1705651963675?e=1710979200&v=beta&t=CH0W7N47B0axwoe8KTKyexq1T8sDINnS4mLVGp0d5Oc"  # Replace with the URL of your profile picture
linkedin_url = "https://www.linkedin.com/in/preetha-preethajayaseelan-97b982145/"
github_url = "https://github.com/preethajayaseelan"

# Your Streamlit code...

if SELECT == "Contact":
    col1, col2 = st.columns(2)

    # Display profile picture in the center column
    with col1:
        st.image(profile_picture_url, caption="My Profile Picture", use_column_width=True)

   
    # Right column with personal details
    with col2:
        st.title(name)
        st.title(mail)
        st.subheader("An Aspiring DATA-ANALYST.... !")

        # Social media links
        st.write(f"[LinkedIn]({linkedin_url})")
        st.write(f"[GitHub]({github_url})")






if SELECT == "Basic insights":
    st.title("BASIC INSIGHTS")
    st.write("----")
    st.subheader("Let's know some basic insights about the data")
    options = ["--select--", "Top 10 states based on year and amount of transaction",
               "Least 10 states based on type and amount of transaction",
               "Top 10 mobile brands based on percentage of transaction",
               "Top 10 Registered-users based on States and District(pincode)",
               "Top 10 Districts based on states and amount of transaction",
               "Least 10 Districts based on states and amount of transaction",
               "Least 10 registered-users based on District_Pincode and states",
               "Top 10 transactions_type based on states and transaction_amount"]
    select = st.selectbox("Select the option", options)

    if select == "Top 10 states based on year and amount of transaction":
        cursor.execute("SELECT DISTINCT State, Transaction_amount, Year, Quarter FROM top_transaction ORDER BY transaction_amount DESC LIMIT 10;")
        df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Transaction_amount', 'Year', 'Quarter'])

    # Display data table
        st.write("### Top 10 States based on Year and Amount of Transaction:")
        st.table(df)

        plt.figure(figsize=(12, 8))

        sns.barplot(x='State', y='Transaction_amount', hue='Year', data=df)
        plt.title('Top 10 States based on Year and Amount of Transaction')
        plt.xlabel('State')
        plt.ylabel('Amount of Transaction')
        plt.show()
        st.pyplot(plt.gcf())

    #_______________________________________________________________________________________            
    elif select == "Least 10 states based on type and amount of transaction":
        cursor.execute(
            "SELECT DISTINCT State, Transaction_amount, Year, Quarter FROM top_transaction ORDER BY transaction_amount ASC LIMIT 10;")
        df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Transaction_amount', 'Year', 'Quarter'])
        st.write(df)


        fig = px.bar(df, x='State', y='Transaction_amount', color='Year',
             title='Top 10 States Based on Type and Amount of Transaction',
             labels={'Transaction_amount': 'Transaction Amount'})
        st.plotly_chart(fig)

# Visualize with Seaborn
        plt.figure(figsize=(10, 6))
        sns.barplot(x='State', y='Transaction_amount', hue='Year', data=df)
        plt.title('Top 10 States Based on Type and Amount of Transaction')
        plt.xlabel('State')
        plt.ylabel('Transaction Amount')
        plt.show()
        
    
        

    #_______________________________________________________________________________________            

    elif select == "Top 10 mobile brands based on percentage of transaction":
        cursor.execute(
            "SELECT Brands, AVG(User_Percentage) as Avg_Percentage FROM aggregated_user GROUP BY Brands ORDER BY Avg_Percentage DESC LIMIT 10;")
        df = pd.DataFrame(cursor.fetchall(), columns=['Brands', 'Avg_Percentage'])
        st.write(df)


     # Visualize the data using Plotly Express
        fig = px.bar(df, x='Brands', y='Avg_Percentage', title='Top 10 Mobile Brands Based on Percentage of Transaction')
        st.plotly_chart(fig)

         # Visualize the data using Seaborn
        plt.figure(figsize=(10, 6))
        sns.barplot(x='Brands', y='Avg_Percentage', data=df)
        plt.title('Top 10 Mobile Brands Based on Percentage of Transaction')
        plt.xlabel('Mobile Brands')
        plt.ylabel('Average Percentage')
        st.pyplot(plt)
    
    #_______________________________________________________________________________________

    elif select == "Top 10 Registered-users based on States and District(pincode)":
        
        cursor.execute("""SELECT State, District_Pincode, SUM(Registered_User) as Total_Registered_Users FROM top_user GROUP BY State, District_Pincode ORDER BY State, Total_Registered_Users DESC LIMIT 10;""")
    
    # Fetch data and create a DataFrame
        df = pd.DataFrame(cursor.fetchall(), columns=['State', 'District_Pincode', 'Total_Registered_Users'])

        col1,col2 = st.columns(2)

        with col1:
            st.write(df)
        with col2:
            st.subheader("Top 10 Registered-users based on States and District(pincode)")
            fig=px.bar(df,x="State",y="Total_Registered_Users")
            tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
            with tab1:
                st.plotly_chart(fig, theme="streamlit", use_container_width=True)
            with tab2:
                st.plotly_chart(fig, theme=None, use_container_width=True)
    #_______________________________________________________________________________________
    elif select == "Top 10 Districts based on states and amount of transaction":
        cursor.execute("SELECT DISTINCT State, District, Transaction_Amount FROM map_transaction ORDER BY Transaction_Amount DESC LIMIT 10;")
        df = pd.DataFrame(cursor.fetchall(), columns=['State', 'District', 'Transaction_amount'])
        st.table(df)

    # Visualization with Plotly Express
        st.title("Top 10 Districts based on states and amount of transaction")
        
        fig_px = px.bar(df, x='State', y='Transaction_amount', title="Top 10 Districts based on states and amount of transaction ",
                        
                        labels={'Transaction_amount': 'Transaction Amount'})
        st.plotly_chart(fig_px, use_container_width=True)
    #_______________________________________________________________________________________
    elif select == "Least 10 Districts based on states and amount of transaction":
        cursor.execute(
            "SELECT DISTINCT State,District,Transaction_Amount FROM map_transaction ORDER BY Transaction_Amount ASC LIMIT 10")
        df = pd.DataFrame(cursor.fetchall(), columns=['State', 'District', 'Transaction_amount'])
        col1, col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Least 10 Districts based on states and amount of transaction")
            fig = px.scatter(df, x="State", y="Transaction_amount")
            tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
            with tab1:
                st.plotly_chart(fig, theme="streamlit", use_container_width=True)
            with tab2:
                st.plotly_chart(fig, theme=None, use_container_width=True)
    #_______________________________________________________________________________________
    elif select == "Least 10 registered-users based on District_Pincode and states":
        cursor.execute(
            "SELECT DISTINCT State,District_Pincode,Registered_User FROM top_user ORDER BY Registered_User ASC LIMIT 10 ;")
        df = pd.DataFrame(cursor.fetchall(), columns=['State', 'District_Pincode', 'Registered_User'])
       # Streamlit layout
        col1, col2 = st.columns(2)

         # Visualization with Plotly Express
        with col1:
            st.write(df)
    
        with col2:
            st.title("Least 10 registered-users based on Districts and states")

        # Plotly Bar Chart
            fig = px.bar(df, x="State", y="Registered_User", title="Plotly Bar Chart")
            st.plotly_chart(fig, use_container_width=True)

       
        # Seaborn Pair Plot
            pair_plot = sns.pairplot(df, hue='State')
            st.pyplot(pair_plot)

        # Plotly Scatter Plot
            fig_scatter = px.scatter(df, x='District_Pincode', y='Registered_User', color='State', title="Plotly Scatter Plot")
            st.plotly_chart(fig_scatter, use_container_width=True)
    #_______________________________________________________________________________________
    elif select == "Top 10 transactions_type based on states and transaction_amount":
        cursor.execute(
            "SELECT DISTINCT State,Transaction_type,Transaction_amount FROM aggregated_transaction ORDER BY Transaction_amount DESC LIMIT 10;")
        df = pd.DataFrame(cursor.fetchall(), columns=['State', 'Transaction_type', 'Transaction_amount'])
        
        col1, col2 = st.columns(2)
        with col1:
           st.write(df)
        with col2:
            # Simple Bar Chart
            st.title("Top 10 transactions_type based on states and transaction_amount")
            fig = px.bar(df, x="State", y="Transaction_amount", color="Transaction_type", title="Top 10 transactions_type based on states and transaction_amount")
            st.plotly_chart(fig, use_container_width=True)
#_______________________________________________________________________________________

