import streamlit as st
import tabula
import pandas as pd
import tempfile
import os

st.set_page_config(page_title="PDF to Excel Converter", layout="centered")

st.title("📄 PDF to Excel Converter")
st.write("Convert large tabular PDFs (like PG Counselling lists) into Excel.")

uploaded_file = st.file_uploader(
    "Upload PDF file",
    type=["pdf"]
)

if uploaded_file is not None:
    st.success("PDF uploaded successfully")

    if st.button("Convert to Excel"):
        with st.spinner("Processing PDF… this may take several minutes for large files"):

            # Save uploaded PDF to a temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                tmp_pdf.write(uploaded_file.read())
                pdf_path = tmp_pdf.name

            try:
                # Extract tables
                tables = tabula.read_pdf(
                    pdf_path,
                    pages="all",
                    multiple_tables=True,
                    java_options="-Xmx4g"  # important for large PDFs
                )

                if not tables:
                    st.error("No tables found in PDF")
                else:
                    # Create Excel file
                    excel_path = os.path.join(tempfile.gettempdir(), "PG_Counselling_2025_Round3.xlsx")

                    with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
                        for i, table in enumerate(tables):
                            table.to_excel(
                                writer,
                                sheet_name=f"Page_{i+1}",
                                index=False
                            )

                    st.success("Excel file created successfully")

                    with open(excel_path, "rb") as f:
                        st.download_button(
                            label="⬇ Download Excel",
                            data=f,
                            file_name="PG_Counselling_2025_Round3.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )

            except Exception as e:
                st.error(f"Error occurred: {e}")

            finally:
                os.remove(pdf_path)
