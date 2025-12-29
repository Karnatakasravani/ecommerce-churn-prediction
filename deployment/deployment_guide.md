\# Deployment Guide  

\## Platform: Streamlit Community Cloud (Free)



---



\## ✅ Prerequisites



\- GitHub account  

\- Public GitHub repository  

\- `streamlit\_app.py` located either:

&nbsp; - in root folder \*\*or\*\*

&nbsp; - inside `app/` folder



---



\## 🚀 Step-by-Step Deployment



\### 1️⃣ Prepare Your Repository



Make sure your project has the correct structure:



your-repo/

├── app/

│ └── streamlit\_app.py

├── models/

│ ├── logistic\_model.pkl

│ ├── random\_forest\_model.pkl

│ └── scaler.pkl

├── data/

│ ├── processed/

│ └── raw/

├── requirements.txt

└── README.md





---



\### 2️⃣ Create `requirements.txt`



Ensure this file exists in the \*\*root directory\*\* and includes:



streamlit==1.28.0

pandas==2.1.4

numpy==1.26.2

scikit-learn==1.3.2

joblib==1.3.2

matplotlib==3.8.2

seaborn==0.13.1







(Add anything else you actually use)



---



\### 3️⃣ Deploy on Streamlit Cloud



1\. Go to 🔗 https://share.streamlit.io  

2\. Click \*\*Sign in with GitHub\*\*

3\. Click \*\*“New app”\*\*

4\. Select:

&nbsp;  - Repository → `your-repo`

&nbsp;  - Branch → `main`

&nbsp;  - Main file path →  

&nbsp;    - `app/streamlit\_app.py`  \*(if inside app folder)\*  

&nbsp;    - OR `streamlit\_app.py` \*(if in root)\*



5\. Click \*\*Deploy\*\*



⏳ Wait 1–3 minutes



Streamlit will automatically:

✔ Install dependencies  

✔ Download model files  

✔ Launch your app  



---



\## 🔍 4️⃣ Post-Deployment Checklist



After deployment, test the app:



\### ✅ Testing Checklist



\- ☐ App loads successfully  

\- ☐ Single prediction works  

\- ☐ Batch prediction works  

\- ☐ Visualizations display  

\- ☐ No Python errors in logs  



(Open logs via Streamlit → “Manage app” → “Logs”)



---



\## 🔗 Live Application URL



Paste your deployed link here:



https://your-app-name.streamlit.app/





---



\# ⚠️ Common Issues \& Fixes



\### ❌ App fails to load  

✔ Check `requirements.txt`



\### ❌ Model file not found  

✔ Ensure paths match exactly  

✔ Model inside `/models/`



\### ❌ Import errors  

✔ Restart \& redeploy



---



\# 🎯 Final Step



Update your README.md



Include:



\- Deployment link

\- Screenshot

\- Short usage guide



---



\## ✅ You’re Done!



Your churn prediction app is now live 🚀





