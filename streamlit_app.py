import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import math

st.title("BMI 2.0 Calculator")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

def calculate_body_fat_percentage(weight, height, neck, waist, hip, gender, units='metric'):
    # Convert measurements to metric if they are in imperial units
    if units == 'imperial':
        weight = weight * 0.453592
        height = height * 2.54
        neck = neck * 2.54
        waist = waist * 2.54
        if hip:
            hip = hip * 2.54

    if gender == 'male':
        # BFP calculation for men (metric)
        bfp = 495 / (1.0324 - 0.19077 * math.log10(waist - neck) + 0.15456 * math.log10(height)) - 450
    else:
        # BFP calculation for women (metric)
        bfp = 495 / (1.29579 - 0.35004 * math.log10(waist + hip - neck) + 0.22100 * math.log10(height)) - 450

    return round(bfp, 2)

def plot_body_fat_categories(height, neck, waist, hip, gender, user_weight, user_bfp, units='metric'):
    weights = np.linspace(40, 150, 300)  # Range of weights
    bfp_values = [calculate_body_fat_percentage(weight, height, neck, waist, hip, gender, units) for weight in weights]

    plt.figure(figsize=(12, 6))

    # Plot Body Fat Percentage values
    plt.plot(weights, bfp_values, label='Body Fat %')

    # Define categories
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

    # Plot user's Body Fat Percentage
    plt.scatter([user_weight], [user_bfp], color='black', zorder=5)
    plt.text(user_weight, user_bfp, f' {user_bfp}%', fontsize=12, verticalalignment='bottom')

    plt.title('Body Fat Percentage Categories')
    plt.xlabel('Weight (kg)')
    plt.ylabel('Body Fat %')
    plt.legend(loc='upper left')
    plt.grid(True)
    st.pyplot(plt)

def main():
    st.title("BMI 2.0 Calculator")
    
    gender = st.selectbox("Select Gender", ["male", "female"])
    units = st.selectbox("Select Units", ["metric", "imperial"])
    
    weight = st.number_input("Enter weight:", min_value=1.0)
    height = st.number_input("Enter height:", min_value=1.0)
    neck = st.number_input("Enter neck size:", min_value=1.0)
    waist = st.number_input("Enter waist size:", min_value=1.0)
    
    hip = None
    if gender == 'female':
        hip = st.number_input("Enter hip size:", min_value=1.0)

    if st.button("Calculate"):
        bfp = calculate_body_fat_percentage(weight, height, neck, waist, hip, gender, units)
        st.write(f"Your Body Fat Percentage is: {bfp}%")
        
        # Plot the Body Fat Percentage categories and user's BFP
        plot_body_fat_categories(height, neck, waist, hip, gender, weight, bfp, units)

if __name__ == "__main__":
    main()
