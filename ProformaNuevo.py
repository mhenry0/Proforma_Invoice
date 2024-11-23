import pandas as pd
from datetime import datetime
from weasyprint import HTML
import os

# Function to gather input from the user
def get_user_input():
    # Gather details for the invoice
    customer_name = input("Enter the name of the customer: ")
    agency_name = input("Enter the name of the agency (code name): ")
    reservations_agent = input("Enter the name of the reservations agent: ")
    room_type = input("Enter the type of room (e.g., Single, Double, Suite): ")
    
    try:
        num_people = int(input("Enter the number of people: "))
        if num_people <= 0:
            print("Error: Number of people must be greater than 0.")
            return
        price_per_night = float(input("Enter the price per night per person (in USD): "))
        if price_per_night <= 0:
            print("Error: Price per night must be greater than 0.")
            return
        tax_rate = float(input("Enter the tax rate (as a percentage, e.g., 13 for 13%): "))
        if tax_rate < 0:
            print("Error: Tax rate must not be negative.")
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

    # Calculate total price and tax
    subtotal = num_people * price_per_night * total_days
    tax_amount = subtotal * (tax_rate / 100)
    total_price = subtotal + tax_amount

    # Return all collected data
    return {
        'customer_name': customer_name,
        'agency_name': agency_name,
        'reservations_agent': reservations_agent,
        'room_type': room_type,
        'num_people': num_people,
        'price_per_night': price_per_night,
        'tax_rate': tax_rate,
        'start_date': start_date,
        'end_date': end_date,
        'total_days': total_days,
        'subtotal': subtotal,
        'tax_amount': tax_amount,
        'total_price': total_price
    }

# Function to sanitize file name by removing unwanted characters
def sanitize_filename(filename):
    # Replace spaces with underscores and remove non-alphanumeric characters
    filename = filename.replace(" ", "_")
    filename = ''.join(e for e in filename if e.isalnum() or e == "_")
    return filename

# Function to generate HTML invoice
def generate_html_invoice(data):
    html_content = f"""
 <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Proforma Invoice</title>
    <link rel="stylesheet" href="./styles.css">
</head>
<body>
    <div class="container">
        <header>
            <div class="logo">
                <img src="logo.png" alt="Wildlife Reserve Logo">
            </div>
            <div class="invoice-header">
                <h1>PROFORMA INVOICE</h1>
                <p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d')}</p>
            </div>
        </header>

        <section class="customer-details">
            <h2>Customer Details</h2>
            <table>
                <tr>
                    <td><strong>Customer Name:</strong></td>
                    <td>{data['customer_name']}</td>
                </tr>
                <tr>
                    <td><strong>Agency:</strong></td>
                    <td>{data['agency_name']}</td>
                </tr>
                <tr>
                    <td><strong>Reservations Agent:</strong></td>
                    <td>{data['reservations_agent']}</td>
                </tr>
                <tr>
                    <td><strong>Room Type:</strong></td>
                    <td>{data['room_type']}</td>
                </tr>
                <tr>
                    <td><strong>Stay Dates:</strong></td>
                    <td>{data['start_date']} to {data['end_date']} ({data['total_days']} nights)</td>
                </tr>
            </table>
        </section>

        <section class="pricing-details">
            <h2>Pricing Details</h2>
            <table>
                <tr>
                    <td><strong>Price per Night (per person):</strong></td>
                    <td>${data['price_per_night']:.2f}</td>
                </tr>
                <tr>
                    <td><strong>Subtotal:</strong></td>
                    <td>${data['subtotal']:.2f}</td>
                </tr>
                <tr>
                    <td><strong>Tax ({data['tax_rate']}%):</strong></td>
                    <td>${data['tax_amount']:.2f}</td>
                </tr>
                <tr>
                    <td><strong>Total Price:</strong></td>
                    <td>${data['total_price']:.2f}</td>
                </tr>
            </table>
        </section>

        <section class="payment-info">
            <h2>Payment Instructions</h2>
            <p>Please make the payment via bank transfer to the following account:</p>
            <p><strong>Account Number:</strong> 123456789</p>
            <p><strong>Bank Name:</strong> XYZ Bank</p>
            <p><strong>SWIFT Code:</strong> XYZ123</p>
        </section>

        <section class="terms-conditions">
            <h2>Terms & Conditions</h2>
            <p>Please read the following terms carefully:</p>
            <ul>
                <li>Payment is due within 7 days of receiving the invoice.</li>
                <li>Cancellations must be made at least 48 hours in advance for a full refund.</li>
                <li>Any modifications to the reservation may incur additional charges.</li>
                <li>All services provided are subject to availability.</li>
            </ul>
        </section>

        <section class="social-media">
            <h2>Follow Us on Social Media</h2>
            <p>Stay updated with our latest news, promotions, and events:</p>
            <ul>
                <li><a href="https://www.facebook.com/ecosdelbosque" target="_blank">Facebook</a></li>
                <li><a href="https://www.instagram.com/ecosdelbosque" target="_blank">Instagram</a></li>
                <li><a href="https://twitter.com/ecosdelbosque" target="_blank">Twitter</a></li>
                <li><a href="https://www.linkedin.com/company/ecosdelbosque" target="_blank">LinkedIn</a></li>
            </ul>
        </section>

        <footer>
            <p>Contact: 
                <a href="mailto:info@wildlifereserve.com">info@wildlifereserve.com</a> | 
                <a href="http://www.ecosdelbosquereserve.com" target="_blank">www.ecosdelbosquereserve.com</a>
            </p>
            <p>© 2024 Ecos del Bosque Wildlife Reserve</p>
            <p>Thank you for choosing Ecos del Bosque for your nature getaway!</p>
        </footer>
    </div>
</body>
</html>
"""
    return html_content

# Function to save HTML file
def save_html_to_file(html_content, agency_name, customer_name):
    # Generate a sanitized file name
    filename = f"Proforma_Invoice_{sanitize_filename(agency_name)}_{sanitize_filename(customer_name)}.html"
    with open(filename, "w") as file:
        file.write(html_content)
    print(f"Proforma invoice saved as {filename}")

# Function to save PDF file using WeasyPrint
def save_pdf_from_html(html_content, agency_name, customer_name):
    # Generate a sanitized file name
    filename = f"Proforma_Invoice_{sanitize_filename(agency_name)}_{sanitize_filename(customer_name)}.pdf"
    HTML(string=html_content).write_pdf(filename)
    print(f"Proforma invoice saved as {filename}")

# Main function to run the script
def main():
    user_data = get_user_input()
    if user_data:
        html_content = generate_html_invoice(user_data)
        
        # Ask user for file format
        print("\nChoose the file format to save:")
        print("1. HTML")
        print("2. PDF")
        choice = input("Enter the number corresponding to your choice: ")
        
        if choice == '1':
            save_html_to_file(html_content, user_data['agency_name'], user_data['customer_name'])
        elif choice == '2':
            save_pdf_from_html(html_content, user_data['agency_name'], user_data['customer_name'])
        else:
            print("Invalid choice. Exiting.")
            return

if __name__ == "__main__":
    main()
