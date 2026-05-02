"""
Test PDF Generator
Creates sample PDF files for testing the OCR extraction system.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os
from datetime import datetime, timedelta

OUTPUT_DIR = "test_pdfs"


def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def build_pdf(filename, story):
    file_path = os.path.join(OUTPUT_DIR, filename)
    doc = SimpleDocTemplate(file_path, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    doc.build(story)
    print(f"✓ Created {file_path}")
    return file_path


def create_invoice_pdf():
    """Create a sample invoice PDF with clear invoice fields."""
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=26,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=20,
    )
    story.append(Paragraph("INVOICE", title_style))

    invoice_date = datetime.now()
    due_date = invoice_date + timedelta(days=30)

    header_data = [
        [Paragraph('<b>Invoice Number:</b>', styles['Normal']), 'INV-2024-00157', Paragraph('<b>Invoice Date:</b>', styles['Normal']), invoice_date.strftime('%B %d, %Y')],
        [Paragraph('<b>Due Date:</b>', styles['Normal']), due_date.strftime('%B %d, %Y'), Paragraph('<b>Currency:</b>', styles['Normal']), 'USD'],
        [Paragraph('<b>Payment Terms:</b>', styles['Normal']), 'Net 30', '', ''],
    ]

    header_table = Table(header_data, colWidths=[1.7*inch, 2.3*inch, 1.7*inch, 1.7*inch])
    header_table.setStyle(TableStyle([
        ('SPAN', (1, 0), (1, 0)),
        ('SPAN', (1, 1), (1, 1)),
        ('SPAN', (1, 2), (3, 2)),
        ('BACKGROUND', (0, 0), (-1, -1), colors.whitesmoke),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 0.25*inch))

    vendor_data = [
        [Paragraph('<b>Vendor Name:</b>', styles['Normal']), 'Acme Corporation'],
        [Paragraph('<b>Vendor Address:</b>', styles['Normal']), '123 Business Street, New York, NY 10001'],
        [Paragraph('<b>Bill To:</b>', styles['Normal']), 'Global Enterprises'],
        [Paragraph('<b>Bill To Address:</b>', styles['Normal']), '789 Commerce Blvd, San Francisco, CA 94105']
    ]
    vendor_table = Table(vendor_data, colWidths=[1.6*inch, 4.4*inch])
    vendor_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BACKGROUND', (0, 0), (-1, 1), colors.lightgrey),
        ('BACKGROUND', (0, 2), (-1, 3), colors.whitesmoke),
    ]))
    story.append(vendor_table)
    story.append(Spacer(1, 0.3*inch))

    item_data = [
        [Paragraph('<b>Description</b>', styles['Normal']), Paragraph('<b>Quantity</b>', styles['Normal']), Paragraph('<b>Unit Price</b>', styles['Normal']), Paragraph('<b>Line Total</b>', styles['Normal'])],
        ['Professional Services', '10', '$450.00', '$4,500.00'],
        ['Software License', '1', '$1,200.00', '$1,200.00'],
        ['Technical Support', '5', '$160.00', '$800.00'],
    ]

    item_table = Table(item_data, colWidths=[3*inch, 1*inch, 1.2*inch, 1.3*inch])
    item_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(item_table)
    story.append(Spacer(1, 0.25*inch))

    totals_data = [
        ['Subtotal', '$6,500.00'],
        ['Tax Amount (15%)', '$975.00'],
        ['Total Amount', '$7,475.00'],
    ]
    totals_table = Table(totals_data, colWidths=[4.3*inch, 1.7*inch])
    totals_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('LINEABOVE', (0, -1), (-1, -1), 1, colors.black),
    ]))
    story.append(totals_table)

    return build_pdf('test_invoice.pdf', story)


def create_receipt_pdf():
    """Create a sample receipt PDF with easy-to-read payment details."""
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#228B22'),
        spaceAfter=20,
    )
    story.append(Paragraph("RECEIPT", title_style))

    receipt_date = datetime.now()

    metadata_data = [
        [Paragraph('<b>Receipt Number:</b>', styles['Normal']), 'RCP-2024-4521', Paragraph('<b>Date:</b>', styles['Normal']), receipt_date.strftime('%B %d, %Y %I:%M %p')],
        [Paragraph('<b>Vendor Name:</b>', styles['Normal']), 'TechMart Solutions', Paragraph('<b>Payment Method:</b>', styles['Normal']), 'Credit Card'],
    ]
    metadata_table = Table(metadata_data, colWidths=[1.5*inch, 2.5*inch, 1.5*inch, 1.5*inch])
    metadata_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    story.append(metadata_table)
    story.append(Spacer(1, 0.25*inch))

    receipt_items = [
        [Paragraph('<b>Description</b>', styles['Normal']), Paragraph('<b>Qty</b>', styles['Normal']), Paragraph('<b>Price</b>', styles['Normal']), Paragraph('<b>Total</b>', styles['Normal'])],
        ['Laptop Computer', '1', '$1,200.00', '$1,200.00'],
        ['Wireless Mouse', '2', '$45.00', '$90.00'],
        ['USB-C Cable', '3', '$12.00', '$36.00'],
    ]
    receipt_table = Table(receipt_items, colWidths=[3*inch, 1*inch, 1.2*inch, 1.3*inch])
    receipt_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    story.append(receipt_table)
    story.append(Spacer(1, 0.25*inch))

    summary_data = [
        ['Subtotal', '$1,326.00'],
        ['Tax (8%)', '$106.08'],
        ['Total Amount', '$1,432.08'],
    ]
    summary_table = Table(summary_data, colWidths=[4.3*inch, 1.7*inch])
    summary_table.setStyle(TableStyle([
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('LINEABOVE', (0, -1), (-1, -1), 1, colors.black),
    ]))
    story.append(summary_table)

    return build_pdf('test_receipt.pdf', story)


def create_purchase_order_pdf():
    """Create a sample purchase order PDF suitable for testing."""
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#CC0000'),
        spaceAfter=20,
    )
    story.append(Paragraph("PURCHASE ORDER", title_style))

    po_date = datetime.now()

    po_meta = [
        [Paragraph('<b>PO Number:</b>', styles['Normal']), 'PO-2024-8832', Paragraph('<b>PO Date:</b>', styles['Normal']), po_date.strftime('%B %d, %Y')],
        [Paragraph('<b>Vendor:</b>', styles['Normal']), 'Global Supplies Inc.', Paragraph('<b>Contact:</b>', styles['Normal']), 'supplier@globalsupplies.com']
    ]
    po_table = Table(po_meta, colWidths=[1.5*inch, 2.5*inch, 1.5*inch, 1.5*inch])
    po_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    story.append(po_table)
    story.append(Spacer(1, 0.25*inch))

    po_items = [
        [Paragraph('<b>Item</b>', styles['Normal']), Paragraph('<b>Quantity</b>', styles['Normal']), Paragraph('<b>Unit Price</b>', styles['Normal']), Paragraph('<b>Total</b>', styles['Normal'])],
        ['Office Chairs', '50', '$150.00', '$7,500.00'],
        ['Desks', '25', '$300.00', '$7,500.00'],
        ['Filing Cabinets', '10', '$200.00', '$2,000.00'],
    ]
    po_items_table = Table(po_items, colWidths=[2.5*inch, 1*inch, 1.2*inch, 1.5*inch])
    po_items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkred),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ]))
    story.append(po_items_table)
    story.append(Spacer(1, 0.25*inch))

    totals_data = [
        ['Total Amount', '$17,000.00'],
        ['Tax Amount', '$1,700.00'],
        ['Grand Total', '$18,700.00'],
    ]
    totals_table = Table(totals_data, colWidths=[4.3*inch, 1.7*inch])
    totals_table.setStyle(TableStyle([
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('LINEABOVE', (0, -1), (-1, -1), 1, colors.black),
    ]))
    story.append(totals_table)

    return build_pdf('test_po.pdf', story)


def create_mismatch_invoice_pdf():
    """Create a sample invoice PDF with intentional calculation errors for testing mismatch detection."""
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=26,
        textColor=colors.HexColor('#8B0000'),
        spaceAfter=20,
    )
    story.append(Paragraph("INVOICE (WITH ERRORS)", title_style))

    invoice_date = datetime.now()
    due_date = invoice_date + timedelta(days=30)

    header_data = [
        [Paragraph('<b>Invoice Number:</b>', styles['Normal']), 'INV-2024-99999', Paragraph('<b>Invoice Date:</b>', styles['Normal']), invoice_date.strftime('%B %d, %Y')],
        [Paragraph('<b>Due Date:</b>', styles['Normal']), due_date.strftime('%B %d, %Y'), Paragraph('<b>Currency:</b>', styles['Normal']), 'USD'],
        [Paragraph('<b>Payment Terms:</b>', styles['Normal']), 'Net 30', '', ''],
    ]

    header_table = Table(header_data, colWidths=[1.7*inch, 2.3*inch, 1.7*inch, 1.7*inch])
    header_table.setStyle(TableStyle([
        ('SPAN', (1, 0), (1, 0)),
        ('SPAN', (1, 1), (1, 1)),
        ('SPAN', (1, 2), (3, 2)),
        ('BACKGROUND', (0, 0), (-1, -1), colors.whitesmoke),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 0.25*inch))

    vendor_data = [
        [Paragraph('<b>Vendor Name:</b>', styles['Normal']), 'Faulty Corp'],
        [Paragraph('<b>Vendor Address:</b>', styles['Normal']), '456 Error Street, Bug City, BC 12345'],
        [Paragraph('<b>Bill To:</b>', styles['Normal']), 'Test Company'],
        [Paragraph('<b>Bill To Address:</b>', styles['Normal']), '123 Test Ave, Validation City, VC 67890']
    ]
    vendor_table = Table(vendor_data, colWidths=[1.6*inch, 4.4*inch])
    vendor_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BACKGROUND', (0, 0), (-1, 1), colors.lightgrey),
        ('BACKGROUND', (0, 2), (-1, 3), colors.whitesmoke),
    ]))
    story.append(vendor_table)
    story.append(Spacer(1, 0.3*inch))

    item_data = [
        [Paragraph('<b>Description</b>', styles['Normal']), Paragraph('<b>Quantity</b>', styles['Normal']), Paragraph('<b>Unit Price</b>', styles['Normal']), Paragraph('<b>Line Total</b>', styles['Normal'])],
        ['Consulting Services', '5', '$200.00', '$1,000.00'],
        ['Software Development', '2', '$500.00', '$1,000.00'],
        ['Training Session', '3', '$150.00', '$450.00'],
    ]

    item_table = Table(item_data, colWidths=[3*inch, 1*inch, 1.2*inch, 1.3*inch])
    item_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8B0000')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(item_table)
    story.append(Spacer(1, 0.25*inch))

    # Intentional calculation errors:
    # Correct subtotal: 1000 + 1000 + 450 = 2450
    # Correct tax (15%): 2450 * 0.15 = 367.50
    # Correct total: 2450 + 367.50 = 2817.50
    # But we'll show wrong numbers to trigger mismatch
    totals_data = [
        ['Subtotal', '$2,450.00'],  # Correct
        ['Tax Amount (15%)', '$500.00'],  # Wrong! Should be $367.50
        ['Total Amount', '$3,000.00'],  # Wrong! Should be $2,817.50
    ]
    totals_table = Table(totals_data, colWidths=[4.3*inch, 1.7*inch])
    totals_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('LINEABOVE', (0, -1), (-1, -1), 1, colors.black),
    ]))
    story.append(totals_table)

    return build_pdf('test_mismatch_invoice.pdf', story)


if __name__ == "__main__":
    ensure_output_dir()
    print("\n📄 Generating Test PDFs...")
    print("=" * 40)

    pdfs = [
        create_invoice_pdf(),
        create_receipt_pdf(),
        create_purchase_order_pdf(),
        create_mismatch_invoice_pdf(),
    ]

    print("=" * 40)
    print(f"\n✅ Generated {len(pdfs)} test PDFs:")
    for pdf in pdfs:
        print(f"   • {pdf}")
    print("\nThese files are ready for testing in the web UI!")
