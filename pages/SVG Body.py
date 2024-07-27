import streamlit as st
from streamlit.components.v1 import components

def calculate_bmi(weight, height):
    return weight / (height / 100) ** 2

def get_bmi_category(bmi):
    if bmi < 18.5:
        return 'underweight', '#ADD8E6', underweight_svg
    elif 18.5 <= bmi < 24.9:
        return 'healthy', '#90EE90', healthy_svg
    elif 25 <= bmi < 29.9:
        return 'overweight', '#FFD700', unhealthy_svg
    else:
        return 'obese', '#FF6347', unhealthy_svg

underweight_svg = """
<svg id="underweight" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 400">
  <g fill="#ADD8E6">
    <!-- SVG content for underweight body -->
  </g>
</svg>
"""

healthy_svg = """
<svg id="healthy" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 400">
  <g fill="#90EE90">
    <!-- SVG content for healthy body -->
  </g>
</svg>
"""

unhealthy_svg = """
<svg id="unhealthy" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 400">
  <g fill="#FF6347">
    <!-- SVG content for unhealthy body -->
  </g>
</svg>
"""

# Streamlit app
st.title("BMI 2.0 Calculator and Visualizer")

st.sidebar.header("User Input Parameters")
gender = st.sidebar.selectbox("Select Gender", ["male", "female"])
weight = st.sidebar.slider("Weight (kg)", 30.0, 150.0, 70.0)
height = st.sidebar.slider("Height (cm)", 100.0, 220.0, 170.0)
neck = st.sidebar.slider("Neck circumference (cm)", 20.0, 60.0, 40.0)
waist = st.sidebar.slider("Waist circumference (cm)", 40.0, 150.0, 70.0)

hip = None
if gender == 'female':
    hip = st.sidebar.slider("Hip circumference (cm)", 70.0, 160.0, 100.0)

if st.sidebar.button("Calculate"):
    bmi = calculate_bmi(weight, height)
    category, color, svg_code = get_bmi_category(bmi)
    
    st.write(f"Calculated BMI: {bmi:.2f}")
    st.write(f"BMI Category: {category}")

    # Display SVG
    components.html(svg_code, height=400)
