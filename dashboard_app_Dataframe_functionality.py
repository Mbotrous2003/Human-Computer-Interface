#Installing required libraries 
#!pip install psycopg2
#!pip install SQLAlchemy
#!pip install streamlit 
#!pip install streamlit-aggrid
#!pip install streamlit_stl


from sqlalchemy import create_engine
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode, GridUpdateMode
from streamlit_stl import stl_from_text, stl_from_file
 

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

def confirm_save(df_name):
        st.session_state[f"{df_name}_original"] = st.session_state[f"{df_name}_edited"].copy() #Save edits
        st.session_state[f"{df_name}_show_confirm"] = False #Hide confirmation
        st.success("Changes saved successfully!")

def cancel_save(df_name):
        st.session_state[f"{df_name}_show_confirm"] = False #Hide confirmation

# Functions to display the data editor and save/cancel buttons
def display_tab(df_name, title):
        initialize_data(df_name) #ensure data state exists
        st.subheader(title)

        # Editable Dataframe
        st.session_state[f"{df_name}_edited"] = st.data_editor(
                st.session_state[f"{df_name}_edited"],
                num_rows="dynamic",
                key=f"editor_{df_name}_{st.session_state[f'{df_name}_key']}"
        )
        
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
        
        # Show the STL model only for Jeep Model 1
        if df_name == "df2":
                st.subheader("3D Model Viewer")
                #referenced https://github.com/Lucandia/streamlit_stl for library and documentation
                #display STL file
                #create 6 columns for color, material, auto rotation, opacity, height, and STL file
                cols = st.columns(5)
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
                # camera position can be used to give the user the ability to change the view of the model
                #cols = st.columns(4)
                #with cols[0]:
                #        cam_v_angle = st.number_input("Camera Vertical Angle", value=60, key='cam_v_angle')
                #with cols[1]:
                #        cam_h_angle = st.number_input("Camera Horizontal Angle", value=-90, key='cam_h_angle')
                #with cols[2]:
                #        cam_distance = st.number_input("Camera Distance", value=0, key='cam_distance')
                #with cols[3]:
                #        max_view_distance = st.number_input("Max view distance", min_value=1, value=1000, key='max_view_distance')

                #sets "selected_jeep_model" variable as the file path of the selected model.
                stl_from_file(  
                file_path= 'JeepModel1.stl', 
                color=color,
                material=material,
                auto_rotate=auto_rotate,
                opacity=opacity,
                height=height,
                shininess=100,
                cam_v_angle=60,
                cam_h_angle=90,
                cam_distance=0,
                max_view_distance=1000,
                key='jeepmodel')


tab_labels = ["Quality Tickets", "Jeep Model 1", "Jeep Model 2", "Jeep Model 3", "Project Management Needs"]

df_names = ["df1", "df2", "df3", "df4", "df5"]

tabs = st.tabs(tab_labels)

#Display all tabs using a loop 
for tab, df_name, title in zip(tabs, df_names, tab_labels):
        with tab:
                display_tab(df_name, title)

# with tab1:
#     st.subheader("Jeep Model 1")
#     # Editable dataframe

#     edited_df1 = st.data_editor(st.session_state.df1_edited, num_rows="dynamic"
#     , key = f"editor_df1_{st.session_state.df1_key}")

#     # Buttons for save and undo
#     if st.session_state.show_confirm:
#                 #display confirmation message 
#         st.warning(" **Once you click save, you can NOT go back.**")

#         col1, col2 = st.columns([1, 1]) 
#         with col1:
#                 st.button("Confirm Save", on_click=confirm_save)
#         with col2:
#                 st.button("Cancel", on_click=cancel_save)

#     else:
#         st.button("Save Changes", on_click=trigger_confirm)
        # with col2:
        #         st.button("Undo Changes", on_click=undo_changes)

#     with col2:
#         st.button("Undo changes", on_click=undo_changes)


                # st.warning("Reverted to last save state")
    # Display saved data; This will show another dataframe right below Jeep Model 1 dataframe so unnecessary unless you saved the current dataframe and want to see your last saved data 
#     st.write("Last Saved Data:")
#     st.dataframe(st.session_state.df1_original)
# with tab2:
#     st.subheader("Jeep Model 2")
#     st.dataframe(df2)

# with tab3:
#     st.subheader("Jeep Model 3")
#     st.dataframe(df3)

# with tab4:
#     st.subheader("PM Needs")
#     st.dataframe(df4)

# with tab5:
#     st.subheader("Quality Tickets")
#     st.dataframe(df5)

#jeep model 1 stl file comes from pritables https://www.printables.com/model/191461-scx24-jeep-wrangler-body/files
#jeep model 2 stl file comes from https://www.printables.com/model/417126-jeep/files
#defines jeep model 1 and jeep model 2 files from file path
# JeepModel1 = 'JeepModel1.stl'
# JeepModel2 = 'JeepModel2.stl'

# <<<<<<< HEAD
# #This is for excel files if needed -- you will use the same method used for the database connection
# # df1 = pd.read_csv('C:/Users/maria/Dashboard/Quality Tickets.csv')

# # df2 = pd.read_csv('C:/Users/maria/Dashboard/PM needs.csv')
# =======
# #Mapping the dropwdown to the file path for jeep models
# options = {
#         "Jeep Model 1": JeepModel1,
#         "Jeep Model 2": JeepModel2
# }

