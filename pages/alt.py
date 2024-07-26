import streamlit as st
import math
import streamlit.components.v1 as components

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
    st.set_page_config(page_title="BMI 2.0 Calculator and 3D Visualizer", page_icon="🫠")
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
        
        # Embed the 3D BMI visualizer canvas with dynamic inputs
        html_code = f"""
        <div id="body_viewer">
            <canvas id="bmiCanvas" width="550" height="670"></canvas>
            <script>
                var canvas = document.getElementById('bmiCanvas');
                var context = canvas.getContext('2d');
                var img = new Image();
                img.src = 'https://www.bmivisualizer.com/body_viewer.png';  // Use a static image for demonstration
                img.onload = function() {{
                    context.drawImage(img, 0, 0, canvas.width, canvas.height);
                }};
                function updateCanvas() {{
                    // This is a placeholder for the actual 3D rendering logic
                    context.clearRect(0, 0, canvas.width, canvas.height);
                    context.drawImage(img, 0, 0, canvas.width, canvas.height);
                    context.font = '20px Arial';
                    context.fillStyle = 'red';
                    context.fillText('Gender: {gender}', 10, 30);
                    context.fillText('Weight: {weight} kg', 10, 60);
                    context.fillText('Height: {height} cm', 10, 90);
                }}
                updateCanvas();
            </script>
        </div>
        """
        components.html(html_code, height=700)

if __name__ == "__main__":
    main()
