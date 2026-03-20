import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch
import io
from datetime import datetime, date

def generate_invoice(data: dict) ->bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Header
    elements.append(Paragraph(f"<b>{data['from_name']}</b>", styles['Title']))
    elements.append(Paragraph(data['from_email'], styles['Normal']))
    elements.append(Paragraph(data['from_address'], styles['Normal']))
    elements.append(Spacer(1, 20))

    # Invoice info
    invoice_data = [
        ['INVOICE', ''],
        ['Invoice No:', data['invoice_no']],
        ['Date:', data['date']],
        ['Due Date:', data['due_date']],
    ]
    invoice_table = Table(invoice_data, colWidths=[2*inch, 3*inch])
    invoice_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('SPAN', (0, 0), (-1, 0)),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.lightblue, colors.white]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(invoice_table)
    elements.append(Spacer(1, 20))

    # Bill To
    elements.append(Paragraph("<b>Bill To:</b>", styles['Heading2']))
    elements.append(Paragraph(data['to_name'], styles['Normal']))
    elements.append(Paragraph(data['to_company'], styles['Normal']))
    elements.append(Paragraph(data['to_email'], styles['Normal']))
    elements.append(Spacer(1, 20))

    # Items table
    items_header = ['#', 'Description', 'Qty', 'Rate', 'Amount']
    items_data = [items_header]
    
    subtotal = 0
    for i, item in enumerate(data['invoice_items']):
        amount = item['qty'] * item['rate']
        subtotal += amount
        items_data.append([
            str(i+1),
            item['description'],
            str(item['qty']),
            f"Rs.{item['rate']:,.0f}",
            f"Rs.{amount:,.0f}"
        ])

    # Totals
    tax = subtotal * data['tax_rate'] / 100
    total = subtotal + tax

    items_data.append(['', '', '', 'Subtotal:', f"Rs.{subtotal:,.0f}"])
    items_data.append(['', '', '', f"Tax ({data['tax_rate']}%):", f"Rs.{tax:,.0f}"])
    items_data.append(['', '', '', 'TOTAL:', f"Rs.{total:,.0f}"])

    items_table = Table(items_data, colWidths=[0.4*inch, 3*inch, 0.6*inch, 1*inch, 1*inch])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -2), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -4), [colors.white, colors.lightgrey]),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 12),
        ('BACKGROUND', (0, -1), (-1, -1), colors.darkblue),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.white),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(items_table)
    elements.append(Spacer(1, 20))

    # Notes
    if data.get('notes'):
        elements.append(Paragraph("<b>Notes:</b>", styles['Heading3']))
        elements.append(Paragraph(data['notes'], styles['Normal']))
        elements.append(Spacer(1, 10))

    # Payment info
    elements.append(Paragraph("<b>Payment Details:</b>", styles['Heading3']))
    elements.append(Paragraph(f"Bank: {data['bank_name']}", styles['Normal']))
    elements.append(Paragraph(f"Account: {data['account_no']}", styles['Normal']))
    elements.append(Paragraph(f"UPI: {data['upi_id']}", styles['Normal']))

    doc.build(elements)
    return buffer.getvalue()

# App
st.set_page_config(
    page_title="AI Invoice Generator",
    page_icon="🧾",
    layout="wide"
)

st.title("🧾 AI Invoice Generator")
st.markdown("Generate professional invoices instantly")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 👤 Your Details")
    from_name = st.text_input("Your Name:", value="Priyanka Late")
    from_email = st.text_input("Your Email:", value="priyanka@email.com")
    from_address = st.text_input("Your Address:", value="Surat, Gujarat, India")

    st.markdown("### 🏢 Client Details")
    to_name = st.text_input("Client Name:")
    to_company = st.text_input("Client Company:")
    to_email = st.text_input("Client Email:")

with col2:
    st.markdown("### 📋 Invoice Details")
    invoice_no = st.text_input("Invoice No:", value="INV-001")
    inv_date = st.date_input("Invoice Date:", value=date.today())
    due_date = st.date_input("Due Date:")
    tax_rate = st.number_input("Tax Rate (%):", value=18, min_value=0, max_value=100)

    st.markdown("### 🏦 Payment Details")
    bank_name = st.text_input("Bank Name:")
    account_no = st.text_input("Account Number:")
    upi_id = st.text_input("UPI ID:")

# Items
st.markdown("---")
st.markdown("### 📝 Items")

if 'invoice_items' not in st.session_state:
    st.session_state.invoice_items = [
        {"description": "", "qty": 1, "rate": 0}
    ]

for i, item in enumerate(st.session_state.invoice_items):
    col1, col2, col3, col4 = st.columns([4, 1, 1, 1])
    with col1:
        st.session_state.invoice_items[i]['description'] = st.text_input(
            f"Description {i+1}:", 
            value=item['description'],
            key=f"desc_{i}"
        )
    with col2:
        st.session_state.invoice_items[i]['qty'] = st.number_input(
            "Qty:", value=item['qty'], min_value=1, key=f"qty_{i}"
        )
    with col3:
        st.session_state.invoice_items[i]['rate'] = st.number_input(
            "Rate (Rs.):", value=item['rate'], min_value=0, key=f"rate_{i}"
        )
    with col4:
        amount = item['qty'] * item['rate']
        st.metric("Amount", f"Rs.{amount:,}")

col1, col2 = st.columns(2)
with col1:
    if st.button("➕ Add Item", key="add_item"):
        st.session_state.invoice_items.append({"description": "", "qty": 1, "rate": 0})
        st.rerun()
with col2:
    if len(st.session_state.invoice_items) > 1:
        if st.button("➖ Remove Last", key="remove_item"):
            st.session_state.invoice_items.pop()
            st.rerun()

# Notes
notes = st.text_area("Notes (optional):", placeholder="Payment terms, thank you message...")

# Total preview
subtotal = sum(i['qty'] * i['rate'] for i in st.session_state.invoice_items)
tax = subtotal * tax_rate / 100
total = subtotal + tax

st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Subtotal", f"Rs.{subtotal:,}")
with col2:
    st.metric(f"Tax ({tax_rate}%)", f"Rs.{tax:,.0f}")
with col3:
    st.metric("Total", f"Rs.{total:,.0f}")

# Generate
st.markdown("---")
if st.button("🧾 Generate Invoice PDF", type="primary", use_container_width=True):
    if not to_name:
        st.warning("Please enter client name!")
    else:
        data = {
            'from_name': from_name,
            'from_email': from_email,
            'from_address': from_address,
            'to_name': to_name,
            'to_company': to_company,
            'to_email': to_email,
            'invoice_no': invoice_no,
            'date': str(inv_date),
            'due_date': str(due_date),
            'tax_rate': tax_rate,
            'invoice_items': st.session_state.invoice_items,
            'notes': notes,
            'bank_name': bank_name,
            'account_no': account_no,
            'upi_id': upi_id
        }
        
        with st.spinner("Generating PDF..."):
            pdf_bytes = generate_invoice(data)
        
        st.success("✅ Invoice generated!")
        st.download_button(
            label="📥 Download Invoice PDF",
            data=pdf_bytes,
            file_name=f"{invoice_no}.pdf",
            mime="application/pdf"
        )
