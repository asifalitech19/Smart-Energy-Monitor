# ⚡ Smart Energy Monitor: AI-Powered Home Efficiency System

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Green AI](https://img.shields.io/badge/Green%20AI-Sustainable-green?style=for-the-badge&logo=leaf&logoColor=white)

## 📌 Project Overview
The **Smart Energy Monitor** is an end-to-end Machine Learning application designed to predict household energy consumption and optimize electricity bills. 

Building upon my research experience at **Chengdu University of Technology (CDUT), China**, where I analyzed energy patterns of 2.2 million households, this project brings those insights to a practical, user-friendly dashboard tailored for the **Pakistani context**.

It combines **Real-time Weather Data**, **Appliance Load Calculation**, and **AI Prediction** to help users reduce their Carbon Footprint and Electricity Costs (PKR).

## 🚀 Key Features
* **🇵🇰 Localized Context:** Customized for Pakistani households (includes UPS, Water Motors, Iron, ACs).
* **💰 Bill Estimation:** Real-time calculation of hourly and monthly costs in **PKR (Rs.)**.
* **🤖 AI-Powered:** Uses `Random Forest Regressor` to predict Base Load based on weather conditions.
* **⏱️ Real-Time Sync:** Automatically fetches Pakistan Standard Time (PKT) for accurate simulation.
* **🌱 Green AI Audit:** The model training process was audited using `CodeCarbon` to ensure minimal energy consumption (0.12g CO2 footprint).

## 🛠️ Tech Stack
* **Frontend:** Streamlit (Custom CSS & Glassmorphism UI).
* **Machine Learning:** Scikit-Learn (Random Forest).
* **Visualization:** Plotly (Interactive Gauge Meters & Pie Charts).
* **Sustainability:** CodeCarbon (for tracking model efficiency).

## 📊 How It Works
1.  **Weather Input:** The user sets the current weather (Temperature, Humidity).
2.  **Appliance Selection:** Selects active devices (AC, Fans, Fridge, UPS charging).
3.  **AI + Logic:** The system combines the AI's "Base Load" prediction with the calculated "Appliance Load".
4.  **Output:** Provides a live dashboard showing total watts, estimated bill, and energy-saving tips.

## 🔧 Installation
```bash
# Clone the repository
git clone [https://github.com/your-username/smart-energy-monitor.git](https://github.com/your-username/smart-energy-monitor.git)

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
