# 📄 EDA-LLM-Project (README.md)

# 📊 LLM-Powered Exploratory Data Analysis (EDA)

This project automates Exploratory Data Analysis (EDA) by combining **Pandas, Seaborn, Matplotlib** with **Google Gemini LLM** for AI-driven insights.  
It generates:
- 📝 Summary statistics  
- 🧩 Missing values report  
- 📈 Visualizations (histograms, heatmaps, etc.)  
- 🤖 AI-powered insights from Gemini  
- 📑 Downloadable PDF Report  

---

## 🚀 Features
- Upload a CSV file and instantly get an **EDA Report**
- Structured summary + missing values in tabular format
- Automated visualizations for numeric features
- AI insights powered by **Gemini**
- Export results as a PDF report

---

## 📂 Project Structure
```

LLM-Powered-EDA/
│── app.py                     # Main Gradio app
│── requirements.txt           # Dependencies
│── README.md                  # Project description

````

---

## 🔧 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/LLM-Powered-EDA.git
   cd LLM-Powered-EDA

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up your **Gemini API Key**:

   ```bash
   export GOOGLE_API_KEY="your_api_key_here"    # Mac/Linux
   set GOOGLE_API_KEY="your_api_key_here"       # Windows PowerShell
   ```

4. Run the app:

   ```bash
   python app.py
   ```

---

## 🤖 Gemini Setup

* Get your free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
* Students usually get **\$300 free credits (3 months)**
* Each request costs only a few tokens — more than enough for EDA projects

---

## 📊 Example Workflow

1. Upload `sample.csv`
2. View summary + missing values + AI insights
3. Explore histograms + correlation heatmap
4. Download full PDF report

---

## 📜 License

MIT License. Use freely for education and research.

## 📦 requirements.txt

```txt
gradio==4.36.1
pandas==2.2.2
numpy==1.26.4
matplotlib==3.9.2
seaborn==0.13.2
reportlab==4.2.2
google-generativeai==0.5.4
````
