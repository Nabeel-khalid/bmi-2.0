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
    st.title("BMI 2.0 Calculator and Visualizer")

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
        
        # Embed the interactive canvas
        html_code = f"""
        <div>
            <canvas id="bmiCanvas" width="400" height="800"></canvas>
            <script>
                function drawBodyShape(bmi, weight, height) {{
                    var canvas = document.getElementById('bmiCanvas');
                    var ctx = canvas.getContext('2d');
                    ctx.clearRect(0, 0, canvas.width, canvas.height);

                    // Adjustments for body shape based on BMI, weight, and height
                    var baseWidth = 50;
                    var baseHeight = 150;
                    var bodyWidth = baseWidth + (bmi - 20);
                    var bodyHeight = baseHeight + ((height - 170) / 10);

                    // Draw head
                    ctx.beginPath();
                    ctx.arc(200, 100, 40, 0, 2 * Math.PI);
                    ctx.fillStyle = 'lightgray';
                    ctx.fill();
                    ctx.stroke();

                    // Draw body
                    ctx.fillStyle = 'lightgray';
                    ctx.fillRect(200 - bodyWidth / 2, 140, bodyWidth, bodyHeight);

                    // Draw arms
                    ctx.fillRect(200 - bodyWidth / 2 - 20, 140, 20, 100);
                    ctx.fillRect(200 + bodyWidth / 2, 140, 20, 100);

                    // Draw legs
                    ctx.fillRect(200 - bodyWidth / 4, 140 + bodyHeight, 20, 100);
                    ctx.fillRect(200 + bodyWidth / 4 - 20, 140 + bodyHeight, 20, 100);
                }}
                
                // Update the canvas based on the current values
                var bmi = {bmi};
                var weight = {weight};
                var height = {height};
                drawBodyShape(bmi, weight, height);
            </script>
        </div>
        """
        components.html(html_code, height=800)

if __name__ == "__main__":
    main()
