import streamlit as st
import pdfplumber
import pandas as pd
import tempfile
import os
import re

st.set_page_config(page_title="PDF to Excel (Cloud Safe)", layout="centered")
st.title("📄 PDF to Excel Converter (No Java)")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file and st.button("Convert"):
    with st.spinner("Extracting text from PDF… this may take time"):

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            pdf_path = tmp.name

        rows = []

        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if not text:
                    continue

                for line in text.split("\n"):
                    # Detect rows starting with Roll No
                    match = re.match(r"^(\d{11})\s+(.*)", line)
                    if match:
                        rows.append([match.group(1), match.group(2)])

        os.remove(pdf_path)

        if not rows:
            st.error("No data extracted")
        else:
            df = pd.DataFrame(rows, columns=["Roll No", "Details"])

            excel_path = "PG_Counselling_2025_Round3.xlsx"
            df.to_excel(excel_path, index=False)

            st.success("Excel file created")

            with open(excel_path, "rb") as f:
                st.download_button(
                    "⬇ Download Excel",
                    f,
                    file_name=excel_path,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
