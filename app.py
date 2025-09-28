import streamlit as st
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import io

# ===== PDF CONFIG =====
PDF_WIDTH = 50 * mm   # 50mm wide
PDF_HEIGHT = 30 * mm  # 30mm tall

# ===== STREAMLIT APP =====
st.title("Label Generator (30mm x 50mm)")

st.write("""
Upload an Excel file with **Item Name**, **Net Weight**, and **MRP** columns.
Each row will generate a 30mm x 50mm label in the PDF.
""")

# Font size selector
font_size = st.number_input(
    "Select font size",
    min_value=8,
    max_value=20,
    value=12,
    step=1,
    help="Adjust the font size for the label text"
)

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    try:
        # Read Excel file
        df = pd.read_excel(uploaded_file)

        # Validate columns
        required_columns = ["Item Name", "Net Weight", "MRP"]
        if not all(col in df.columns for col in required_columns):
            st.error(f"Excel must contain these columns: {required_columns}")
        else:
            st.success("File uploaded successfully!")

            # Generate PDF in memory
            pdf_buffer = io.BytesIO()
            c = canvas.Canvas(pdf_buffer, pagesize=(PDF_WIDTH, PDF_HEIGHT))

            for _, row in df.iterrows():
                item_name = str(row['Item Name']).strip()
                net_weight = str(row['Net Weight']).strip()
                mrp = f"MRP: ₹{row['MRP']:.2f}" if not pd.isnull(row['MRP']) else "MRP: -"

                # --- Draw Text ---
                c.setFont("Courier-Bold", font_size + 2)  # Slightly larger for item name
                c.drawCentredString(PDF_WIDTH / 2, PDF_HEIGHT - 8 * mm, item_name)

                c.setFont("Courier-Bold", font_size)
                c.drawCentredString(PDF_WIDTH / 2, PDF_HEIGHT - 15 * mm, f"Net Wt: {net_weight}")
                c.drawCentredString(PDF_WIDTH / 2, PDF_HEIGHT - 22 * mm, mrp)

                # End of page
                c.showPage()

            # Save PDF
            c.save()
            pdf_buffer.seek(0)

            # Download button
            st.download_button(
                label="Download PDF",
                data=pdf_buffer,
                file_name="labels.pdf",
                mime="application/pdf"
            )

            st.success("PDF generated successfully! Click above to download.")

    except Exception as e:
        st.error(f"Error processing file: {e}")
