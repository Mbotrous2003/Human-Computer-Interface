#Installing required libraries 
#!pip install psycopg2
#!pip install SQLAlchemy
#!pip install streamlit 
#!pip install streamlit-aggrid
#!pip install streamlit_stl ##kareem edit

from sqlalchemy import create_engine
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode, GridUpdateMode
from streamlit_stl import stl_from_file ##kareem edit
 
# Database connection details
user = 'postgres'
password = 'Marina789'
server = 'localhost'
database = 'HCI_requirements'
port = '5433'
 
# Construct the database URL
DATABASE_URL = "postgresql://postgres:Marina789@localhost:5433/HCI_requirements"
 
#Connect to PostgreSQL database
@st.cache_data
def load_data():
    engine = create_engine(DATABASE_URL)
    #Load data from each table into pandas DataFrames
    df_jeep_models = pd.read_sql_query('SELECT * FROM public."Jeep_Models";', engine)
    df_pm_needs = pd.read_sql_query('SELECT * FROM public."PM_Needs";', engine)
    df_quality_tickets = pd.read_sql_query('SELECT * FROM public."Quality_Tickets";', engine)
    return (df_jeep_models, df_pm_needs, df_quality_tickets) #Return the dataframes
#Call function to load the data
df_jeep_models, df_pm_needs, df_quality_tickets = load_data()
 
# Check to see if your output of each table
# print(df_jeep_models.head())
# print(df_pm_needs.head())
# print(df_quality_tickets.head())
 
#Query the database
#df_JeepModels = pd.read_sql_query(JeepModels, engine)
#df_PMNeeds = pd.read_sql_query(PMNeeds, engine)
#df_QualityTickets = pd.read_sql_query(QualityTickets, engine)
#df = pd.read_sql_query(PMNeeds, engine)
#df_JeepModels.head()
#df_PMNeeds.head()
 
# Streamlit layout
st.title("HCI Requirements Dashboard")


 
# Display each dataframe using AgGrid for interactivity
st.subheader("Jeep Models")
AgGrid(df_jeep_models, height=400, update_mode=GridUpdateMode.SELECTION_CHANGED)
 
st.subheader("PM Needs")
AgGrid(df_pm_needs, height=400, update_mode=GridUpdateMode.SELECTION_CHANGED)
 
st.subheader("Quality Tickets")
AgGrid(df_quality_tickets, height=400, update_mode=GridUpdateMode.SELECTION_CHANGED)

#jeep model 1 stl file comes from pritables https://www.printables.com/model/191461-scx24-jeep-wrangler-body/files
#jeep model 2 stl file comes from https://www.printables.com/model/417126-jeep/files
#defines jeep model 1 and jeep model 2 files from file path
JeepModel1 = 'JeepModel1.stl'
JeepModel2 = 'JeepModel2.stl'
#Mapping the dropwdown to the file path for jeep models
options = {
        "Jeep Model 1": JeepModel1,
        "Jeep Model 2": JeepModel2
}

#referenced https://github.com/Lucandia/streamlit_stl for library and documentation
#display STL file
st.subheader("Jeep Model 1")
#create 6 columns for color, material, auto rotation, opacity, height, and STL file
cols = st.columns(6)
with cols[0]:
        color = st.color_picker("Pick a color", "#FF9900", key='color_file')
with cols[1]:
        material = st.selectbox("Select a material", ["material", "flat", "wireframe"], key='material_file')
with cols[2]:
        st.write('\n'); st.write('\n')
        auto_rotate = st.toggle("Auto rotation", key='auto_rotate_file')
with cols[3]:
        opacity = st.slider("Opacity", min_value=0.0, max_value=1.0, value=1.0, key='opacity_file')
with cols[4]:
        height = st.slider("Height", min_value=50, max_value=1000, value=500, key='height_file')
#asks user which jeep model they would like to view
with cols[5]:
        STLfile = st.selectbox("Select Jeep Model", list(options.keys()))

# camera position can be used to give the user the ability to change the view of the model
cols = st.columns(4)
with cols[0]:
        cam_v_angle = st.number_input("Camera Vertical Angle", value=60, key='cam_v_angle')
with cols[1]:
        cam_h_angle = st.number_input("Camera Horizontal Angle", value=-90, key='cam_h_angle')
with cols[2]:
        cam_distance = st.number_input("Camera Distance", value=0, key='cam_distance')
with cols[3]:
        max_view_distance = st.number_input("Max view distance", min_value=1, value=1000, key='max_view_distance')

#sets "selected_jeep_model" variable as the file path of the selected model.
selected_jeep_model = options[STLfile]
stl_from_file(  file_path= selected_jeep_model, 
                color=color,
                material=material,
                auto_rotate=auto_rotate,
                opacity=opacity,
                height=height,
                shininess=100,
                cam_v_angle=cam_v_angle,
                cam_h_angle=cam_h_angle,
                cam_distance=cam_distance,
                max_view_distance=max_view_distance,
                key='jeepmodel')