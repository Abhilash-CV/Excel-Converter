import streamlit as st
import tabula
import tempfile
import os

st.set_page_config(page_title="PDF to CSV Converter", layout="centered")
st.title("📄 PDF to CSV Converter (Streamlit Cloud Safe)")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file and st.button("Convert"):
    with st.spinner("Converting PDF… (large files may take time)"):

        # Save uploaded PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            pdf_path = tmp.name

        output_csv = os.path.join(tempfile.gettempdir(), "output.csv")

        try:
            # 🔑 CRITICAL: force_subprocess=True (NO JVM)
            tabula.convert_into(
                pdf_path,
                output_csv,
                output_format="csv",
                pages="all",
                lattice=True,
                force_subprocess=True
            )

            st.success("Conversion completed")

            with open(output_csv, "rb") as f:
                st.download_button(
                    "⬇ Download CSV",
                    f,
                    file_name="PG_Counselling_2025_Round3.csv",
                    mime="text/csv"
                )

        except Exception as e:
            st.error(f"Conversion failed: {e}")

        finally:
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
