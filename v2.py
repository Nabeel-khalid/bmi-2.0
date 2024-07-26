import streamlit as st
import math
import streamlit.components.v1 as components

st.set_page_config(page_title="BMI 2.0 Calculator and 3D Visualizer v2", page_icon="🔥")

def calculate_bmi(weight, height):
    return weight / (height / 100) ** 2

def calculate_body_fat_percentage(weight, height, neck, waist, hip, gender, units='metric'):
    if units == 'imperial':
        weight = weight * 0.453592
        height = height * 2.54
        neck = neck * 2.54
        waist = waist * 2.54
        if hip:
            hip = hip * 2.54

    if gender == 'male':
        bfp = 495 / (1.0324 - 0.19077 * math.log10(waist - neck) + 0.15456 * math.log10(height)) - 450
    else:
        bfp = 495 / (1.29579 - 0.35004 * math.log10(waist + hip - neck) + 0.22100 * math.log10(height)) - 450

    return round(bfp, 2)

def main():
    st.title("BMI 2.0 Calculator and 3D Visualizer")

    st.sidebar.header("User Input Parameters")
    
    gender = st.sidebar.selectbox("Select Gender", ["male", "female"])
    units = st.sidebar.selectbox("Select Units", ["metric", "imperial"])
    
    weight = st.sidebar.slider("Weight (kg)", 30.0, 150.0, 70.0)
    height = st.sidebar.slider("Height (cm)", 100.0, 220.0, 170.0)
    neck = st.sidebar.slider("Neck circumference (cm)", 20.0, 60.0, 40.0)
    waist = st.sidebar.slider("Waist circumference (cm)", 40.0, 150.0, 70.0)
    
    hip = None
    if gender == 'female':
        hip = st.sidebar.slider("Hip circumference (cm)", 70.0, 160.0, 100.0)

    if st.sidebar.button("Calculate"):
        bmi = calculate_bmi(weight, height)
        bfp = calculate_body_fat_percentage(weight, height, neck, waist, hip, gender, units)
        
        st.write(f"Calculated BMI: {bmi:.2f}")
        st.write(f"Calculated Body Fat Percentage: {bfp:.2f}%")
        
        # Embed the 3D BMI visualizer
        bmi_visualizer_url = f"https://www.bmivisualizer.com/?gender={gender}&weight={weight}&height={height}"
        st.components.v1.iframe(bmi_visualizer_url, width=550, height=670)

if __name__ == "__main__":
    main()
