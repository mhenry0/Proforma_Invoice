from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
import os


def generate_tour_invoice():
    # Collect input from the user
    customer_name = input("Enter the name of the customer: ")
    agency_name = input("Enter the name of the agency (code name): ")
    reservations_agent = input("Enter the name of the reservations agent: ")
    
    # Ask for tour type
    print("\nSelect the type of tour:")
    tour_types = [
        "Twilight Nightwalk",
        "Nightwalk",
        "Natural History Hike",
        "Farm and Natural Medicine Combo Tour",
        "Farm Tour",
        "Medicinal Plants"
    ]
    for i, tour in enumerate(tour_types, start=1):
        print(f"{i}. {tour}")
    try:
        tour_choice = int(input("Enter the number corresponding to the tour type: "))
        if tour_choice < 1 or tour_choice > len(tour_types):
            print("Error: Invalid choice.")
            return
        tour_type = tour_types[tour_choice - 1]
    except ValueError:
        print("Error: Please enter a valid number.")
        return
    
    # Add time of the tour
    tour_time = input("Enter the time of the tour (HH:MM, 24-hour format): ")
    try:
        datetime.strptime(tour_time, "%H:%M")  # Validate time format
    except ValueError:
        print("Error: Invalid time format. Please use HH:MM in 24-hour format.")
        return

    # Ask for the number of participants
    try:
        num_participants = int(input("Enter the number of participants: "))
        if num_participants <= 0:
            print("Error: Number of participants must be greater than 0.")
            return
    except ValueError:
        print("Error: Please enter a valid number.")
        return

    # Price per person for the tour
    try:
        tour_price_per_person = float(input(f"Enter the price per person for the {tour_type} tour (in USD): "))
        if tour_price_per_person <= 0:
            print("Error: Price must be greater than 0.")
            return
    except ValueError:
        print("Error: Please enter a valid price.")
        return

    # Tax Rate
    try:
        tax_rate = float(input("Enter the tax rate (as a percentage, e.g., 13 for 13%): "))
        if tax_rate < 0:
            print("Error: Tax rate must not be negative.")
            return
    except ValueError:
        print("Error: Please enter a valid tax rate.")
        return

    # Calculate total price, tax, and total with tax
    total_price = tour_price_per_person * num_participants
    tax_amount = total_price * (tax_rate / 100)
    total_price_with_tax = total_price + tax_amount

    # Create the PDF
    pdf_filename = f"tour_invoice_{customer_name.replace(' ', '_')}.pdf"
    if os.path.exists(pdf_filename):
        print(f"Warning: {pdf_filename} already exists and will be overwritten.")
    
    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

    # Styles for the PDF content
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    normal_style = styles['Normal']
    contact_style = ParagraphStyle(name='ContactInfo', fontSize=10, textColor=colors.grey)

    # Start building the document
    elements = []

    # Add Logo
    logo_path = "/path/to/logo.jpg"  # Update the path to your logo file
    try:
        logo = Image(logo_path, width=100, height=100)
        elements.append(logo)
    except FileNotFoundError:
        print(f"Logo file not found at: {logo_path}. Proceeding without the logo.")
    except Exception as e:
        print(f"Error loading logo: {e}")

    # Company Info
    company_info = """
    <b>Your Eco Reserve</b><br/>
    Address Line 1, City, Country<br/>
    Phone: (123) 456-7890<br/>
    Email: contact@ecoreserve.com<br/>
    Website: www.ecoreserve.com
    """
    elements.append(Paragraph(company_info, contact_style))
    elements.append(Spacer(1, 12))

    # Invoice Title
    elements.append(Paragraph("TOUR INVOICE", title_style))
    elements.append(Spacer(1, 12))

    # Customer and Tour Details
    data = [
        ["Customer Name", customer_name],
        ["Agency", agency_name],
        ["Reservations Agent", reservations_agent],
        ["Tour Type", tour_type],
        ["Tour Time", tour_time],
        ["Number of Participants", num_participants],
        ["Price per Person", f"${tour_price_per_person:.2f}"],
        ["Total Price (before tax)", f"${total_price:.2f}"],
        ["Tax (%)", f"{tax_rate}%"],
        ["Tax Amount", f"${tax_amount:.2f}"],
        ["Total Price (with tax)", f"${total_price_with_tax:.2f}"]
    ]

    table = Table(data, colWidths=[200, 200])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(table)

    # Space after table
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
    doc.build(elements)
    print(f"Tour invoice generated successfully: {pdf_filename}")


generate_tour_invoice()
