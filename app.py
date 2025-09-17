import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import google.generativeai as genai
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib.styles import getSampleStyleSheet
import os

# Configure Gemini
genai.configure(api_key="your_api_key_here")  # Replace with your API key

def eda_analysis(file_path):
    df = pd.read_csv(file_path)
    
    # Handle missing values
    for col in df.select_dtypes(include=['number']).columns:
        df[col].fillna(df[col].median(), inplace=True)
    
    for col in df.select_dtypes(include=['object']).columns:
        df[col].fillna(df[col].mode()[0], inplace=True)
    
    # Summary as DataFrame (reset index so stats names appear)
    summary_df = df.describe(include='all').reset_index().rename(columns={'index': 'Statistic'})
    
    # Missing values as DataFrame (include column names)
    missing_values_df = df.isnull().sum().reset_index()
    missing_values_df.columns = ['Column', 'Missing Values']
    
    # AI insights
    insights = generate_ai_insights(summary_df.to_string())
    
    # Generate visualizations
    plot_paths = generate_visualizations(df)
    
    # Generate PDF report
    pdf_path = generate_pdf_report(summary_df, missing_values_df, insights, plot_paths)
    
    return (
        summary_df,
        missing_values_df,
        insights,
        plot_paths,
        pdf_path
    )

def generate_ai_insights(df_summary):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(f"Analyze the dataset summary and provide clear, structured insights:\n\n{df_summary}")
    return response.text

def generate_visualizations(df):
    plot_paths = []
    
    # Histogram for numeric columns
    for col in df.select_dtypes(include=['number']).columns:
        plt.figure(figsize=(6,4))
        sns.histplot(df[col], bins=30, kde=True, color="blue")
        plt.title(f"Distribution of {col}")
        path = f"{col}_distribution.png"
        plt.savefig(path)
        plot_paths.append(path)
        plt.close()
    
    # Correlation heatmap
    numeric_df = df.select_dtypes(include=['number'])
    if not numeric_df.empty:
        plt.figure(figsize=(8,5))
        sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
        plt.title("Correlation Heatmap")
        path = "correlation_heatmap.png"
        plt.savefig(path)
        plot_paths.append(path)
        plt.close()

    return plot_paths

def generate_pdf_report(summary_df, missing_df, insights, plot_paths):
    pdf_path = "EDA_Report.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph("📊 Automated EDA Report", styles["Title"]))
    elements.append(Spacer(1, 12))

    # Summary table
    elements.append(Paragraph("Dataset Summary", styles["Heading2"]))
    elements.append(Table([["Column"] + summary_df.columns.tolist()] + summary_df.reset_index().values.tolist()))
    elements.append(Spacer(1, 12))

    # Missing values
    elements.append(Paragraph("Missing Values", styles["Heading2"]))
    elements.append(Table([["Column", "Missing Count"]] + missing_df.reset_index().values.tolist()))
    elements.append(Spacer(1, 12))

    # Insights
    elements.append(Paragraph("AI Insights", styles["Heading2"]))
    elements.append(Paragraph(insights.replace("**", ""), styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Visualizations
    elements.append(Paragraph("Data Visualizations", styles["Heading2"]))
    for path in plot_paths:
        if os.path.exists(path):
            elements.append(Image(path, width=400, height=250))
            elements.append(Spacer(1, 12))

    doc.build(elements)
    return pdf_path


# -------------------- Gradio Advanced Layout --------------------
with gr.Blocks(title="📊 LLM-Powered EDA with Gemini") as demo:
    gr.Markdown("## 📂 Upload Your Dataset (CSV)")

    with gr.Row():
        file_input = gr.File(type="filepath", label="Upload CSV File")

    with gr.Column():
        gr.Markdown("### 📊 Dataset Summary")
        summary_output = gr.DataFrame(label="Summary Table")
        
        gr.Markdown("### ❌ Missing Values")
        missing_output = gr.DataFrame(label="Missing Values")

        gr.Markdown("### 🤖 AI Insights")
        insights_output = gr.Markdown()

        gr.Markdown("### 📉 Data Visualizations")
        gallery_output = gr.Gallery(label="Visualizations", columns=2, height="auto")

        gr.Markdown("### 📑 Download Report")
        pdf_output = gr.File(label="Download EDA Report (PDF)")

    file_input.change(
        fn=eda_analysis,
        inputs=file_input,
        outputs=[summary_output, missing_output, insights_output, gallery_output, pdf_output]
    )

demo.launch(share=True)

