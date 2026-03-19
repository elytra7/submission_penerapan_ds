import streamlit as st
import pandas as pd
import joblib

# 1. PAGE CONFIGURATION & STYLING
st.set_page_config(
    page_title="Dropout Early Warning System",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-size: 18px !important;
    }
    .main-header {
        font-size: 4rem !important; 
        font-weight: 550; 
        margin-bottom: 0;
        line-height: 1.2;
    }
    .sub-header {font-size: 1.3rem; color: #6B7280; margin-bottom: 2rem;}
    .card-metric {background-color: #F3F4F6; padding: 20px; border-radius: 10px; text-align: center;}
    </style>
""", unsafe_allow_html=True)

# 2. CACHED DATA & MODEL LOADING
@st.cache_resource
def load_model():
    model = joblib.load('model/rf_dropout_model.pkl')
    features = joblib.load('model/model_features.pkl')
    return model, features

@st.cache_data
def load_default_data():
    df = pd.read_csv('data.csv', sep=';')
    df.columns = df.columns.str.strip()
    return df.drop(columns=['Target'], errors='ignore').median()

try:
    model, feature_names = load_model()
    default_values = load_default_data()
except Exception as e:
    st.error(f"Critical Error: Could not load model or dataset. Details: {e}")
    st.stop()

# 3. APP HEADER
st.markdown('<p class="main-header">Dropout Early Warning System</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Identify at-risk students instantly using our machine learning model. Fill in the top 10 key metrics below to generate a risk assessment.</p>', unsafe_allow_html=True)

st.markdown("---")

# 4. USER INPUT SECTION
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.subheader("Academic Performance")
    cu_1st_app = st.slider("1st Sem Units Approved", 0, 20, 5, help="Number of curricular units approved in the 1st semester.")
    cu_1st_grade = st.slider("1st Sem Grade Average", 0.0, 20.0, 12.0, 0.1, help="Average grade in the 1st semester (0-20 scale).")
    cu_2nd_app = st.slider("2nd Sem Units Approved", 0, 20, 5, help="Number of curricular units approved in the 2nd semester.")
    cu_2nd_grade = st.slider("2nd Sem Grade Average", 0.0, 20.0, 12.0, 0.1, help="Average grade in the 2nd semester (0-20 scale).")

with col2:
    st.subheader("Financial Status")
    tuition = st.selectbox("Tuition Fees Up to Date", options=[1, 0], format_func=lambda x: "Yes" if x == 1 else "No", help="Are the student's tuition fees fully paid?")
    scholarship = st.selectbox("Scholarship Holder", options=[1, 0], format_func=lambda x: "Yes" if x == 1 else "No", help="Does the student have a scholarship?")
    debtor = st.selectbox("Is a Debtor?", options=[1, 0], format_func=lambda x: "Yes" if x == 1 else "No", index=1, help="Does the student have outstanding debts to the institution?")

with col3:
    st.subheader("Demographics & Entry")
    age = st.number_input("Age at Enrollment", min_value=15, max_value=60, value=20, help="Student's age when they first enrolled.")
    gender = st.selectbox("Gender", options=[1, 0], format_func=lambda x: "Male" if x == 1 else "Female")
    app_mode = st.number_input("Application Mode (ID)", min_value=1, max_value=60, value=1, help="The method by which the student applied (e.g., General contingent, Special status).")

st.markdown("<br>", unsafe_allow_html=True)

# 5. ACTION BUTTON & PREDICTION LOGIC
analyze_btn = st.button("Analyze Student Risk", type="primary", use_container_width=True)

if analyze_btn:
    st.markdown("---")
    
    input_data = pd.DataFrame([default_values], columns=feature_names)

    input_data.at[0, 'Curricular units 2nd sem (approved)'] = cu_2nd_app
    input_data.at[0, 'Curricular units 2nd sem (grade)'] = cu_2nd_grade
    input_data.at[0, 'Curricular units 1st sem (approved)'] = cu_1st_app
    input_data.at[0, 'Curricular units 1st sem (grade)'] = cu_1st_grade
    input_data.at[0, 'Tuition fees up to date'] = tuition
    input_data.at[0, 'Scholarship holder'] = scholarship
    input_data.at[0, 'Age at enrollment'] = age
    input_data.at[0, 'Debtor'] = debtor
    input_data.at[0, 'Gender'] = gender
    input_data.at[0, 'Application mode'] = app_mode

    prediction = model.predict(input_data)[0]
    prediction_proba = model.predict_proba(input_data)[0]
    
    # 6. RESULTS VISUALIZATION
    st.subheader("Assessment Results")
    
    res_col1, res_col2 = st.columns([1, 2], gap="medium")
    
    with res_col1:
        if prediction == 1:
            st.error("HIGH RISK")
            risk_score = prediction_proba[1] * 100
            st.metric(label="Probability of Dropout", value=f"{risk_score:.1f}%")
        else:
            st.success("LOW RISK")
            safe_score = prediction_proba[0] * 100
            st.metric(label="Probability of Graduating", value=f"{safe_score:.1f}%")
            
    with res_col2:
        st.markdown("#### Actionable Insights")
        if prediction == 1:
            st.progress(prediction_proba[1])
            st.markdown("""
            * **Immediate Action Required:** Schedule a 1-on-1 counseling session to discuss academic or financial hurdles.
            * **Financial Check:** Verify if the student needs assistance with tuition or debt restructuring.
            * **Academic Support:** Recommend tutoring for subjects causing low grades in the recent semesters.
            """)
        else:
            st.progress(prediction_proba[1])
            st.markdown("""
            * **On Track:** The student shows healthy academic progression and financial stability.
            * **Monitor:** Continue standard monitoring. Encourage participation in advanced projects or scholarships.
            """)