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

def get_bmi_category(bmi):
    if bmi < 18.5:
        return 'underweight', '#ADD8E6'
    elif 18.5 <= bmi < 24.9:
        return 'normal weight', '#90EE90'
    elif 25 <= bmi < 29.9:
        return 'overweight', '#FFD700'
    else:
        return 'obese', '#FF6347'

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
        bmi_category, color = get_bmi_category(bmi)
        
        st.write(f"Calculated BMI: {bmi:.2f}")
        st.write(f"Calculated Body Fat Percentage: {bfp:.2f}%")
        st.write(f"BMI Category: {bmi_category}")
        
        # Embed the interactive canvas
        html_code = f"""
        <div id="body_viewer" style="position: relative; width: 550px; height: 670px;">
            <canvas id="bmiCanvas" width="550" height="670"></canvas>
            <script>
                function drawBodyShape(bmi, weight, height, color) {{
                    var canvas = document.getElementById('bmiCanvas');
                    var ctx = canvas.getContext('2d');
                    ctx.clearRect(0, 0, canvas.width, canvas.height);

                    var centerX = canvas.width / 2;
                    var centerY = canvas.height / 2;

                    var bodyWidth = 50 + (bmi - 20);
                    var bodyHeight = 150 + ((height - 170) / 2);
                    var armLength = bodyHeight / 4;
                    var legLength = bodyHeight / 3;

                    ctx.beginPath();
                    ctx.arc(centerX, centerY - bodyHeight / 2 - 30, 30, 0, 2 * Math.PI);
                    ctx.fillStyle = color;
                    ctx.fill();
                    ctx.stroke();

                    ctx.fillStyle = color;
                    ctx.fillRect(centerX - bodyWidth / 2, centerY - bodyHeight / 2, bodyWidth, bodyHeight);
                    ctx.fillRect(centerX - bodyWidth / 2 - 20, centerY - bodyHeight / 2, 20, armLength);
                    ctx.fillRect(centerX + bodyWidth / 2, centerY - bodyHeight / 2, 20, armLength);
                    ctx.fillRect(centerX - bodyWidth / 4, centerY + bodyHeight / 2, 20, legLength);
                    ctx.fillRect(centerX + bodyWidth / 4 - 20, centerY + bodyHeight / 2, 20, legLength);

                    ctx.font = '20px Arial';
                    ctx.fillStyle = 'black';
                    ctx.fillText('BMI: ' + bmi.toFixed(2), 10, 30);
                    ctx.fillText('Weight: ' + weight + ' kg', 10, 60);
                    ctx.fillText('Height: ' + height + ' cm', 10, 90);
                }}
                
                var bmi = {bmi};
                var weight = {weight};
                var height = {height};
                var color = '{color}';
                drawBodyShape(bmi, weight, height, color);
            </script>
        </div>
        """
        components.html(html_code, height=700)

if __name__ == "__main__":
    main()
