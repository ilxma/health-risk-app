import streamlit as st
import plotly.graph_objects as go
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="Health Risk Predictor",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for medical theme
st.markdown("""
    <style>
    .title-main {
        text-align: center;
        color: #1f77b4;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 0.5em;
    }
    .subtitle {
        text-align: center;
        color: #555;
        font-size: 1.1em;
        margin-bottom: 2em;
    }
    .metric-box {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
    .risk-low {
        background-color: #d1f2eb;
        border-left: 5px solid #27ae60;
        padding: 20px;
        border-radius: 5px;
    }
    .risk-moderate {
        background-color: #fef5e7;
        border-left: 5px solid #f39c12;
        padding: 20px;
        border-radius: 5px;
    }
    .risk-high {
        background-color: #fadbd8;
        border-left: 5px solid #e74c3c;
        padding: 20px;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Title and Subtitle
st.markdown('<div class="title-main">❤️ AI-Based Health Risk Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Predicting cardiovascular and metabolic disease risk using clinical and lifestyle data</div>', unsafe_allow_html=True)

st.divider()

# Create two columns for input
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Personal Information")
    age = st.slider("Age (years)", min_value=18, max_value=100, value=45, step=1)
    
    st.subheader("📏 Body Measurements")
    bmi = st.number_input("BMI (Body Mass Index)", min_value=10.0, max_value=60.0, value=25.0, step=0.1)
    systolic_bp = st.number_input("Systolic Blood Pressure (mmHg)", min_value=70, max_value=220, value=120, step=1)
    
with col2:
    st.subheader("🩸 Blood Tests")
    glucose = st.number_input("Fasting Glucose Level (mg/dL)", min_value=50, max_value=400, value=100, step=1)
    hba1c = st.number_input("HbA1c (%)", min_value=3.0, max_value=15.0, value=5.5, step=0.1)
    cholesterol = st.number_input("Total Cholesterol (mg/dL)", min_value=100, max_value=500, value=200, step=1)

st.divider()

# Lifestyle factors
col3, col4 = st.columns(2)

with col3:
    st.subheader("🏃 Lifestyle Factors")
    activity = st.selectbox("Physical Activity Level", ["Low", "Moderate", "High"], index=1)

with col4:
    st.subheader("🚭 Habits")
    smoking = st.radio("Do you smoke?", ["No", "Yes"], index=0)

st.divider()

# Calculate risk score
def calculate_risk_score(bmi, systolic_bp, glucose, hba1c, cholesterol, activity, smoking):
    score = 0
    
    # BMI assessment
    if bmi > 30:
        score += 2
    
    # Blood Pressure assessment
    if systolic_bp > 140:
        score += 2
    
    # Glucose assessment
    if glucose > 126:
        score += 2
    
    # HbA1c assessment
    if hba1c > 6.5:
        score += 3
    
    # Cholesterol assessment
    if cholesterol > 200:
        score += 2
    
    # Physical Activity assessment
    if activity == "Low":
        score += 2
    
    # Smoking assessment
    if smoking == "Yes":
        score += 2
    
    return score

def get_risk_level(score):
    if score <= 4:
        return "Low Risk", "🟢", "#27ae60"
    elif score <= 8:
        return "Moderate Risk", "🟡", "#f39c12"
    else:
        return "High Risk", "🔴", "#e74c3c"

def get_recommendations(risk_level):
    recommendations = {
        "Low Risk": [
            "✓ Continue maintaining your current healthy lifestyle",
            "✓ Keep regular health check-ups (annually)",
            "✓ Maintain BMI below 30",
            "✓ Exercise 150 minutes per week",
            "✓ Eat a heart-healthy diet rich in vegetables and whole grains"
        ],
        "Moderate Risk": [
            "⚠️ Schedule a consultation with your healthcare provider",
            "⚠️ Increase physical activity to 150+ minutes per week",
            "⚠️ Consider dietary modifications (reduce salt and saturated fat)",
            "⚠️ Monitor blood pressure and glucose regularly",
            "⚠️ If applicable, consider smoking cessation programs",
            "⚠️ Health check-ups every 6 months"
        ],
        "High Risk": [
            "🔴 Seek immediate medical consultation",
            "🔴 This assessment does not replace professional medical advice",
            "🔴 Work with your doctor on a personalized risk reduction plan",
            "🔴 Intensive lifestyle modification is strongly recommended",
            "🔴 Regular monitoring and possible medical management needed",
            "🔴 Consider referral to cardiometabolic specialist",
            "🔴 Health check-ups every 3 months or as advised"
        ]
    }
    return recommendations.get(risk_level, [])

# Calculate score
risk_score = calculate_risk_score(bmi, systolic_bp, glucose, hba1c, cholesterol, activity, smoking)
risk_level, emoji, color = get_risk_level(risk_score)

# Display results
st.markdown("---")
st.subheader("📊 Risk Assessment Results", divider=True)

# Risk score display
result_col1, result_col2, result_col3 = st.columns([1, 1, 1])

with result_col2:
    st.metric(label="Risk Score", value=f"{risk_score}/15")

# Risk level display
if risk_level == "Low Risk":
    st.markdown(f'<div class="risk-low"><h3>{emoji} {risk_level}</h3><p>Your predicted cardiovascular and metabolic disease risk is relatively low. Continue maintaining your healthy lifestyle.</p></div>', unsafe_allow_html=True)
elif risk_level == "Moderate Risk":
    st.markdown(f'<div class="risk-moderate"><h3>{emoji} {risk_level}</h3><p>Your predicted risk is moderate. Consult with your healthcare provider and implement recommended lifestyle changes.</p></div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="risk-high"><h3>{emoji} {risk_level}</h3><p>Your predicted risk is high. Please seek medical consultation for proper assessment and management.</p></div>', unsafe_allow_html=True)

# Display recommendations
st.subheader("💡 Recommendations", divider=True)
recommendations = get_recommendations(risk_level)
for rec in recommendations:
    st.write(rec)

# Risk breakdown visualization
st.subheader("📈 Risk Factor Breakdown", divider=True)

risk_factors = {
    "BMI > 30": 2 if bmi > 30 else 0,
    "BP > 140": 2 if systolic_bp > 140 else 0,
    "Glucose > 126": 2 if glucose > 126 else 0,
    "HbA1c > 6.5": 3 if hba1c > 6.5 else 0,
    "Cholesterol > 200": 2 if cholesterol > 200 else 0,
    "Low Activity": 2 if activity == "Low" else 0,
    "Smoking": 2 if smoking == "Yes" else 0,
}

# Filter out zero scores for cleaner visualization
active_factors = {k: v for k, v in risk_factors.items() if v > 0}

if active_factors:
    fig = go.Figure(data=[
        go.Bar(
            y=list(active_factors.keys()),
            x=list(active_factors.values()),
            orientation='h',
            marker=dict(color='#1f77b4')
        )
    ])
    fig.update_layout(
        title="Contributing Risk Factors",
        xaxis_title="Points Contributed",
        yaxis_title="Risk Factor",
        height=400,
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("✓ No significant risk factors detected. Great job on maintaining your health!")

# Medical disclaimer
st.divider()
st.markdown("""
<div style="padding: 15px; background-color: #e8f4f8; border-radius: 5px; border-left: 4px solid #3498db;">
<strong>⚠️ Medical Disclaimer:</strong> This tool is for educational and informational purposes only. It does not provide medical diagnosis or treatment advice. 
The results should not replace professional medical evaluation. Always consult with a qualified healthcare provider for medical concerns or decisions.
</div>
""", unsafe_allow_html=True)

st.markdown(f"<div style='text-align: center; color: #999; font-size: 0.9em; margin-top: 2em;'>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>", unsafe_allow_html=True)