# #referenced https://github.com/Lucandia/streamlit_stl for library and documentation
# #display STL file
# st.subheader("Jeep Model 1")
# #create 6 columns for color, material, auto rotation, opacity, height, and STL file
# cols = st.columns(6)
# with cols[0]:
#         color = st.color_picker("Pick a color", "#FF9900", key='color_file')
# with cols[1]:
#         material = st.selectbox("Select a material", ["material", "flat", "wireframe"], key='material_file')
# with cols[2]:
#         st.write('\n'); st.write('\n')
#         auto_rotate = st.toggle("Auto rotation", key='auto_rotate_file')
# with cols[3]:
#         opacity = st.slider("Opacity", min_value=0.0, max_value=1.0, value=1.0, key='opacity_file')
# with cols[4]:
#         height = st.slider("Height", min_value=50, max_value=1000, value=500, key='height_file')
# #asks user which jeep model they would like to view
# with cols[5]:
#         STLfile = st.selectbox("Select Jeep Model", list(options.keys()))
# >>>>>>> 08b4b263181d5275524ffa84360044b222e247b5

# # df3 = pd.read_csv('C:/Users/maria/Dashboard/Jeep model 1.csv')

# # df4 = pd.read_csv('C:/Users/maria/Dashboard/Jeep model 2.csv')

# # df5 = pd.read_csv('C:/Users/maria/Dashboard/Jeep model 3.csv')

# #sets "selected_jeep_model" variable as the file path of the selected model.
# selected_jeep_model = options[STLfile]
# stl_from_file(  
#     file_path= selected_jeep_model, 
#     color=color,
#     material=material,
#     auto_rotate=auto_rotate,
#     opacity=opacity,
#     height=height,
#     shininess=100,
#     cam_v_angle=cam_v_angle,
#     cam_h_angle=cam_h_angle,
#     cam_distance=cam_distance,
#     max_view_distance=max_view_distance,
#     key='jeepmodel')

# <<<<<<< HEAD
# #----> Section below is for the CAD files for Jeep models 

# # #display STL file for Jeep model CAD file 
# # st.subheader("Jeep Model 1")
# # #create 5 columns for color, material, auto rotation, opacity, and height
# # cols = st.columns(5)
# # with cols[0]:
# #         color = st.color_picker("Pick a color", "#FF9900", key='color_file')
# # with cols[1]:
# #         material = st.selectbox("Select a material", ["material", "flat", "wireframe"], key='material_file')
# # with cols[2]:
# #         st.write('\n'); st.write('\n')
# #         auto_rotate = st.toggle("Auto rotation", key='auto_rotate_file')
# # with cols[3]:
# #         opacity = st.slider("Opacity", min_value=0.0, max_value=1.0, value=1.0, key='opacity_file')
# # with cols[4]:
# #         height = st.slider("Height", min_value=50, max_value=1000, value=500, key='height_file')

# # # camera position can be used to give the user the ability to change the view of the model
# # cols = st.columns(4)
# # with cols[0]:
# #         cam_v_angle = st.number_input("Camera Vertical Angle", value=60, key='cam_v_angle')
# # with cols[1]:
# #         cam_h_angle = st.number_input("Camera Horizontal Angle", value=-90, key='cam_h_angle')
# # with cols[2]:
# #         cam_distance = st.number_input("Camera Distance", value=0, key='cam_distance')
# # with cols[3]:
# #         max_view_distance = st.number_input("Max view distance", min_value=1, value=1000, key='max_view_distance')


# # #upload STL file from file path
# # #referenced https://github.com/Lucandia/streamlit_stl for library and documentation
# # #stl file comes from pritables https://www.printables.com/model/191461-scx24-jeep-wrangler-body/files
# # stl_from_file(  file_path='Jeep_Wrangler.stl', 
# #                 color=color,
# #                 material=material,
# #                 auto_rotate=auto_rotate,
# #                 opacity=opacity,
# #                 height=height,
# #                 shininess=100,
# #                 cam_v_angle=cam_v_angle,
# #                 cam_h_angle=cam_h_angle,
# #                 cam_distance=cam_distance,
# #                 max_view_distance=max_view_distance,
# #                 key='jeepmodel1')
# =======
# #this provides the option to drag and drop a STL file rather than using the ones provided.   
# file_input = st.file_uploader("Or upload a STL file ", type=["stl"])

# cols = st.columns(5)
# with cols[0]:
#     color = st.color_picker("Pick a color", "#0099FF", key='color_text')
# with cols[1]:
#     material = st.selectbox("Select a material", ["material", "flat", "wireframe"], key='material_text')
# with cols[2]:
#     st.write('\n'); st.write('\n')
#     auto_rotate = st.toggle("Auto rotation", key='auto_rotate_text')
# with cols[3]:
#     opacity = st.slider("Opacity", min_value=0.0, max_value=1.0, value=1.0, key='opacity_text')
# with cols[4]:
#     height = st.slider("Height", min_value=50, max_value=1000, value=500, key='height_text')

# cols = st.columns(4)
# with cols[0]:
#     cam_v_angle = st.number_input("Camera Vertical Angle", value=60, key='cam_v_angle_text')
# with cols[1]:
#     cam_h_angle = st.number_input("Camera Horizontal Angle", value=0, key='cam_h_angle_text')
# with cols[2]:
#     cam_distance = st.number_input("Camera Distance", value=0, key='cam_distance_text')
# with cols[3]:
#     max_view_distance = st.number_input("Max view distance", min_value=1, value=1000, key='max_view_distance_text')

# if file_input:
#     stl_from_text(  text=file_input.getvalue(), 
#                     color=color,
#                     material=material,
#                     auto_rotate=auto_rotate,
#                     opacity=opacity,
#                     height=height,
#                     cam_v_angle=cam_v_angle,
#                     cam_h_angle=cam_h_angle,
#                     cam_distance=cam_distance,
#                     max_view_distance=max_view_distance,
#                     key='user-upload')
# >>>>>>> 08b4b263181d5275524ffa84360044b222e247b5
