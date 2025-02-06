#This script is intended to take an .STL file as an input and out the contents of the file as a CSV file. This file can be stored in the PostgreSQL database and displayed in the Streamlit dashboard.
#The script is broken down into two steps:

#Installing required libraries 
#!pip install numpy-stl
#pip install pandas

import stl
from stl import mesh
import pandas as pd 
#this segment of code vonerts stl files to ascii format (STEP 1)
# Load the binary STL file
#stl_file_path = "JeepModel1.stl"
#your_mesh = mesh.Mesh.from_file(stl_file_path)
# Save as ASCII STL
#ascii_stl_path = "JeepModel1_ascii.stl"
#your_mesh.save(ascii_stl_path, mode=stl.Mode.ASCII)
#print("Converted to ASCII STL!")

#prints contents of ascii stl to strings (STEP 2)
with open("JeepModel1_ascii.stl", "r") as f:
    stl_text = f.read()

print(stl_text[:500])  # Print first 500 characters

#Reads string and converts to CSV 
# Create a DataFrame with the STL text
df = pd.DataFrame({"File Name": ["JeepModel1"], "STL Content": [stl_text]})

# Save to a CSV file
df.to_csv("stl_files.csv", index=False)

print("STL data saved to CSV!")