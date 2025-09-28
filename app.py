import streamlit as st
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import mm
from io import BytesIO

# Function to generate PDF
def generate_pdf(item_name, net_weight, mrp):
    buffer = BytesIO()
    pdf_width = 50 * mm
    pdf_height = 30 * mm

    c = canvas.Canvas(buffer, pagesize=(pdf_width, pdf_height))

    # Set font to Courier-Bold
    c.setFont("Courier-Bold", 14)
    c.drawString(5 * mm, 20 * mm, str(item_name))

    c.setFont("Courier-Bold", 12)
    c.drawString(5 * mm, 14 * mm, f"Net Wt: {net_weight}")
    c.drawString(5 * mm, 8 * mm, f"MRP: ₹{mrp}")

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# Streamlit app
st.title("PDF Label Generator (30mm x 50mm)")

uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("### Uploaded Data")
    st.dataframe(df)

    # Dropdown to select an item
    selected_item = st.selectbox("Select an item to generate PDF", df["Item Name"].tolist())

    # Get selected row
    item_row = df[df["Item Name"] == selected_item].iloc[0]
    item_name = item_row["Item Name"]
    net_weight = item_row["Net Weight"]
    mrp = item_row["MRP"]

    if st.button("Generate PDF"):
        pdf_buffer = generate_pdf(item_name, net_weight, mrp)
        st.download_button(
            label="Download PDF",
            data=pdf_buffer,
            file_name=f"{item_name}_label.pdf",
            mime="application/pdf"
        )
