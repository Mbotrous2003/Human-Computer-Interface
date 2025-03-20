#Installing required libraries 
#!pip install psycopg2
#!pip install SQLAlchemy
#!pip install streamlit 
#!pip install streamlit-aggrid
#!pip install streamlit_stl
#!pip install streamlit-pdf-viewer




from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode, GridUpdateMode
import matplotlib.pyplot as plt
import plotly.express as px

 

#Give the page a name
st.set_page_config(page_title="Requirements Tracking", layout="wide")

#Title name of the page
st.title("Jeep Model Requirements")

#Connect to the database 
user = 'postgres'
password = 'Marina789'
server = 'localhost'
database = 'HCI_requirements'
port = '5433'
 
# Construct the database URL
DATABASE_URL = "postgresql://postgres:Marina789@localhost:5433/HCI_requirements"
engine = create_engine(DATABASE_URL)
#Connect to PostgreSQL database
@st.cache_data
def load_data():
    engine = create_engine(DATABASE_URL)
    #Load data from each table into pandas DataFrames
    df_jeep_model1 = pd.read_sql_query('SELECT * FROM public."Jeep Model 1";', engine)
    df_jeep_model2 = pd.read_sql_query('SELECT * FROM public."Jeep Model 2";', engine)
    df_jeep_model3 = pd.read_sql_query('SELECT * FROM public."Jeep Model 3";', engine)    
    df_pm_needs = pd.read_sql_query('SELECT * FROM public."PM Needs";', engine)
    df_quality_tickets = pd.read_sql_query('SELECT * FROM public."Quality Tickets";', engine)
    return (df_jeep_model1, df_jeep_model2, df_jeep_model3, df_pm_needs, df_quality_tickets) #Return the dataframes
    
#Call function to load the data

df_jeep_model1, df_jeep_model2, df_jeep_model3, df_pm_needs, df_quality_tickets = load_data()

df1 = df_quality_tickets

df2 = df_jeep_model1

df3 = df_jeep_model2

df4= df_jeep_model3

df5= df_pm_needs
 
# Create Tabs 
# tab1, tab2, tab3, tab4, tab5 = st.tabs(["Quality Tickets", "Jeep Model 1", "Jeep Model 2", "Jeep Model 3", "Project Management Needs"])


# Initializing state for all my dataframes 

def initialize_data(df_name):

        if df_name =="df1": 
                default_data = df_quality_tickets
        elif df_name == "df2":
                default_data = df_jeep_model1

        elif df_name == "df3":
                default_data = df_jeep_model2

        elif df_name == "df4":
                default_data = df_jeep_model3
        
        elif df_name == "df5":
                default_data = df_pm_needs

        if f"{df_name}_original" not in st.session_state:
                st.session_state[f"{df_name}_original"] = default_data.copy()
                st.session_state[f"{df_name}_edited"] = default_data.copy()       
                st.session_state[f"{df_name}_key"] = 0

        if f"{df_name}_show_confirm" not in st.session_state:
                st.session_state[f"{df_name}_show_confirm"] = False # For confirmation dialog

#Define functions for button actions 
def trigger_confirm(df_name):
        st.session_state[f"{df_name}_show_confirm"] = True # Show confirmation message

# The section below creates a connection to the database to save changes back to postgreSQL
     
def confirm_save(df_name):
    edited_data = st.session_state.get(f"{df_name}_edited")  # Use .get() to avoid errors
    if edited_data is None or edited_data.empty:
        st.warning("No changes detected.")
        return

    with engine.connect() as connection:
        with connection.begin():  # Use explicit transaction
            for index, row in edited_data.iterrows():
                query = text('''
                    UPDATE "Quality Tickets"
                    SET "Dealership" = :Dealership, 
                        "Date" = :Date,
                        "Model" = :Model,
                        "Text" = :Text
                    WHERE id = :id;
                ''')

                # Convert NaN to None and ensure 'id' is an integer
                params = {
                    "Dealership": None if pd.isna(row["Dealership"]) else row["Dealership"],
                    "Date": None if pd.isna(row["Date"]) else row["Date"],
                    "Model": None if pd.isna(row["Model"]) else row["Model"],
                    "Text": None if pd.isna(row["Text"]) else row["Text"],
                    "id": int(row["id"])  # Ensure 'id' is an integer
                }

                connection.execute(query, params)  # Execute the update

    st.session_state[f"{df_name}_original"] = edited_data.copy()  # Save edits
    st.session_state[f"{df_name}_show_confirm"] = False  # Hide confirmation
    st.success("Changes saved successfully to the database")
def cancel_save(df_name):
        st.session_state[f"{df_name}_show_confirm"] = False #Hide confirmation

# Functions to display the data editor and save/cancel buttons
def display_tab(df_name, title):
        initialize_data(df_name) #ensure data state exists
        st.subheader(title)
        col1, col2 = st.columns([2,1])

        with col1:
        # Editable Dataframe
                st.session_state[f"{df_name}_edited"] = st.data_editor(
                        st.session_state[f"{df_name}_edited"],
                        num_rows="dynamic",
                        key=f"editor_{df_name}_{st.session_state[f'{df_name}_key']}",
                        column_config={
                        "Met requirements based on tickets": st.column_config.CheckboxColumn(
                                "Requirements met",
                                help = "Select your **completed** jeep models",
                                default=False
                        )
                        },
                        hide_index=True,
                )
        with col2:
                if "Met requirements based on tickets" in st.session_state[f"{df_name}_edited"].columns:
                # Count checked (True) and unchecked (False) values for the "Met requirements based on tickets" column
                        checked_count = st.session_state[f"{df_name}_edited"]['Met requirements based on tickets'].sum()  # Count checked (True) boxes
                        unchecked_count = len(st.session_state[f"{df_name}_edited"]) - checked_count  # Count unchecked (False) boxes

                        # Prepare data for pie chart
                        pie_data = {
                        "Status": ["Checked", "Unchecked"],
                        "Count": [checked_count, unchecked_count]
                        }

                        # Convert to DataFrame for pie chart plotting
                        pie_df = pd.DataFrame(pie_data)

                        # Create Pie chart
                        fig = px.pie(pie_df, values='Count', names='Status', title=f"Met Requirements Based on Tickets for {title}")
                        st.plotly_chart(fig, use_container_width=True)
                else:
                        st.warning("The column 'Met requirements based on tickets' was not found in the dataframe.")

       
        # Show confirmation message when saving
        if st.session_state[f"{df_name}_show_confirm"]:
                st.warning("**Once you click Save, you can NOT go back.**")
                col1, col2 = st.columns([1, 1])
                with col1:
                        st.button("Confirm Save", on_click=confirm_save, args=(df_name,), key=f"confirm_{df_name}")
                with col2:
                        st.button("Cancel", on_click=cancel_save, args=(df_name,), key=f"cancel_{df_name}")
        else:
                st.button("Save Changes", on_click=trigger_confirm, args=(df_name,), key=f"save_{df_name}")
