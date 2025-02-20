import streamlit as st  # type: ignore
import pandas as pd
import numpy as np
st.title("Hello World!")

with st.sidebar:
    st.header("About app")
    st.write("This is my first app")

st.header("This is a header with a divider", divider="rainbow")

st.markdown("This is created using st.markdown")

#To adjust app layout 
col1, col2 = st.columns(2)

with col1:
    x = st.slider("Choose an x value", 1, 10)
with col2:
    st.write("The value of :blue[***x***] is ", x)

st.subheader("st.area_chart")
chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
st.area_chart(chart_data)
