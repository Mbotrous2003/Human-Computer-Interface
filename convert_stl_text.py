#This script is intended to take an .STL file as an input and output the contents of the file as a CSV file and recreates it back to an STL file to confirm that the csv is accurate. This file can be stored in the PostgreSQL database and displayed in the Streamlit dashboard.
#The script is broken down into three steps:

#Installing required libraries 
#!pip install numpy-stl
#!pip install pandas

import stl
from stl import mesh
import pandas as pd 
import numpy as np
#this segment of code converts stl files to ascii format (STEP 1)

#STEP 1 Converts from Binary STL to ASCII STL 
stl_file_path = "JeepModel1.stl"
your_mesh = mesh.Mesh.from_file(stl_file_path)
# Save as ASCII STL
ascii_stl_path = "JeepModel1_ascii.stl"
your_mesh.save(ascii_stl_path, mode=stl.Mode.ASCII)
print("Converted to ASCII STL!")

# STEP 2: Read ASCII STL as text
with open(ascii_stl_path, "r") as f:
    stl_text = f.readlines()  # Read all lines into a list

# STEP 3: Save STL text to CSV (Each line as a new row)
df = pd.DataFrame(stl_text)  # Convert list of lines to DataFrame
df.to_csv("stl_files.csv", index=False, header=False)  # Save without index/header
print("STL data saved to CSV!")


#Converting back to STL format
# STEP 4: Read CSV and Convert Back to STL
df = pd.read_csv("stl_files.csv", header=None)  # Read CSV without headers
stl_text = "".join(df[0].tolist())  # Join lines back into a single string

# STEP 5: Save the reconstructed STL file
reconstructed_stl_path = "Reconstructed_JeepModel1.stl"
with open(reconstructed_stl_path, "w") as f:
    f.write(stl_text)

print(f"STL file successfully reconstructed: {reconstructed_stl_path}")