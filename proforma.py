from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from io import BytesIO
import os


def generate_proforma_invoice():
    # Collect input from the user
    customer_name = input("Enter the name of the customer: ")
    agency_name = input("Enter the name of the agency (code name): ")
    reservations_agent = input("Enter the name of the reservations agent: ")
    
    try:
        num_people = int(input("Enter the number of people: "))
        if num_people <= 0:
            print("Error: Number of people must be greater than 0.")
            return
        price_per_night = float(input("Enter the price per night per person (in USD): "))
        if price_per_night <= 0:
            print("Error: Price per night must be greater than 0.")
            return
    except ValueError:
        print("Error: Please enter valid numeric values.")
        return

    start_date = input("Enter the start date of the stay (YYYY-MM-DD): ")
    end_date = input("Enter the end date of the stay (YYYY-MM-DD): ")

    try:
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        print("Error: Invalid date format. Please use YYYY-MM-DD.")
        return

    total_days = (end_date_obj - start_date_obj).days
    if total_days <= 0:
        print("Error: The end date must be after the start date.")
        return

    total_price = num_people * price_per_night * total_days

    # Create the PDF
    pdf_filename = f"proforma_invoice_{customer_name.replace(' ', '_')}.pdf"
    if os.path.exists(pdf_filename):
        print(f"Warning: {pdf_filename} already exists and will be overwritten.")
    
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

    # Styles for the PDF content
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    normal_style = styles['Normal']
    bold_style = ParagraphStyle(name='Bold', fontName='Helvetica-Bold', fontSize=12)
    contact_style = ParagraphStyle(name='ContactInfo', fontSize=10, textColor=colors.grey)

    # Start building the document
    elements = []

    # Add Hotel Logo
    logo_path = "hotel_logo.png"  # Add your logo file path here
    try:
        logo = Image(logo_path, width=100, height=100)
        elements.append(logo)
    except FileNotFoundError:
        print("Logo file not found. Proceeding without the logo.")
    except Exception as e:
        print(f"Error loading logo: {e}")

    # Hotel Information
    hotel_info = """
    <b>Hotel Name</b><br/>
    Address Line 1, City, Country<br/>
    Phone: (123) 456-7890<br/>
    Email: contact@hotel.com<br/>
    Website: www.hotel.com
    """
    hotel_info_paragraph = Paragraph(hotel_info, contact_style)
    elements.append(hotel_info_paragraph)

    # Space after hotel information
    elements.append(Spacer(1, 12))

    # Invoice Title
    elements.append(Paragraph("PROFORMA INVOICE", title_style))
    elements.append(Spacer(1, 12))

    # Customer and reservation details
    details = f"""
    <b>Customer Name:</b> {customer_name}<br/>
    <b>Agency:</b> {agency_name}<br/>
    <b>Reservations Agent:</b> {reservations_agent}<br/>
    <b>Number of People:</b> {num_people}<br/>
    <b>Stay Dates:</b> {start_date} to {end_date} ({total_days} nights)<br/>
    <b>Price per Night (per person):</b> ${price_per_night:.2f}<br/>
    <b>Total Price:</b> ${total_price:.2f}
    """
    customer_info_paragraph = Paragraph(details, normal_style)
    elements.append(customer_info_paragraph)

    # Space after customer details
    elements.append(Spacer(1, 12))

    # Additional Information
    additional_info = """
    <b>Payment Instructions:</b><br/>
    Please make the payment via bank transfer to the following account:<br/>
    Account Number: 123456789<br/>
    Bank Name: XYZ Bank<br/>
    SWIFT Code: XYZ123<br/><br/>
    <b>Contact:</b> For any questions, feel free to reach out at contact@hotel.com.
    """
    additional_info_paragraph = Paragraph(additional_info, contact_style)
    elements.append(additional_info_paragraph)

    # Save the PDF
    doc.title = None
    doc.subject = None
    doc.author = None
    doc.build(elements)

    print(f"Proforma invoice saved as {pdf_filename}")


# Run the function to generate the proforma invoice
generate_proforma_invoice()
