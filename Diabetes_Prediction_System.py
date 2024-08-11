# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 10:18:58 2023
@author: Akshay Ravella

"""

import numpy as np
import pickle
import streamlit as st
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from streamlit_option_menu import option_menu
 

with st.sidebar:
    selected = option_menu("Menu", ["Home", 'Others'], 
        icons=['house', 'three-dots'], default_index=0)
    

# loading the saved model
loaded_model = pickle.load(open('trained_model.sav', 'rb'))

# creating a function for prediction
def diabetes_prediction(input_data):
    # changing the input_data to numpy array
    input_data_as_numpy_array = np.asarray(input_data)
    # reshape the array as we are predicting for one instance
    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)
    prediction = loaded_model.predict(input_data_reshaped)
    print(prediction)
    if prediction[0] == 0:
        return 'Not Diabetic'
    else:
        return 'Diabetic'

# Function to send a thank-you email with test result and contact details
def send_thank_you_email(name, email, diagnosis):
    sender_name = "Akshay Ravella"
    sender_email = "akshayravella1@gmail.com"  
    sender_password = "fuyq wyjl cgnn wbpw"  

    linkedin_profile = "https://www.linkedin.com/in/akshay-ravella"
    webpapp_url = "https://diabetespredictionsystem-by-akshay.streamlit.app/"
    
    banner = """<!-- Insert the banner image -->
    <img src="{}" alt="Banner Image" style="max-width: 100%; height: auto; margin-top: 20px;">
    """.format('https://d2jx2rerrg6sh3.cloudfront.net/images/Article_Images/ImageForArticle_22744_16565132428524067.jpg')
    
    # Additional tips for diabetic patients and prevention
    additional_tips = """ 
    <p><strong><u>Tips for Diabetic Patients:</u></strong></p>
    <ol>
        <li><strong>Monitor Blood Sugar Levels:</strong><br>
        - Regularly check your blood glucose levels as advised by your healthcare provider.</li>
        <li><strong>Medication Adherence:</strong><br>
        - Take medications as prescribed by your healthcare provider.</li>
        <li><strong>Balanced Nutrition:</strong><br>
        - Adopt a diet rich in whole grains, lean proteins, fruits, and vegetables.</li>
        <li><strong>Regular Exercise:</strong><br>
        - Engage in physical activity like brisk walking, swimming, or cycling.</li>
        <li><strong>Mindful Stress Management:</strong><br>
        - Practice stress-reducing techniques, such as mindfulness, meditation, or yoga.</li>
    </ol>
    <p><strong><u>Tips for Diabetes Prevention:</u></strong></p>
    <ol>
        <li><strong>Healthy Dietary Choices:</strong><br>
        - Consume a well-balanced diet with a focus on fruits, vegetables, whole grains, and lean proteins.<br>
        - Limit the intake of processed foods, sugary drinks, and high-fat items.</li>
        <li><strong>Regular Physical Activity:</strong><br>
        - Engage in regular physical activity to maintain a healthy weight and improve insulin sensitivity.</li>
        <li><strong>Weight Management:</strong><br>
        - Aim for a body mass index (BMI) within the normal range.<br>
        - Even a small reduction in weight can significantly lower the risk of diabetes.</li>
        <li><strong>Reduce Sedentary Time:</strong><br>
        - Minimize sitting time and incorporate more movement into your daily routine.</li>
        <li><strong>Routine Health Check-ups:</strong><br>
        - Schedule regular check-ups to monitor overall health and detect any potential issues early on.</li>
    </ol>
    <p>**It's important to note that these tips should be personalized based on individual health conditions and preferences. Consultation with healthcare professionals is crucial for tailored advice and management.</p>
    """

    subject = "Thank You for Visiting Diabetes Prediction Web Application!"
    color = "red" if diagnosis == "Diabetic" else "green"
    body = f"Dear {name},<br><br>Thank you for visiting my Diabetes Prediction Web Application!<br><br><b>Test Result:</b> <b style='color:{color}'>{diagnosis}</b>{banner}{additional_tips}<br><br>WebApp URL: {webpapp_url}<br><br>Connect: {linkedin_profile}<br><br><br>Best regards,<br>Akshay Ravella"

    message = MIMEMultipart()
    message["From"] = f"{sender_name} <{sender_email}>"
    message["To"] = email
    message["Subject"] = subject
    message.attach(MIMEText(body, "html"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, message.as_string())

def main():
    
    if(selected == 'Home'):
        
        
        st.title('Diabetes Prediction Web App')

        name = st.text_input('Enter Your Name')
        email = st.text_input('Enter Your Email')

        if not name or not email:
            st.warning('Please enter both Name and Email to proceed!', icon="⚠️")
            st.stop()

        if not email.endswith('@gmail.com'):
            st.error("Invalid email address!", icon="❌")
            st.stop()
        
        st.caption("**Having confusion in giving inputs? Navigate to the Options menu in the top-left corner and click on **Others** for more information.")
        
        sex = st.selectbox('Gender',('Male','Female'))
        Pregnancies = st.text_input('Number of Pregnancies (Enter 0 if Male)')
        Glucose = st.text_input('Glucose Level')
        BloodPressure = st.text_input('BloodPressure Value')
        SkinThickness = st.text_input('Skin Thickness Value')
        Insulin = st.text_input('Insulin Level')
        BMI = st.text_input('BMI Value')
        DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function Value')
        Age = st.slider('Choose your Age',1,100)
        
        # Check if the entered values are numeric
        if not all(value.replace('.', '', 1).isdigit() for value in [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction]):
            st.error("❗Please enter valid numerical values for the input fields.")
            st.stop()
     
        # Prediction button
        if st.button('Predict'):
            diagnosis = diabetes_prediction([Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age])

            # Sending thank-you email with test result and contact details
            send_thank_you_email(name, email, diagnosis)

            # Displaying the result
            with st.spinner('Please wait, loading...'):
                time.sleep(2)

                st.success(f"Test Result: **{diagnosis}**")
                
                st.info('Do check your email for more details, Thank You.', icon="ℹ️")
                
        st.markdown(
        """<div style="position: fixed; bottom: 7.6px; left: 10px; right: 10px; text-align: left; color: grey; font-size: 14px;">
        Made by <span style="font-weight: bold; color: grey;">Akshay</span>🎈
        </div>""",
        unsafe_allow_html=True
        ) 

    elif(selected == 'Others'):
        
        tab1, tab2, tab3 = st.tabs(["❓Help", "💬 Feedback", "📩 Contact"])
        
        with tab1:
            st.header("Welcome to the Help Page!",divider='rainbow')
            st.write("This application is designed to predict whether a person is diabetic or not based on input data such as the number of pregnancies, glucose level, blood pressure, and other relevant factors.")
            st.write("It works in real-time with 90% accuracy, since it is built using a trained and tested machine learning model.")
            st.write("If you possess true values for pregnancies, BMI, insulin, etc., enter them for precise predictions.")
            st.write("To experience how the application functions, you can use the sample values provided below.")

            # Sample data table
            sample_data = {
                "Pregnancies": [6, 1, 8, 1, 0, 5, 3, 10, 2],
                "Glucose": [148, 85, 183, 89, 137, 116, 78, 115, 197],
                "BloodPressure": [72, 66, 64, 66, 40, 74, 50, 0, 70],
                "SkinThickness": [35, 29, 0, 23, 35, 0, 32, 0, 45],
                "Insulin": [0, 0, 0, 94, 168, 0, 88, 0, 543],
                "BMI": [33.6, 26.6, 23.3, 28.1, 43.1, 25.6, 31, 35.3, 30.5],
                "PedigreeFunction": [0.627, 0.351, 0.672, 0.167, 2.288, 0.201, 0.248, 0.134, 0.158],
                "Age": [50, 31, 32, 21, 33, 30, 26, 29, 53]
            }

            # Convert sample data to a Pandas DataFrame for better tabular display
            import pandas as pd
            sample_df = pd.DataFrame(sample_data)

            st.caption("Sample Data:")
            st.dataframe(sample_df)
            
            st.subheader("Note:")
            
            st.info(
                
                "This webpage requests your name and email to send you details about your test results.\n\n"
                "Rest assured, your information is safe and will be kept confidential."
                )
            
        with tab3:
            st.write("Connect: [LinkedIn Profile](https://www.linkedin.com/in/akshay-ravella)")
            st.write("Email: [akshayravella1@gmail.com](mailto:akshayravella1@gmail.com)")
            st.write(" ")
            st.image('https://pngimg.com/d/thank_you_PNG88.png', width=220)
            
            st.markdown(
            """<div style="position: fixed; bottom: 7.6px; left: 10px; right: 10px; text-align: left; color: grey; font-size: 14px;">
            Made by <span style="font-weight: bold; color: grey;">Akshay</span>🎈
            </div>""",
            unsafe_allow_html=True
            ) 
            
        with tab2:
            import requests
            st.subheader("Your Feedback is Valuable!", divider='rainbow')
            user_message = st.text_area("Have questions or suggestions? I'd love to hear from you.", height=80, placeholder="Type here...")
            if st.button("Send"):
                formspree_endpoint = "https://formspree.io/f/mbjnrbvv"
                data = {"message": user_message}
                response = requests.post(formspree_endpoint, data=data)
                
                if response.status_code == 200:
                    st.success("Message sent successfully!")
                else:
                    st.error("Failed to send message, Please try again.")
            
if __name__ == "__main__":
    main()