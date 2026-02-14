import streamlit as st
import tabula
import tempfile
import os

st.title("PDF to Excel Converter (Cloud Safe)")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file and st.button("Convert"):
    with st.spinner("Converting… this may take time for large PDFs"):

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            pdf_path = tmp.name

        output_csv = os.path.join(tempfile.gettempdir(), "output.csv")

        # 👇 NO JVM, NO JPype
        tabula.convert_into(
            pdf_path,
            output_csv,
            output_format="csv",
            pages="all",
            lattice=True
        )

        st.success("Conversion completed")

        with open(output_csv, "rb") as f:
            st.download_button(
                "⬇ Download CSV",
                f,
                file_name="PG_Counselling_2025_Round3.csv",
                mime="text/csv"
            )

        os.remove(pdf_path)
