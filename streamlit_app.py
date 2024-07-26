import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math

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

def plot_body_fat_categories(height, neck, waist, hip, gender, user_weight, user_bfp, units='metric'):
    weights = np.linspace(40, 150, 300)
    bfp_values = [calculate_body_fat_percentage(weight, height, neck, waist, hip, gender, units) for weight in weights]

    plt.figure(figsize=(12, 6))
    plt.plot(weights, bfp_values, label='Body Fat %')

    if gender == 'male':
        plt.fill_between(weights, 0, 6, color='blue', alpha=0.3, label='Essential fat')
        plt.fill_between(weights, 6, 14, color='green', alpha=0.3, label='Athletes')
        plt.fill_between(weights, 14, 18, color='yellow', alpha=0.3, label='Fitness')
        plt.fill_between(weights, 18, 25, color='orange', alpha=0.3, label='Average')
        plt.fill_between(weights, 25, max(bfp_values), color='red', alpha=0.3, label='Obese')
    else:
        plt.fill_between(weights, 0, 13, color='blue', alpha=0.3, label='Essential fat')
        plt.fill_between(weights, 13, 21, color='green', alpha=0.3, label='Athletes')
        plt.fill_between(weights, 21, 25, color='yellow', alpha=0.3, label='Fitness')
        plt.fill_between(weights, 25, 32, color='orange', alpha=0.3, label='Average')
        plt.fill_between(weights, 32, max(bfp_values), color='red', alpha=0.3, label='Obese')

    plt.scatter([user_weight], [user_bfp], color='black', zorder=5)
    plt.text(user_weight, user_bfp, f' {user_bfp}%', fontsize=12, verticalalignment='bottom')

    plt.title('Body Fat Percentage Categories')
    plt.xlabel('Weight (kg)')
    plt.ylabel('Body Fat %')
    plt.legend(loc='upper left')
    plt.grid(True)
    st.pyplot(plt)

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
        
        plot_body_fat_categories(height, neck, waist, hip, gender, weight, bfp, units)
        
        # Placeholder for 3D model update
        st.write(f"Updating 3D model for a {gender} with BMI: {bmi:.2f}")
        st.write("3D Model would be displayed here based on the calculated BMI.")
        # st.components.v1.iframe("URL_TO_3D_MODEL")

if __name__ == "__main__":
    main()
