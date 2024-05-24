import streamlit as st
import openai
import io
from contextlib import redirect_stdout
from fpdf import FPDF
import os

#Your API Key here
openai.api_key = "#"

def perform_auto_analysis(data, default_dataset):
    with st.spinner("🤖 Generating auto analysis code..."):
        column_names = ", ".join(data.columns)
        first_rows = data.head().to_string(index=False)

        if default_dataset:
            file_name = "amazon_reviews.csv"
        else:
            file_name = uploaded_file.name

        prompt = f"You are a Data Analyst. You are given a dataset named '{file_name}' with the following columns: {column_names}\n\nHere are the first 5 rows of the dataset:\n{first_rows}\n\nPerform a complete analysis like you are telling a story. Return the code for each section line by line as I am saving this code in a .py file on extracting, so try not adding commas like these ``` or any other weird characters in code. Make sure you import all the default libraries required to run the code. Just directly provide the code as you write in a text editor normally. Make sure you use the correct column names as provided to you. After each plot, provide a brief explanation of the insights gained from the plot and save the plots with respectable name in form of images when the code is executed."
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=4096,
            n=1,
            stop=None,
            temperature=0.7,
        )
        auto_analysis_code = response.choices[0].message['content']

        code_file = "auto_analysis_code.py"
        with open(code_file, "w") as file:
            file.write(auto_analysis_code)

        st.success(f"Auto analysis code generated and saved as '{code_file}'")

        with st.expander("Generated Code and Output"):
            st.code(auto_analysis_code, language='python')

            plot_objects = []
            explanations = []
            stdout_buffer = io.StringIO()
            with redirect_stdout(stdout_buffer):
                exec(auto_analysis_code, {"data": data, "plt": plt, "sns": sns, "plot_objects": plot_objects, "explanations": explanations})

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            analysis_story = stdout_buffer.getvalue()
            pdf.multi_cell(0, 10, txt=analysis_story)

            pdf_file = "auto_analysis_report.pdf"
            pdf.output(pdf_file)

            with open(pdf_file, "rb") as file:
                pdf_data = file.read()
            st.download_button(
                label="Download PDF Report",
                data=pdf_data,
                file_name=pdf_file,
                mime="application/pdf",
            )

    return auto_analysis_code

def auto_analysis(data, default_dataset):
    auto_analysis_tabs = st.tabs(["CSV Analysis", "Perform Auto Analysis"])

    with auto_analysis_tabs[0]:
        st.subheader("📊 CSV Analysis")
        st.write("Get recommendations and analysis based on your CSV file.")
        
        if st.button("Analyze CSV"):
            column_names = ", ".join(data.columns)
            first_rows = data.head().to_string(index=False)
            
            if default_dataset:
                file_name = "amazon_reviews.csv"
            else:
                file_name = uploaded_file.name
            
            prompt = f"You are a Data Analyst. You are given a dataset named '{file_name}' with the following columns: {column_names}\n\nHere are the first 5 rows of the dataset:\n{first_rows}\n\nProvide recommendations and analysis on what kind of EDA and analysis can be performed on this dataset. Suggest specific visualizations, statistical tests, and insights that can be derived from the data."
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.7,
            )
            csv_analysis = response.choices[0].message['content']
            st.write(csv_analysis)

    with auto_analysis_tabs[1]:
        st.subheader("🤖 Perform Auto Analysis")
        st.write("Generate auto analysis code and summary based on your dataset.")

        if st.button("Generate Auto Analysis Code"):
            auto_analysis_code = perform_auto_analysis(data, default_dataset)

        if st.button("Generate Analysis Summary"):
            st.write("Click this button to generate a detailed summary and analysis of the auto-generated code. The summary will explain the generated graphs and provide insights as a full story analysis.")
            
            with open("auto_analysis_code.py", "r") as file:
                auto_analysis_code = file.read()

            prompt = f"Please provide a detailed summary and analysis of the following code:\n\n{auto_analysis_code}\n\nExplain the generated graphs and provide insights as a full story analysis."
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=4096,
                n=1,
                stop=None,
                temperature=0.7,
            )
            analysis_summary = response.choices[0].message['content']

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            pdf.multi_cell(0, 10, txt=analysis_summary)

            plot_files = [f for f in os.listdir() if f.endswith(".png")]
            for plot_file in plot_files:
                pdf.add_page()
                pdf.image(plot_file, x=10, y=10, w=190)

            pdf_file = "analysis_summary.pdf"
            pdf.output(pdf_file)

            with open(pdf_file, "rb") as file:
                pdf_data = file.read()
            st.download_button(
                label="Download Analysis Summary",
                data=pdf_data,
                file_name=pdf_file,
                mime="application/pdf",
            )